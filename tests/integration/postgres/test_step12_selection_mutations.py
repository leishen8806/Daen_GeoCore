# pyright: basic, reportArgumentType=false, reportAttributeAccessIssue=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportUnknownVariableType=false, reportReturnType=false, reportMissingParameterType=false, reportUnusedImport=false

import os
import threading
from datetime import UTC, datetime
from pathlib import Path

import pytest
from alembic import command as alembic_command
from alembic.config import Config
from sqlalchemy import create_engine, select

from daen_geocore.application.selection_mutations import (
    ADD_OPERATION,
    REPLACE_OPERATION,
    AddSelection,
    AddSelectionCommand,
    ReplaceSelection,
    ReplaceSelectionCommand,
    SelectionMutationOutcome,
)
from daen_geocore.application.source_assertion_withdrawal import (
    SourceAssertionWithdrawalOutcome,
    WithdrawSourceAssertion,
)
from daen_geocore.domain.references import PlaceRef, SelectionRecordRef, SourceAssertionRef
from daen_geocore.infrastructure.postgres.mutation_factory import PostgresMutationUnitOfWorkFactory
from daen_geocore.infrastructure.postgres.schema import (
    assertions_history,
    assertions_source_assertion,
    assertions_standing_head,
    identity_place,
    mutation_audit,
    mutation_committed_binding,
    representation_selection_record,
    representation_selection_slot_head,
    representation_selection_support,
)
from daen_geocore.ports.evidence.store import (
    EvidenceLookupKey,
    RequestReferenceRecoveryMapping,
)
from daen_geocore.ports.idempotency.store import IdempotencyBindingKey
from daen_geocore.ports.mutation import (
    AssertionOwner,
    MutationBasisClaims,
    ObservedOwnerState,
    OwnerAbsent,
    OwnerPresent,
    SelectionSlotOwner,
)
from daen_geocore.ports.persistence.records import (
    OpaqueEncodedPayload,
    PersistedExplicitScope,
    PersistedQualityUnknown,
    PersistedTypedValue,
    SelectionSlotKey,
    StateWitness,
)
from daen_geocore.ports.recovery.gate import RecoveryIncarnation
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueReplayMetadata,
    OpaqueRequestIdentity,
)
from tests.fakes.mutation_runtime import FakeMutationBasisCodec
from tests.integration.postgres.test_step11_source_assertion_withdrawal import _BarrierGate
from tests.integration.postgres.test_step11_source_assertion_withdrawal import (
    _command as withdraw_command,
)
from tests.integration.postgres.test_step11_source_assertion_withdrawal import (
    _seed as seed_withdrawal,
)
from tests.unit.test_source_assertion_transition import (
    Candidates,
    Evidence,
    FakeTransitionClock,
    Gate,
)

NOW = datetime(2026, 10, 9, 15, 0, tzinfo=UTC)
DATABASE_URL = os.getenv("DAEN_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="DAEN_TEST_DATABASE_URL is not configured")


def _config() -> Config:
    config = Config(str(Path("alembic.ini").resolve()))
    config.set_main_option("sqlalchemy.url", DATABASE_URL or "")
    return config


@pytest.fixture(scope="module")
def engine():
    assert DATABASE_URL is not None
    alembic_command.upgrade(_config(), "head")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    yield engine
    alembic_command.downgrade(_config(), "base")
    engine.dispose()


def _scope() -> PersistedExplicitScope:
    return PersistedExplicitScope("language", OpaqueEncodedPayload("scope", b"km"), b"km")


def _seed(engine, place: str, assertion: str) -> None:
    with engine.begin() as connection:
        connection.execute(identity_place.insert().values(place_ref=place, recorded_at=NOW))
        connection.execute(
            assertions_source_assertion.insert().values(
                source_assertion_ref=assertion,
                place_ref=place,
                fact_purpose="name",
                value_type_id="text",
                value_encoding="utf8",
                value_payload=b"source",
                scope_is_explicit=False,
                provenance_encoding="source",
                provenance_payload=b"source",
                quality_is_known=False,
                recorded_at=NOW,
            )
        )
        connection.execute(
            assertions_standing_head.insert().values(
                source_assertion_ref=assertion,
                latest_history_fact_ref=None,
                state_witness="w1",
            )
        )


def _key(request: str) -> IdempotencyBindingKey:
    return IdempotencyBindingKey(OpaqueClientIdentity("step12"), OpaqueRequestIdentity(request))


def test_postgres_selection_add_replace_and_replay(engine) -> None:
    place = PlaceRef("step12-place")
    assertion = SourceAssertionRef("step12-assertion")
    _seed(engine, place.token, assertion.token)
    scope = _scope()
    slot = SelectionSlotKey(place, "name", scope.type_id, scope.equality_key or b"")
    codec = FakeMutationBasisCodec()
    evidence = Evidence()
    add_token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (
                ObservedOwnerState(SelectionSlotOwner(slot), OwnerAbsent()),
                ObservedOwnerState(AssertionOwner(assertion), OwnerPresent(StateWitness("w1"))),
            ),
        )
    ).value
    add = AddSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        evidence,
        Gate(),
        codec,
        Candidates(),
        FakeTransitionClock(),
    )
    command = AddSelectionCommand(
        _key("add"),
        EvidenceLookupKey("step12-add"),
        IntentFingerprint("add-v1"),
        place,
        "name",
        add_token,
        scope,
        PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"selected")),
        (assertion,),
        OpaqueEncodedPayload("attribution", b"a"),
        OpaqueEncodedPayload("selection", b"p"),
        PersistedQualityUnknown(),
        OpaqueEncodedPayload("mutation", b"m"),
    )
    first = add.execute(command)
    assert first.value.outcome is SelectionMutationOutcome.APPLIED
    ref = first.value.selection_record_ref
    assert ref is not None
    replay = add.execute(command)
    assert replay.value.outcome is SelectionMutationOutcome.REPLAY
    assert replay.value.selection_record_ref == ref
    with engine.connect() as connection:
        head = (
            connection.execute(
                select(representation_selection_slot_head).where(
                    representation_selection_slot_head.c.place_ref == place.token
                )
            )
            .mappings()
            .one()
        )
    replace_token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (
                ObservedOwnerState(
                    SelectionSlotOwner(slot), OwnerPresent(StateWitness(head["state_witness"]))
                ),
                ObservedOwnerState(AssertionOwner(assertion), OwnerPresent(StateWitness("w1"))),
            ),
        )
    ).value
    replace_candidates = Candidates()
    replace_candidates.calls = 1000
    replace = ReplaceSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        evidence,
        Gate(),
        codec,
        replace_candidates,
        FakeTransitionClock(),
    )
    replacement = replace.execute(
        ReplaceSelectionCommand(
            _key("replace"),
            EvidenceLookupKey("step12-replace"),
            IntentFingerprint("replace-v1"),
            place,
            ref,
            "name",
            replace_token,
            scope,
            PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"new")),
            (assertion,),
            OpaqueEncodedPayload("attribution", b"a2"),
            OpaqueEncodedPayload("selection", b"p2"),
            PersistedQualityUnknown(),
            OpaqueEncodedPayload("mutation", b"m2"),
        )
    )
    assert replacement.value.outcome is SelectionMutationOutcome.APPLIED
    assert replacement.value.selection_record_ref != ref
    with engine.connect() as connection:
        assert connection.execute(select(representation_selection_record)).mappings().all()
        assert connection.execute(select(representation_selection_support)).mappings().all()


def _fixed_evidence(command, ref: str, witness: str) -> Evidence:
    evidence = Evidence()
    evidence.mapping[command.evidence_lookup_key] = RequestReferenceRecoveryMapping(
        command.key.client_identity,
        command.key.request_identity,
        command.intent_fingerprint,
        ADD_OPERATION if isinstance(command, AddSelectionCommand) else REPLACE_OPERATION,
        (SelectionRecordRef(ref),),
        OpaqueReplayMetadata((("state_witness", witness), ("recorded_at", NOW.isoformat()))),
    )
    return evidence


def _add_command(request: str, place: PlaceRef, assertion: SourceAssertionRef, token, ref: str):
    command = AddSelectionCommand(
        _key(request),
        EvidenceLookupKey(f"step12-{request}"),
        IntentFingerprint(f"add-{request}"),
        place,
        "name",
        token,
        _scope(),
        PersistedTypedValue("text", OpaqueEncodedPayload("utf8", request.encode())),
        (assertion,),
        OpaqueEncodedPayload("attribution", b"a"),
        OpaqueEncodedPayload("selection", b"p"),
        PersistedQualityUnknown(),
        OpaqueEncodedPayload("mutation", b"m"),
    )
    return command, _fixed_evidence(command, ref, f"w-{request}")


def _replace_command(
    request: str,
    place: PlaceRef,
    assertion: SourceAssertionRef,
    prior: SelectionRecordRef,
    token,
    ref: str,
):
    command = ReplaceSelectionCommand(
        _key(request),
        EvidenceLookupKey(f"step12-{request}"),
        IntentFingerprint(f"replace-{request}"),
        place,
        prior,
        "name",
        token,
        _scope(),
        PersistedTypedValue("text", OpaqueEncodedPayload("utf8", request.encode())),
        (assertion,),
        OpaqueEncodedPayload("attribution", b"a"),
        OpaqueEncodedPayload("selection", b"p"),
        PersistedQualityUnknown(),
        OpaqueEncodedPayload("mutation", b"m"),
    )
    return command, _fixed_evidence(command, ref, f"w-{request}")


class _Step12BarrierGate(_BarrierGate):
    pass


class _CountingEvidence(Evidence):
    def __init__(self) -> None:
        super().__init__()
        self.mapping_reads = 0

    def read_request_mapping(self, key):
        self.mapping_reads += 1
        return super().read_request_mapping(key)


def _table_counts(engine):
    with engine.connect() as connection:
        return tuple(
            len(connection.execute(select(table)).mappings().all())
            for table in (
                representation_selection_record,
                representation_selection_support,
                representation_selection_slot_head,
                mutation_audit,
                mutation_committed_binding,
            )
        )


def _run_selection_race(operations):
    results = []

    def worker(operation, command):
        results.append(operation.execute(command))

    threads = [threading.Thread(target=worker, args=item) for item in operations]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=30)
    assert all(not thread.is_alive() for thread in threads)
    return results


def test_postgres_add_add_race_has_one_current_winner(engine) -> None:
    suffix = "add-add"
    place = PlaceRef(f"step12-{suffix}-place")
    assertion = SourceAssertionRef(f"step12-{suffix}-assertion")
    _seed(engine, place.token, assertion.token)
    slot = SelectionSlotKey(place, "name", _scope().type_id, _scope().equality_key or b"")
    codec = FakeMutationBasisCodec()
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerAbsent()),),
        )
    ).value
    barrier = threading.Barrier(2)
    commands = [
        _add_command("add-add-a", place, assertion, token, "step12-add-a"),
        _add_command("add-add-b", place, assertion, token, "step12-add-b"),
    ]
    operations = [
        (
            AddSelection(
                PostgresMutationUnitOfWorkFactory(DATABASE_URL),
                evidence,
                _Step12BarrierGate(barrier),
                codec,
                Candidates(),
                FakeTransitionClock(),
            ),
            command,
        )
        for command, evidence in commands
    ]
    results = _run_selection_race(operations)
    assert (
        sum(
            getattr(getattr(result, "value", None), "outcome", None)
            is SelectionMutationOutcome.APPLIED
            for result in results
        )
        <= 1
    )
    with engine.connect() as connection:
        heads = (
            connection.execute(
                select(representation_selection_slot_head).where(
                    representation_selection_slot_head.c.place_ref == place.token
                )
            )
            .mappings()
            .all()
        )
        records = (
            connection.execute(
                select(representation_selection_record).where(
                    representation_selection_record.c.selection_record_ref.in_(
                        ["step12-add-a", "step12-add-b"]
                    )
                )
            )
            .mappings()
            .all()
        )
        links = (
            connection.execute(
                select(representation_selection_support).where(
                    representation_selection_support.c.selection_record_ref.in_(
                        ["step12-add-a", "step12-add-b"]
                    )
                )
            )
            .mappings()
            .all()
        )
        audits = (
            connection.execute(
                select(mutation_audit).where(
                    mutation_audit.c.request_identity.in_(["add-add-a", "add-add-b"])
                )
            )
            .mappings()
            .all()
        )
        bindings = (
            connection.execute(
                select(mutation_committed_binding).where(
                    mutation_committed_binding.c.request_identity.in_(["add-add-a", "add-add-b"])
                )
            )
            .mappings()
            .all()
        )
    assert len(heads) == 1
    assert len(records) == 1
    assert len(links) == 1
    assert len(audits) == 1
    assert len(bindings) == 1


def _seed_selection(engine, suffix: str):
    place = PlaceRef(f"step12-{suffix}-place")
    assertion = SourceAssertionRef(f"step12-{suffix}-assertion")
    _seed(engine, place.token, assertion.token)
    codec = FakeMutationBasisCodec()
    slot = SelectionSlotKey(place, "name", _scope().type_id, _scope().equality_key or b"")
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerAbsent()),),
        )
    ).value
    command, evidence = _add_command(
        f"{suffix}-seed", place, assertion, token, f"step12-{suffix}-s1"
    )
    result = AddSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        evidence,
        Gate(),
        codec,
        Candidates(),
        FakeTransitionClock(),
    ).execute(command)
    assert result.value.outcome is SelectionMutationOutcome.APPLIED
    with engine.connect() as connection:
        head = (
            connection.execute(
                select(representation_selection_slot_head).where(
                    representation_selection_slot_head.c.place_ref == place.token
                )
            )
            .mappings()
            .one()
        )
    return (
        place,
        assertion,
        slot,
        SelectionRecordRef(head["selection_record_ref"]),
        StateWitness(head["state_witness"]),
        codec,
    )


def test_postgres_replace_replace_race_has_one_final_replacement(engine) -> None:
    place, assertion, slot, prior, witness, codec = _seed_selection(engine, "replace-replace")
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerPresent(witness)),),
        )
    ).value
    barrier = threading.Barrier(2)
    commands = [
        _replace_command("replace-a", place, assertion, prior, token, "step12-replace-a"),
        _replace_command("replace-b", place, assertion, prior, token, "step12-replace-b"),
    ]
    operations = [
        (
            ReplaceSelection(
                PostgresMutationUnitOfWorkFactory(DATABASE_URL),
                evidence,
                _Step12BarrierGate(barrier),
                codec,
                Candidates(),
                FakeTransitionClock(),
            ),
            command,
        )
        for command, evidence in commands
    ]
    results = _run_selection_race(operations)
    assert (
        sum(
            getattr(getattr(result, "value", None), "outcome", None)
            is SelectionMutationOutcome.APPLIED
            for result in results
        )
        <= 1
    )
    with engine.connect() as connection:
        head = (
            connection.execute(
                select(representation_selection_slot_head).where(
                    representation_selection_slot_head.c.place_ref == place.token
                )
            )
            .mappings()
            .one()
        )
        replacement_rows = (
            connection.execute(
                select(representation_selection_record).where(
                    representation_selection_record.c.selection_record_ref.in_(
                        ["step12-replace-a", "step12-replace-b"]
                    )
                )
            )
            .mappings()
            .all()
        )
        links = (
            connection.execute(
                select(representation_selection_support).where(
                    representation_selection_support.c.selection_record_ref.in_(
                        ["step12-replace-a", "step12-replace-b"]
                    )
                )
            )
            .mappings()
            .all()
        )
        audits = (
            connection.execute(
                select(mutation_audit).where(
                    mutation_audit.c.request_identity.in_(["replace-a", "replace-b"])
                )
            )
            .mappings()
            .all()
        )
        bindings = (
            connection.execute(
                select(mutation_committed_binding).where(
                    mutation_committed_binding.c.request_identity.in_(["replace-a", "replace-b"])
                )
            )
            .mappings()
            .all()
        )
    assert head["selection_record_ref"] in {"step12-replace-a", "step12-replace-b"}
    assert head["state_witness"] != witness.value
    assert len(replacement_rows) == 1
    assert len(links) == 1
    assert len(audits) == 1
    assert len(bindings) == 1


def test_postgres_add_t2_withdrawal_does_not_use_support_owner_basis(engine) -> None:
    suffix = "add-t2"
    target = seed_withdrawal(engine, suffix)
    place = PlaceRef(f"place-{suffix}")
    slot = SelectionSlotKey(place, "address", _scope().type_id, _scope().equality_key or b"")
    codec = FakeMutationBasisCodec()
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerAbsent()),),
        )
    ).value
    command, evidence = _add_command(suffix, place, target, token, f"step12-{suffix}")
    barrier = threading.Barrier(2)
    add = AddSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        evidence,
        _Step12BarrierGate(barrier),
        codec,
        Candidates(),
        FakeTransitionClock(),
    )
    withdraw = WithdrawSourceAssertion(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        _Step12BarrierGate(barrier),
        Candidates(),
        FakeTransitionClock(),
    )
    results = _run_selection_race([(add, command), (withdraw, withdraw_command(suffix, target))])
    outcomes = [getattr(result.value, "outcome", None) for result in results]
    assert (
        SourceAssertionWithdrawalOutcome.APPLIED in outcomes
        or SelectionMutationOutcome.SUPPORT_ASSERTION_WITHDRAWN in outcomes
        or SelectionMutationOutcome.SUPPORT_ASSERTION_STATE_CHANGED in outcomes
    )


def test_postgres_replace_t2_withdrawal_does_not_use_support_owner_basis(engine) -> None:
    place, assertion, slot, prior, witness, codec = _seed_selection(engine, "replace-t2")
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerPresent(witness)),),
        )
    ).value
    command, evidence = _replace_command(
        "replace-t2", place, assertion, prior, token, "step12-replace-t2"
    )
    barrier = threading.Barrier(2)
    replace = ReplaceSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        evidence,
        _Step12BarrierGate(barrier),
        codec,
        Candidates(),
        FakeTransitionClock(),
    )
    withdraw = WithdrawSourceAssertion(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        _Step12BarrierGate(barrier),
        Candidates(),
        FakeTransitionClock(),
    )
    results = _run_selection_race(
        [(replace, command), (withdraw, withdraw_command("replace-t2", assertion))]
    )
    outcomes = [getattr(result.value, "outcome", None) for result in results]
    assert (
        SourceAssertionWithdrawalOutcome.APPLIED in outcomes
        or SelectionMutationOutcome.SUPPORT_ASSERTION_WITHDRAWN in outcomes
        or SelectionMutationOutcome.SUPPORT_ASSERTION_STATE_CHANGED in outcomes
    )


def test_postgres_add_rolls_back_after_audit_conflict(engine) -> None:
    suffix = "add-rollback"
    place = PlaceRef(f"step12-{suffix}-place")
    assertion = SourceAssertionRef(f"step12-{suffix}-assertion")
    _seed(engine, place.token, assertion.token)
    codec = FakeMutationBasisCodec()
    slot = SelectionSlotKey(place, "name", _scope().type_id, _scope().equality_key or b"")
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerAbsent()),),
        )
    ).value
    command, evidence = _add_command(suffix, place, assertion, token, f"step12-{suffix}")
    with engine.begin() as connection:
        connection.execute(
            mutation_audit.insert().values(
                client_identity=command.key.client_identity.value,
                request_identity=command.key.request_identity.value,
                intent_fingerprint=command.intent_fingerprint.value,
                operation_key=ADD_OPERATION.value,
                recorded_at=NOW,
                mutation_provenance_encoding="seed",
                mutation_provenance_payload=b"seed",
                audit_details_encoding="seed",
                audit_details_payload=b"seed",
            )
        )
    result = AddSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        evidence,
        Gate(),
        codec,
        Candidates(),
        FakeTransitionClock(),
    ).execute(command)
    assert result.value.outcome is SelectionMutationOutcome.AUDIT_CONFLICT
    with engine.connect() as connection:
        assert (
            connection.execute(
                select(representation_selection_record).where(
                    representation_selection_record.c.selection_record_ref == f"step12-{suffix}"
                )
            ).first()
            is None
        )
        assert (
            connection.execute(
                select(representation_selection_slot_head).where(
                    representation_selection_slot_head.c.place_ref == place.token
                )
            ).first()
            is None
        )


def test_postgres_replace_rolls_back_after_audit_conflict(engine) -> None:
    place, assertion, slot, prior, witness, codec = _seed_selection(engine, "replace-rollback")
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerPresent(witness)),),
        )
    ).value
    command, evidence = _replace_command(
        "replace-rollback", place, assertion, prior, token, "step12-replace-rollback"
    )
    with engine.begin() as connection:
        connection.execute(
            mutation_audit.insert().values(
                client_identity=command.key.client_identity.value,
                request_identity=command.key.request_identity.value,
                intent_fingerprint=command.intent_fingerprint.value,
                operation_key=REPLACE_OPERATION.value,
                recorded_at=NOW,
                mutation_provenance_encoding="seed",
                mutation_provenance_payload=b"seed",
                audit_details_encoding="seed",
                audit_details_payload=b"seed",
            )
        )
    result = ReplaceSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        evidence,
        Gate(),
        codec,
        Candidates(),
        FakeTransitionClock(),
    ).execute(command)
    assert result.value.outcome is SelectionMutationOutcome.AUDIT_CONFLICT
    with engine.connect() as connection:
        head = (
            connection.execute(
                select(representation_selection_slot_head).where(
                    representation_selection_slot_head.c.place_ref == place.token
                )
            )
            .mappings()
            .one()
        )
    assert head["selection_record_ref"] == prior.token
    assert head["state_witness"] == witness.value


def test_postgres_add_replay_precedes_stale_basis_and_side_effects(engine) -> None:
    place = PlaceRef("step12-add-replay-place")
    assertion = SourceAssertionRef("step12-add-replay-assertion")
    _seed(engine, place.token, assertion.token)
    codec = FakeMutationBasisCodec()
    slot = SelectionSlotKey(place, "name", _scope().type_id, _scope().equality_key or b"")
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerAbsent()),),
        )
    ).value
    command = AddSelectionCommand(
        _key("add-replay"),
        EvidenceLookupKey("step12-add-replay"),
        IntentFingerprint("add-replay"),
        place,
        "name",
        token,
        _scope(),
        PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"value")),
        (assertion,),
        OpaqueEncodedPayload("attribution", b"a"),
        OpaqueEncodedPayload("selection", b"p"),
        PersistedQualityUnknown(),
        OpaqueEncodedPayload("mutation", b"m"),
    )
    evidence = _CountingEvidence()
    ref = SelectionRecordRef("step12-add-replay-ref")
    evidence.mapping[command.evidence_lookup_key] = RequestReferenceRecoveryMapping(
        command.key.client_identity,
        command.key.request_identity,
        command.intent_fingerprint,
        ADD_OPERATION,
        (ref,),
        OpaqueReplayMetadata(
            (("state_witness", "step12-add-replay-w"), ("recorded_at", NOW.isoformat()))
        ),
    )
    candidates = Candidates()
    clock = FakeTransitionClock()
    operation = AddSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL), evidence, Gate(), codec, candidates, clock
    )
    assert operation.execute(command).value.outcome is SelectionMutationOutcome.APPLIED
    counts = _table_counts(engine)
    counters = (evidence.mapping_reads, evidence.reservation_writes, candidates.calls, clock.calls)
    replay = operation.execute(command)
    assert replay.value.outcome is SelectionMutationOutcome.REPLAY
    assert replay.value.selection_record_ref == ref
    assert _table_counts(engine) == counts
    assert (
        evidence.mapping_reads,
        evidence.reservation_writes,
        candidates.calls,
        clock.calls,
    ) == counters


def test_postgres_replace_replay_precedes_stale_basis_and_side_effects(engine) -> None:
    place, assertion, slot, prior, witness, codec = _seed_selection(engine, "replace-replay")
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerPresent(witness)),),
        )
    ).value
    command, evidence = _replace_command(
        "replace-replay", place, assertion, prior, token, "step12-replace-replay-ref"
    )
    evidence = _CountingEvidence()
    evidence.mapping[command.evidence_lookup_key] = RequestReferenceRecoveryMapping(
        command.key.client_identity,
        command.key.request_identity,
        command.intent_fingerprint,
        REPLACE_OPERATION,
        (
            SelectionRecordRef(command.prior_selection_record_ref.token),
            SelectionRecordRef("step12-replace-replay-ref"),
        ),
        OpaqueReplayMetadata(
            (("state_witness", "step12-replace-replay-w"), ("recorded_at", NOW.isoformat()))
        ),
    )
    candidates = Candidates()
    clock = FakeTransitionClock()
    operation = ReplaceSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL), evidence, Gate(), codec, candidates, clock
    )
    assert operation.execute(command).value.outcome is SelectionMutationOutcome.APPLIED
    counts = _table_counts(engine)
    counters = (evidence.mapping_reads, evidence.reservation_writes, candidates.calls, clock.calls)
    replay = operation.execute(command)
    assert replay.value.outcome is SelectionMutationOutcome.REPLAY
    assert replay.value.selection_record_ref == SelectionRecordRef("step12-replace-replay-ref")
    assert replay.value.prior_selection_record_ref == prior
    assert _table_counts(engine) == counts
    assert (
        evidence.mapping_reads,
        evidence.reservation_writes,
        candidates.calls,
        clock.calls,
    ) == counters


def test_postgres_withdrawn_support_rejects_before_recovery(engine) -> None:
    target = seed_withdrawal(engine, "withdrawn-support")
    withdrawal = WithdrawSourceAssertion(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL), Gate(), Candidates(), FakeTransitionClock()
    ).execute(withdraw_command("withdrawn-support", target))
    assert withdrawal.value.outcome is SourceAssertionWithdrawalOutcome.APPLIED
    place = PlaceRef("place-withdrawn-support")
    slot = SelectionSlotKey(place, "address", _scope().type_id, _scope().equality_key or b"")
    codec = FakeMutationBasisCodec()
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerAbsent()),),
        )
    ).value
    command, evidence = _add_command(
        "withdrawn-support", place, target, token, "step12-withdrawn-support"
    )
    candidates = Candidates()
    clock = FakeTransitionClock()
    result = AddSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL), evidence, Gate(), codec, candidates, clock
    ).execute(command)
    assert result.value.outcome is SelectionMutationOutcome.SUPPORT_ASSERTION_WITHDRAWN
    assert evidence.mapping_reads == 0
    assert candidates.calls == 0
    assert clock.calls == 0


def test_postgres_superseded_support_remains_usable(engine) -> None:
    suffix = "superseded-support"
    place = PlaceRef(f"step12-{suffix}-place")
    assertion = SourceAssertionRef(f"step12-{suffix}-assertion")
    _seed(engine, place.token, assertion.token)
    with engine.begin() as connection:
        connection.execute(
            assertions_history.insert().values(
                history_fact_ref=f"step12-{suffix}-history",
                source_assertion_ref=assertion.token,
                fact_type="source_assertion.superseded_by",
                related_source_assertion_ref=assertion.token,
                recorded_at=NOW,
                history_metadata_encoding=None,
                history_metadata_payload=None,
            )
        )
        connection.execute(
            assertions_standing_head.update()
            .where(assertions_standing_head.c.source_assertion_ref == assertion.token)
            .values(latest_history_fact_ref=f"step12-{suffix}-history", state_witness="w2")
        )
    codec = FakeMutationBasisCodec()
    slot = SelectionSlotKey(place, "name", _scope().type_id, _scope().equality_key or b"")
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerAbsent()),),
        )
    ).value
    command, evidence = _add_command(suffix, place, assertion, token, f"step12-{suffix}")
    result = AddSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        evidence,
        Gate(),
        codec,
        Candidates(),
        FakeTransitionClock(),
    ).execute(command)
    assert result.value.outcome is SelectionMutationOutcome.APPLIED


def test_postgres_support_place_mismatch_and_unknown_support_are_preflight_errors(engine) -> None:
    place_a = PlaceRef("step12-support-place-a")
    place_b = PlaceRef("step12-support-place-b")
    assertion_a = SourceAssertionRef("step12-support-assertion-a")
    assertion_b = SourceAssertionRef("step12-support-assertion-b")
    _seed(engine, place_a.token, assertion_a.token)
    _seed(engine, place_b.token, assertion_b.token)
    codec = FakeMutationBasisCodec()
    slot = SelectionSlotKey(place_a, "name", _scope().type_id, _scope().equality_key or b"")
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(SelectionSlotOwner(slot), OwnerAbsent()),),
        )
    ).value
    mismatch, mismatch_evidence = _add_command(
        "support-mismatch", place_a, assertion_b, token, "step12-support-mismatch"
    )
    unknown, unknown_evidence = _add_command(
        "support-unknown",
        place_a,
        SourceAssertionRef("missing-support"),
        token,
        "step12-support-unknown",
    )
    mismatch_result = AddSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        mismatch_evidence,
        Gate(),
        codec,
        Candidates(),
        FakeTransitionClock(),
    ).execute(mismatch)
    unknown_result = AddSelection(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        unknown_evidence,
        Gate(),
        codec,
        Candidates(),
        FakeTransitionClock(),
    ).execute(unknown)
    assert (
        mismatch_result.value.outcome is SelectionMutationOutcome.SUPPORT_ASSERTION_PLACE_MISMATCH
    )
    assert unknown_result.value.outcome is SelectionMutationOutcome.SUPPORT_ASSERTION_NOT_FOUND
    assert getattr(mismatch_evidence, "mapping_reads", 0) == 0
    assert getattr(unknown_evidence, "mapping_reads", 0) == 0
