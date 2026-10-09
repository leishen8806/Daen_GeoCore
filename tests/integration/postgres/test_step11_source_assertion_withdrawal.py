# pyright: basic, reportArgumentType=false, reportAttributeAccessIssue=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportUnknownVariableType=false, reportMissingParameterType=false, reportReturnType=false, reportUnusedImport=false

import os
import threading
from datetime import UTC, datetime
from pathlib import Path

import pytest
from alembic import command as alembic_command
from alembic.config import Config
from sqlalchemy import create_engine, func, select

from daen_geocore.application.source_assertion_transition import (
    CORRECTION_FACT_TYPE,
    SUPERSESSION_FACT_TYPE,
    CorrectSourceAssertion,
    CorrectSourceAssertionCommand,
    SourceAssertionTransitionOutcome,
    SupersedeSourceAssertion,
    SupersedeSourceAssertionCommand,
)
from daen_geocore.application.source_assertion_withdrawal import (
    WITHDRAW_FACT_TYPE,
    SourceAssertionWithdrawalOutcome,
    WithdrawSourceAssertion,
    WithdrawSourceAssertionCommand,
)
from daen_geocore.domain.references import SourceAssertionRef
from daen_geocore.infrastructure.postgres.mutation_factory import PostgresMutationUnitOfWorkFactory
from daen_geocore.infrastructure.postgres.schema import (
    assertions_history,
    assertions_source_assertion,
    assertions_standing_head,
    identity_place,
    mutation_audit,
    mutation_committed_binding,
)
from daen_geocore.ports.evidence.store import EvidenceLookupKey
from daen_geocore.ports.idempotency.store import IdempotencyBindingKey
from daen_geocore.ports.mutation import (
    AssertionOwner,
    MutationBasisClaims,
    ObservedOwnerState,
    OwnerPresent,
)
from daen_geocore.ports.persistence.records import (
    OpaqueEncodedPayload,
    PersistedQualityUnknown,
    PersistedTypedValue,
    PersistedUnknownScope,
    StateWitness,
)
from daen_geocore.ports.recovery.gate import RecoveryIncarnation
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueRequestIdentity,
)
from tests.fakes.mutation_runtime import FakeMutationBasisCodec
from tests.unit.test_source_assertion_transition import (
    Candidates,
    Evidence,
    FakeTransitionClock,
    Gate,
)

DATABASE_URL = os.getenv("DAEN_TEST_DATABASE_URL")
NOW = datetime(2026, 10, 9, 14, 0, tzinfo=UTC)
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


def _seed(engine, request: str, *, with_head: bool = True):
    old_ref = f"old-{request}"
    place_ref = f"place-{request}"
    with engine.begin() as connection:
        connection.execute(identity_place.insert().values(place_ref=place_ref, recorded_at=NOW))
        connection.execute(
            assertions_source_assertion.insert().values(
                source_assertion_ref=old_ref,
                place_ref=place_ref,
                fact_purpose="address",
                value_type_id="text",
                value_encoding="utf8",
                value_payload=b"original",
                scope_is_explicit=False,
                provenance_encoding="source",
                provenance_payload=b"original-source",
                quality_is_known=False,
                recorded_at=NOW,
            )
        )
        if with_head:
            connection.execute(
                assertions_standing_head.insert().values(
                    source_assertion_ref=old_ref,
                    latest_history_fact_ref=None,
                    state_witness="w1",
                )
            )
    return SourceAssertionRef(old_ref)


def _command(request: str, target: SourceAssertionRef) -> WithdrawSourceAssertionCommand:
    return WithdrawSourceAssertionCommand(
        IdempotencyBindingKey(
            OpaqueClientIdentity(f"step11-{request}"), OpaqueRequestIdentity(request)
        ),
        IntentFingerprint("withdraw-v1"),
        target,
        OpaqueEncodedPayload("mutation", b"operator"),
    )


def _withdraw(command, candidates=None, gate=None, clock=None):
    if candidates is None:
        candidates = Candidates()
        candidates.calls = sum(
            (index + 1) * ord(char) for index, char in enumerate(command.key.request_identity.value)
        )
    return WithdrawSourceAssertion(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        gate or Gate(),
        candidates,
        clock or FakeTransitionClock(),
    ).execute(command)


def _count(connection, table):
    return connection.execute(select(func.count()).select_from(table)).scalar_one()


def test_postgres_withdraw_happy_path_and_replays(engine) -> None:
    target = _seed(engine, "happy")
    command = _command("happy", target)
    result = _withdraw(command)
    assert result.value.outcome is SourceAssertionWithdrawalOutcome.APPLIED
    with engine.connect() as connection:
        source = (
            connection.execute(
                select(assertions_source_assertion).where(
                    assertions_source_assertion.c.source_assertion_ref == target.token
                )
            )
            .mappings()
            .one()
        )
        facts = (
            connection.execute(
                select(assertions_history).where(
                    assertions_history.c.source_assertion_ref == target.token
                )
            )
            .mappings()
            .all()
        )
        head = (
            connection.execute(
                select(assertions_standing_head).where(
                    assertions_standing_head.c.source_assertion_ref == target.token
                )
            )
            .mappings()
            .one()
        )
        counts = (_count(connection, assertions_history), _count(connection, mutation_audit))
    assert source["provenance_payload"] == b"original-source"
    assert len(facts) == 1 and facts[0]["fact_type"] == WITHDRAW_FACT_TYPE
    assert facts[0]["related_source_assertion_ref"] is None
    assert head["latest_history_fact_ref"] == facts[0]["history_fact_ref"]
    assert head["state_witness"] != "w1"
    replay = _withdraw(command)
    assert replay.value.outcome is SourceAssertionWithdrawalOutcome.REPLAY
    assert replay.value.replayed_outcome is SourceAssertionWithdrawalOutcome.APPLIED
    with engine.connect() as connection:
        assert (
            _count(connection, assertions_history),
            _count(connection, mutation_audit),
        ) == counts


def test_postgres_already_holds_is_bound_and_replays(engine) -> None:
    target = _seed(engine, "already")
    first = _withdraw(_command("already-first", target))
    assert first.value.outcome is SourceAssertionWithdrawalOutcome.APPLIED
    with engine.connect() as connection:
        before = (_count(connection, assertions_history), _count(connection, mutation_audit))
    second_command = _command("already-second", target)
    second = _withdraw(second_command)
    assert second.value.outcome is SourceAssertionWithdrawalOutcome.ALREADY_HOLDS
    replay = _withdraw(second_command)
    assert replay.value.outcome is SourceAssertionWithdrawalOutcome.REPLAY
    assert replay.value.replayed_outcome is SourceAssertionWithdrawalOutcome.ALREADY_HOLDS
    with engine.connect() as connection:
        assert _count(connection, assertions_history) == before[0]
        assert _count(connection, mutation_audit) == before[1] + 1
        assert _count(connection, mutation_committed_binding) >= 2


def test_postgres_atomic_rollback_and_fail_closed_reads(engine) -> None:
    target = _seed(engine, "rollback")
    command = _command("rollback", target)
    with engine.begin() as connection:
        connection.execute(
            mutation_audit.insert().values(
                client_identity=command.key.client_identity.value,
                request_identity=command.key.request_identity.value,
                intent_fingerprint="other",
                operation_key="other",
                recorded_at=NOW,
                mutation_provenance_encoding="mutation",
                mutation_provenance_payload=b"old",
                audit_details_encoding="audit",
                audit_details_payload=b"old",
            )
        )
    before = None
    with engine.connect() as connection:
        before = (
            _count(connection, assertions_history),
            _count(connection, assertions_standing_head),
        )
    result = _withdraw(command)
    assert result.value.outcome is SourceAssertionWithdrawalOutcome.AUDIT_CONFLICT
    with engine.connect() as connection:
        assert (
            _count(connection, assertions_history),
            _count(connection, assertions_standing_head),
        ) == before
    missing = _withdraw(_command("unknown", SourceAssertionRef("missing")))
    assert missing.value.outcome is SourceAssertionWithdrawalOutcome.TARGET_ASSERTION_NOT_FOUND
    no_head = _seed(engine, "no-head", with_head=False)
    assert (
        _withdraw(_command("no-head", no_head)).value.outcome
        is SourceAssertionWithdrawalOutcome.TARGET_STANDING_HEAD_MISSING
    )


class _BarrierGate:
    def __init__(self, barrier: threading.Barrier) -> None:
        self._barrier = barrier
        self._calls = 0
        self._lock = threading.Lock()

    def observation(self):
        with self._lock:
            first = self._calls == 0
            self._calls += 1
        if first:
            self._barrier.wait(timeout=15)
        return Gate().observation()

    def validate_before_authoritative_serving(self):
        return Gate().validate_before_authoritative_serving()


def _race_t2(engine, other_kind: str, request: str):
    target = _seed(engine, request)
    barrier = threading.Barrier(2)
    codec = FakeMutationBasisCodec()
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(AssertionOwner(target), OwnerPresent(StateWitness("w1"))),),
        )
    ).value
    results = []

    def t2_worker():
        results.append(
            (
                (f"step11-{request}-t2", f"{request}-t2"),
                _withdraw(_command(f"{request}-t2", target), gate=_BarrierGate(barrier)),
            )
        )

    def other_worker():
        common = dict(
            key=IdempotencyBindingKey(
                OpaqueClientIdentity(f"{request}-other"), OpaqueRequestIdentity(request)
            ),
            evidence_lookup_key=EvidenceLookupKey(f"{request}-evidence"),
            intent_fingerprint=IntentFingerprint(other_kind),
            target_source_assertion_ref=target,
            mutation_basis=token,
            value=PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"replacement")),
            scope=PersistedUnknownScope(),
            source_provenance=OpaqueEncodedPayload("source", b"other"),
            quality=PersistedQualityUnknown(),
            mutation_provenance=OpaqueEncodedPayload("mutation", b"other"),
        )
        command_type = (
            SupersedeSourceAssertionCommand
            if other_kind == "supersede"
            else CorrectSourceAssertionCommand
        )
        command = command_type(**common)
        operation_type = (
            SupersedeSourceAssertion if other_kind == "supersede" else CorrectSourceAssertion
        )
        candidates = Candidates()
        candidates.calls = sum((index + 1) * ord(char) for index, char in enumerate(request)) + 1000
        results.append(
            (
                (f"{request}-other", request),
                operation_type(
                    PostgresMutationUnitOfWorkFactory(DATABASE_URL),
                    Evidence(),
                    _BarrierGate(barrier),
                    codec,
                    candidates,
                    FakeTransitionClock(),
                ).execute(command),
            )
        )

    threads = [threading.Thread(target=t2_worker), threading.Thread(target=other_worker)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=20)
    assert all(not thread.is_alive() for thread in threads)
    return results, target


def test_postgres_t2_supersede_and_correct_races_have_one_original_winner(engine) -> None:
    for kind in ("supersede", "correct"):
        results, target = _race_t2(engine, kind, f"race-{kind}")
        outcomes = [result.value.outcome for _, result in results if hasattr(result, "value")]
        total_applied = sum(
            outcome is SourceAssertionWithdrawalOutcome.APPLIED
            or outcome is SourceAssertionTransitionOutcome.APPLIED
            for outcome in outcomes
        )
        assert total_applied <= 1
        with engine.connect() as connection:
            facts = (
                connection.execute(
                    select(assertions_history).where(
                        assertions_history.c.source_assertion_ref == target.token
                    )
                )
                .mappings()
                .all()
            )
            head = (
                connection.execute(
                    select(assertions_standing_head).where(
                        assertions_standing_head.c.source_assertion_ref == target.token
                    )
                )
                .mappings()
                .one()
            )
            bindings = (
                connection.execute(
                    select(mutation_committed_binding).where(
                        mutation_committed_binding.c.client_identity.in_(
                            [f"step11-race-{kind}-t2", f"race-{kind}-other"]
                        )
                    )
                )
                .mappings()
                .all()
            )
            audits = (
                connection.execute(
                    select(mutation_audit).where(
                        mutation_audit.c.client_identity.in_(
                            [f"step11-race-{kind}-t2", f"race-{kind}-other"]
                        )
                    )
                )
                .mappings()
                .all()
            )
            candidate_offset = (
                sum((index + 1) * ord(char) for index, char in enumerate(f"race-{kind}")) + 1001
            )
            proposed_ref = f"new-{candidate_offset}"
            replacement = (
                connection.execute(
                    select(assertions_source_assertion).where(
                        assertions_source_assertion.c.source_assertion_ref == proposed_ref
                    )
                )
                .mappings()
                .all()
            )
        withdrawal_count = sum(fact["fact_type"] == WITHDRAW_FACT_TYPE for fact in facts)
        supersession_count = sum(fact["fact_type"] == SUPERSESSION_FACT_TYPE for fact in facts)
        correction_count = sum(fact["fact_type"] == CORRECTION_FACT_TYPE for fact in facts)
        assert withdrawal_count + supersession_count == 1
        assert head["state_witness"] != "w1"
        if withdrawal_count == 1:
            assert supersession_count == 0 and correction_count == 0
            assert head["latest_history_fact_ref"] == next(
                fact["history_fact_ref"]
                for fact in facts
                if fact["fact_type"] == WITHDRAW_FACT_TYPE
            )
            assert not replacement
        else:
            assert supersession_count == 1
            if kind == "correct":
                assert correction_count == 1
                assert head["latest_history_fact_ref"] == next(
                    fact["history_fact_ref"]
                    for fact in facts
                    if fact["fact_type"] == CORRECTION_FACT_TYPE
                )
            else:
                assert correction_count == 0
                assert head["latest_history_fact_ref"] == next(
                    fact["history_fact_ref"]
                    for fact in facts
                    if fact["fact_type"] == SUPERSESSION_FACT_TYPE
                )
            assert replacement
        assert len(bindings) <= 1
        assert len(audits) <= 1
        if total_applied == 1:
            assert len(bindings) == 1
            assert len(audits) == 1
            applied_identities = {
                identity
                for identity, result in results
                if hasattr(result, "value")
                and (
                    result.value.outcome is SourceAssertionTransitionOutcome.APPLIED
                    or result.value.outcome is SourceAssertionWithdrawalOutcome.APPLIED
                )
            }
            assert len(applied_identities) == 1
            assert bindings[0]["client_identity"] == next(iter(applied_identities))[0]
            assert audits[0]["client_identity"] == next(iter(applied_identities))[0]


def test_postgres_t2_t2_race_has_one_withdrawal_fact(engine) -> None:
    target = _seed(engine, "race-t2-t2")
    barrier = threading.Barrier(2)
    results = []

    def worker(suffix: str):
        candidates = Candidates()
        candidates.calls = 10000 if suffix == "a" else 20000
        results.append(
            _withdraw(
                _command(f"race-t2-t2-{suffix}", target),
                gate=_BarrierGate(barrier),
                candidates=candidates,
            )
        )

    threads = [
        threading.Thread(target=worker, args=("a",)),
        threading.Thread(target=worker, args=("b",)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=20)
    assert all(not thread.is_alive() for thread in threads)
    assert (
        sum(
            getattr(getattr(result, "value", None), "outcome", None)
            is SourceAssertionWithdrawalOutcome.APPLIED
            for result in results
        )
        <= 1
    )
    with engine.connect() as connection:
        facts = (
            connection.execute(
                select(assertions_history).where(
                    assertions_history.c.source_assertion_ref == target.token
                )
            )
            .mappings()
            .all()
        )
    assert sum(fact["fact_type"] == WITHDRAW_FACT_TYPE for fact in facts) == 1
