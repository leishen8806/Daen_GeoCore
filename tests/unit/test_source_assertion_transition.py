# pyright: basic, reportArgumentType=false, reportAttributeAccessIssue=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportUnknownVariableType=false, reportMissingParameterType=false, reportReturnType=false, reportUnusedImport=false

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime

from daen_geocore.application.source_assertion_transition import (
    CORRECTION_FACT_TYPE,
    SUPERSEDE_OPERATION,
    SUPERSESSION_FACT_TYPE,
    CorrectSourceAssertion,
    CorrectSourceAssertionCommand,
    SourceAssertionTransitionOutcome,
    SupersedeSourceAssertion,
    SupersedeSourceAssertionCommand,
)
from daen_geocore.domain.references import PlaceRef, SourceAssertionRef
from daen_geocore.ports.audit.store import MutationAuditRecord
from daen_geocore.ports.clock import Clock
from daen_geocore.ports.evidence.store import (
    EvidenceAbsent,
    EvidenceCreated,
    EvidenceFound,
    EvidenceLookupKey,
    ReferenceReservationEvidence,
    RequestReferenceRecoveryMapping,
)
from daen_geocore.ports.idempotency.store import IdempotencyBindingKey
from daen_geocore.ports.mutation import (
    AssertionOwner,
    MutationBasisClaims,
    ObservedOwnerState,
    OwnerPresent,
)
from daen_geocore.ports.persistence.commit import CommitAccepted
from daen_geocore.ports.persistence.records import (
    AssertionHistoryFact,
    AssertionHistoryFactRef,
    AssertionStandingHead,
    ConditionalWriteDisposition,
    InsertDisposition,
    OpaqueEncodedPayload,
    PersistedQualityUnknown,
    PersistedTypedValue,
    PersistedUnknownScope,
    RecordAbsent,
    RecordFound,
    SourceAssertionRecord,
    StateWitness,
)
from daen_geocore.ports.recovery.gate import RecoveryIncarnation, RecoveryObservation, RecoveryState
from daen_geocore.ports.result import PortSuccess
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueReplayMetadata,
    OpaqueRequestIdentity,
)
from tests.fakes.mutation_runtime import FakeMutationBasisCodec, InMemoryCommittedIdempotencyStore

NOW = datetime(2026, 10, 9, 12, 0, tzinfo=UTC)


class Evidence:
    def __init__(self) -> None:
        self.mapping: dict[EvidenceLookupKey, RequestReferenceRecoveryMapping] = {}
        self.reservations: dict[EvidenceLookupKey, ReferenceReservationEvidence] = {}
        self.reservation_writes = 0

    def read_request_mapping(self, key):
        value = self.mapping.get(key)
        return PortSuccess(EvidenceAbsent() if value is None else EvidenceFound(value))

    def create_request_mapping_if_absent(self, key, record):
        if key not in self.mapping:
            self.mapping[key] = record
            return PortSuccess(EvidenceCreated())
        return PortSuccess(EvidenceCreated() if self.mapping[key] == record else object())

    def create_reservation_if_absent(self, key, record):
        self.reservation_writes += 1
        if key not in self.reservations:
            self.reservations[key] = record
            return PortSuccess(EvidenceCreated())
        from daen_geocore.ports.evidence.store import EvidenceAlreadyPresentSame

        return PortSuccess(EvidenceAlreadyPresentSame())

    def read_reservation(self, key):
        value = self.reservations.get(key)
        return PortSuccess(EvidenceAbsent() if value is None else EvidenceFound(value))


class Gate:
    def observation(self):
        return RecoveryObservation(RecoveryState.READY, RecoveryIncarnation("r1"))

    def validate_before_authoritative_serving(self):
        return PortSuccess(RecoveryIncarnation("r1"))


class Candidates:
    def __init__(self) -> None:
        self.calls = 0

    def _value(self, prefix):
        self.calls += 1
        return f"{prefix}-{self.calls}"

    def new_source_assertion_ref(self):
        return SourceAssertionRef(self._value("new"))

    def new_state_witness(self):
        return StateWitness(self._value("witness"))

    def new_assertion_history_fact_ref(self):
        return AssertionHistoryFactRef(self._value("history"))

    def new_place_ref(self):
        return PlaceRef(self._value("place"))

    def new_selection_record_ref(self):
        from daen_geocore.domain.references import SelectionRecordRef

        return SelectionRecordRef(self._value("selection"))

    def new_access_point_ref(self):
        from daen_geocore.domain.references import AccessPointRef

        return AccessPointRef(self._value("access"))

    def new_place_history_fact_ref(self):
        from daen_geocore.ports.persistence.records import PlaceHistoryFactRef

        return PlaceHistoryFactRef(self._value("place-history"))


class FakeTransitionClock(Clock):
    def __init__(self) -> None:
        self.calls = 0

    def now(self):
        self.calls += 1
        return NOW


@dataclass
class Assertions:
    records: dict[SourceAssertionRef, SourceAssertionRecord] = field(default_factory=dict)
    heads: dict[SourceAssertionRef, AssertionStandingHead] = field(default_factory=dict)
    history: dict[SourceAssertionRef, list[AssertionHistoryFact]] = field(default_factory=dict)

    def get_assertion(self, ref):
        value = self.records.get(ref)
        return PortSuccess(RecordAbsent() if value is None else RecordFound(value))

    def get_standing_head(self, ref):
        value = self.heads.get(ref)
        return PortSuccess(RecordAbsent() if value is None else RecordFound(value))

    def list_assertion_history(self, ref):
        return PortSuccess(tuple(self.history.get(ref, ())))

    def insert_assertion_if_absent(self, record):
        existing = self.records.get(record.source_assertion_ref)
        if existing is None:
            self.records[record.source_assertion_ref] = record
            return PortSuccess(InsertDisposition.INSERTED)
        return PortSuccess(
            InsertDisposition.ALREADY_PRESENT_SAME
            if existing == record
            else InsertDisposition.CONFLICTING_EXISTING
        )

    def insert_standing_head_if_absent(self, head):
        if head.source_assertion_ref not in self.heads:
            self.heads[head.source_assertion_ref] = head
            return PortSuccess(InsertDisposition.INSERTED)
        return PortSuccess(InsertDisposition.CONFLICTING_EXISTING)

    def append_assertion_history_if_absent(self, fact):
        items = self.history.setdefault(fact.source_assertion_ref, [])
        if any(item.history_fact_ref == fact.history_fact_ref for item in items):
            return PortSuccess(InsertDisposition.ALREADY_PRESENT_SAME)
        items.append(fact)
        return PortSuccess(InsertDisposition.INSERTED)

    def compare_and_swap_standing_head(self, ref, expected, latest, witness):
        current = self.heads.get(ref)
        if current is None or current.state_witness != expected:
            return PortSuccess(ConditionalWriteDisposition.PRECONDITION_NOT_MET)
        self.heads[ref] = AssertionStandingHead(ref, latest, witness)
        return PortSuccess(ConditionalWriteDisposition.APPLIED)


class Uow:
    def __init__(self, assertions, committed, audit):
        self.identity = object()
        self.assertions = assertions
        self.representation = object()
        self.committed_idempotency = committed
        self.mutation_audit = audit

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def commit(self):
        return CommitAccepted()

    def rollback(self):
        return None


class Factory:
    def __init__(self, assertions, committed, audit):
        self.assertions, self.committed, self.audit = assertions, committed, audit

    def create(self):
        return Uow(self.assertions, self.committed, self.audit)


class Audit:
    def __init__(self):
        self.records = {}

    def append_if_absent(self, record: MutationAuditRecord):
        if record.key in self.records:
            return PortSuccess(InsertDisposition.CONFLICTING_EXISTING)
        self.records[record.key] = record
        return PortSuccess(InsertDisposition.INSERTED)

    def read(self, key):
        return PortSuccess(self.records.get(key))


def _command(kind, token):
    common = dict(
        key=IdempotencyBindingKey(OpaqueClientIdentity("client"), OpaqueRequestIdentity(kind)),
        evidence_lookup_key=EvidenceLookupKey(f"evidence-{kind}"),
        intent_fingerprint=IntentFingerprint(kind),
        target_source_assertion_ref=SourceAssertionRef("old"),
        mutation_basis=token,
        value=PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"new")),
        scope=PersistedUnknownScope(),
        source_provenance=OpaqueEncodedPayload("source", b"origin"),
        quality=PersistedQualityUnknown(),
        mutation_provenance=OpaqueEncodedPayload("mutation", b"actor"),
    )
    return (
        SupersedeSourceAssertionCommand(**common)
        if kind == "supersede"
        else CorrectSourceAssertionCommand(**common)
    )


def _setup():
    old = SourceAssertionRecord(
        SourceAssertionRef("old"),
        PlaceRef("place"),
        "address",
        PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"old")),
        PersistedUnknownScope(),
        OpaqueEncodedPayload("source", b"old-source"),
        PersistedQualityUnknown(),
        NOW,
    )
    assertions = Assertions(
        {old.source_assertion_ref: old},
        {
            old.source_assertion_ref: AssertionStandingHead(
                old.source_assertion_ref, None, StateWitness("w1")
            )
        },
    )
    committed = InMemoryCommittedIdempotencyStore()
    audit = Audit()
    codec = FakeMutationBasisCodec()
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (
                ObservedOwnerState(
                    AssertionOwner(old.source_assertion_ref), OwnerPresent(StateWitness("w1"))
                ),
            ),
        )
    ).value
    evidence, candidates, clock = Evidence(), Candidates(), FakeTransitionClock()
    factory = Factory(assertions, committed, audit)
    return old, assertions, committed, audit, codec, token, evidence, candidates, clock, factory


def test_supersede_creates_new_assertion_and_one_history_fact() -> None:
    old, assertions, _, audit, codec, token, evidence, candidates, clock, factory = _setup()
    result = SupersedeSourceAssertion(factory, evidence, Gate(), codec, candidates, clock).execute(
        _command("supersede", token)
    )
    assert result.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    new_ref = result.value.new_source_assertion_ref
    assert new_ref is not None and assertions.records[new_ref].place_ref == old.place_ref
    assert assertions.records[new_ref].fact_purpose == old.fact_purpose
    assert len(assertions.history[old.source_assertion_ref]) == 1
    assert assertions.history[old.source_assertion_ref][0].fact_type == SUPERSESSION_FACT_TYPE
    assert len(audit.records) == 1
    assert clock.calls == 1 and candidates.calls == 4


def test_correct_creates_supersession_and_correction_history() -> None:
    old, assertions, _, _, codec, token, evidence, candidates, clock, factory = _setup()
    result = CorrectSourceAssertion(factory, evidence, Gate(), codec, candidates, clock).execute(
        _command("correct", token)
    )
    assert result.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    facts = assertions.history[old.source_assertion_ref]
    assert {fact.fact_type for fact in facts} == {SUPERSESSION_FACT_TYPE, CORRECTION_FACT_TYPE}


def test_replay_precedes_basis_and_recovery_and_cross_operation_conflicts() -> None:
    old, assertions, committed, _, codec, token, evidence, candidates, clock, factory = _setup()
    operation = SupersedeSourceAssertion(factory, evidence, Gate(), codec, candidates, clock)
    command = _command("supersede", token)
    first = operation.execute(command)
    assert first.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    calls, ticks = candidates.calls, clock.calls
    replay = operation.execute(command)
    assert replay.value.outcome is SourceAssertionTransitionOutcome.REPLAY
    assert candidates.calls == calls and clock.calls == ticks
    conflict = CorrectSourceAssertion(factory, evidence, Gate(), codec, candidates, clock).execute(
        replace(_command("supersede", token), mutation_basis=token)
    )
    assert conflict.value.outcome is SourceAssertionTransitionOutcome.IDEMPOTENCY_CONFLICT
    assert old.source_assertion_ref in assertions.records
    assert committed.bindings


def test_stale_basis_precedes_existing_supersession_and_has_no_side_effects() -> None:
    old, assertions, _, _, codec, token, evidence, candidates, clock, factory = _setup()
    operation = SupersedeSourceAssertion(factory, evidence, Gate(), codec, candidates, clock)
    first = operation.execute(_command("supersede", token))
    assert first.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    assertions.history[old.source_assertion_ref].append(
        AssertionHistoryFact(
            AssertionHistoryFactRef("existing"),
            old.source_assertion_ref,
            SUPERSESSION_FACT_TYPE,
            NOW,
            first.value.new_source_assertion_ref,
        )
    )
    candidates.calls = 0
    clock.calls = 0
    evidence.reservation_writes = 0
    result = operation.execute(
        replace(
            _command("supersede", token),
            key=IdempotencyBindingKey(
                OpaqueClientIdentity("client-2"), OpaqueRequestIdentity("stale")
            ),
        )
    )
    assert result.value.outcome is SourceAssertionTransitionOutcome.STALE_BASIS
    assert candidates.calls == 0 and clock.calls == 0 and evidence.reservation_writes == 0


def test_fresh_basis_after_supersession_returns_already_superseded_without_generation() -> None:
    old, assertions, _, _, codec, token, evidence, candidates, clock, factory = _setup()
    operation = SupersedeSourceAssertion(factory, evidence, Gate(), codec, candidates, clock)
    first = operation.execute(_command("supersede", token))
    assert first.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    new_ref = first.value.new_source_assertion_ref
    assert new_ref is not None
    assertions.heads[old.source_assertion_ref] = AssertionStandingHead(
        old.source_assertion_ref, AssertionHistoryFactRef("existing"), StateWitness("w2")
    )
    fresh = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (
                ObservedOwnerState(
                    AssertionOwner(old.source_assertion_ref), OwnerPresent(StateWitness("w2"))
                ),
            ),
        )
    ).value
    candidates.calls = 0
    clock.calls = 0
    evidence.reservation_writes = 0
    result = operation.execute(
        replace(
            _command("supersede", fresh),
            key=IdempotencyBindingKey(
                OpaqueClientIdentity("client-3"), OpaqueRequestIdentity("fresh")
            ),
        )
    )
    assert result.value.outcome is SourceAssertionTransitionOutcome.TARGET_ALREADY_SUPERSEDED
    assert candidates.calls == 0 and clock.calls == 0 and evidence.reservation_writes == 0


def test_valid_mapping_retry_reuses_all_transition_material() -> None:
    old, assertions, _, _, codec, token, evidence, candidates, clock, factory = _setup()
    command = _command("supersede", token)
    evidence.mapping[command.evidence_lookup_key] = RequestReferenceRecoveryMapping(
        command.key.client_identity,
        command.key.request_identity,
        command.intent_fingerprint,
        SUPERSEDE_OPERATION,
        (SourceAssertionRef("recovered"),),
        OpaqueReplayMetadata(
            (
                ("new_source_assertion_ref", "recovered"),
                ("new_assertion_witness", "new-witness"),
                ("replacement_witness", "replacement"),
                ("supersession_history_ref", "history"),
                ("recorded_at", NOW.isoformat()),
            )
        ),
    )
    mapping = next(iter(evidence.mapping.values()))
    retry = SupersedeSourceAssertion(factory, evidence, Gate(), codec, candidates, clock).execute(
        command
    )
    assert retry.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    assert candidates.calls == 0 and clock.calls == 0
    assert mapping.references[0] == retry.value.new_source_assertion_ref
    assert old.source_assertion_ref in assertions.records
