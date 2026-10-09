# pyright: basic, reportArgumentType=false, reportAttributeAccessIssue=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportUnknownVariableType=false, reportMissingParameterType=false, reportReturnType=false, reportUnusedImport=false

import os
import threading
from dataclasses import replace
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
from tests.unit.test_source_assertion_create import FakeEvidence
from tests.unit.test_source_assertion_transition import Candidates, FakeTransitionClock, Gate

DATABASE_URL = os.getenv("DAEN_TEST_DATABASE_URL")
NOW = datetime(2026, 10, 9, 13, 0, tzinfo=UTC)
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


def _command(kind: str, token, request: str):
    common = dict(
        key=IdempotencyBindingKey(OpaqueClientIdentity("step10"), OpaqueRequestIdentity(request)),
        evidence_lookup_key=EvidenceLookupKey(f"step10-{request}"),
        intent_fingerprint=IntentFingerprint(kind),
        target_source_assertion_ref=SourceAssertionRef(f"old-{request}"),
        mutation_basis=token,
        value=PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"replacement")),
        scope=PersistedUnknownScope(),
        source_provenance=OpaqueEncodedPayload("source", b"source"),
        quality=PersistedQualityUnknown(),
        mutation_provenance=OpaqueEncodedPayload("mutation", b"mutation"),
    )
    return (
        SupersedeSourceAssertionCommand(**common)
        if kind == "supersede"
        else CorrectSourceAssertionCommand(**common)
    )


def _seed(engine, request: str):
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
                value_payload=b"old",
                scope_is_explicit=False,
                provenance_encoding="source",
                provenance_payload=b"old-source",
                quality_is_known=False,
                recorded_at=NOW,
            )
        )
        connection.execute(
            assertions_standing_head.insert().values(
                source_assertion_ref=old_ref,
                latest_history_fact_ref=None,
                state_witness="w1",
            )
        )


def _run(engine, kind: str, request: str):
    _seed(engine, request)
    codec = FakeMutationBasisCodec()
    old_ref = SourceAssertionRef(f"old-{request}")
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(AssertionOwner(old_ref), OwnerPresent(StateWitness("w1"))),),
        )
    ).value
    command = _command(kind, token, request)
    candidates = Candidates()
    candidates.calls = sum((index + 1) * ord(char) for index, char in enumerate(request)) + (
        100000 if kind == "correct" else 0
    )
    operation = (SupersedeSourceAssertion if kind == "supersede" else CorrectSourceAssertion)(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        FakeEvidence(),
        Gate(),
        codec,
        candidates,
        FakeTransitionClock(),
    )
    return operation.execute(command), old_ref, token, command, operation, codec


def _count(connection, table, column=None):
    target = func.count() if column is None else func.count(column)
    return connection.execute(select(target).select_from(table)).scalar_one()


def test_postgres_supersede_happy_path(engine) -> None:
    result, old_ref, _, _, _, _ = _run(engine, "supersede", "pg-supersede")
    assert result.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    with engine.connect() as connection:
        facts = (
            connection.execute(
                select(assertions_history).where(
                    assertions_history.c.source_assertion_ref == old_ref.token
                )
            )
            .mappings()
            .all()
        )
        assert len(facts) == 1 and facts[0]["fact_type"] == SUPERSESSION_FACT_TYPE


def test_postgres_correct_happy_path(engine) -> None:
    result, old_ref, _, _, _, _ = _run(engine, "correct", "pg-correct")
    assert result.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    with engine.connect() as connection:
        facts = (
            connection.execute(
                select(assertions_history).where(
                    assertions_history.c.source_assertion_ref == old_ref.token
                )
            )
            .mappings()
            .all()
        )
        assert {fact["fact_type"] for fact in facts} == {
            SUPERSESSION_FACT_TYPE,
            CORRECTION_FACT_TYPE,
        }


def test_postgres_stale_basis_precedes_existing_supersession(engine) -> None:
    result, old_ref, token, command, operation, _ = _run(engine, "supersede", "pg-stale")
    assert result.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    with engine.connect() as connection:
        before = (
            _count(connection, assertions_source_assertion),
            _count(connection, assertions_history),
            _count(connection, assertions_standing_head),
            _count(connection, mutation_audit),
            _count(connection, mutation_committed_binding),
        )
        head = connection.execute(
            select(assertions_standing_head.c.state_witness).where(
                assertions_standing_head.c.source_assertion_ref == old_ref.token
            )
        ).scalar_one()
    assert head != "w1"
    loser = replace(
        command,
        key=IdempotencyBindingKey(
            OpaqueClientIdentity("step10-stale-loser"), OpaqueRequestIdentity("request")
        ),
        evidence_lookup_key=EvidenceLookupKey("step10-stale-loser"),
        mutation_basis=token,
    )
    loser_result = operation.execute(loser)
    assert loser_result.value.outcome is SourceAssertionTransitionOutcome.STALE_BASIS
    with engine.connect() as connection:
        after = (
            _count(connection, assertions_source_assertion),
            _count(connection, assertions_history),
            _count(connection, assertions_standing_head),
            _count(connection, mutation_audit),
            _count(connection, mutation_committed_binding),
        )
    assert after == before


def test_postgres_fresh_basis_after_supersession_has_no_second_branch(engine) -> None:
    result, old_ref, _, command, operation, codec = _run(engine, "supersede", "pg-fresh")
    assert result.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    with engine.connect() as connection:
        witness = connection.execute(
            select(assertions_standing_head.c.state_witness).where(
                assertions_standing_head.c.source_assertion_ref == old_ref.token
            )
        ).scalar_one()
    fresh = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(AssertionOwner(old_ref), OwnerPresent(StateWitness(witness))),),
        )
    ).value
    retry = replace(
        command,
        key=IdempotencyBindingKey(
            OpaqueClientIdentity("step10-fresh-loser"), OpaqueRequestIdentity("request")
        ),
        evidence_lookup_key=EvidenceLookupKey("step10-fresh-loser"),
        mutation_basis=fresh,
    )
    retry_result = operation.execute(retry)
    assert retry_result.value.outcome is SourceAssertionTransitionOutcome.TARGET_ALREADY_SUPERSEDED
    with engine.connect() as connection:
        facts = connection.execute(
            select(assertions_history).where(
                assertions_history.c.source_assertion_ref == old_ref.token
            )
        ).all()
    assert sum(fact.fact_type == SUPERSESSION_FACT_TYPE for fact in facts) == 1


def test_postgres_committed_replay_does_not_change_counts(engine) -> None:
    result, _, _, command, operation, _ = _run(engine, "supersede", "pg-replay")
    assert result.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    with engine.connect() as connection:
        before = (
            _count(connection, assertions_source_assertion),
            _count(connection, assertions_history),
            _count(connection, assertions_standing_head),
            _count(connection, mutation_audit),
            _count(connection, mutation_committed_binding),
        )
    replay = operation.execute(command)
    assert replay.value.outcome is SourceAssertionTransitionOutcome.REPLAY
    with engine.connect() as connection:
        after = (
            _count(connection, assertions_source_assertion),
            _count(connection, assertions_history),
            _count(connection, assertions_standing_head),
            _count(connection, mutation_audit),
            _count(connection, mutation_committed_binding),
        )
    assert after == before


def test_postgres_atomic_rollback_after_staged_transition(engine) -> None:
    result, old_ref, _, command, operation, codec = _run(engine, "supersede", "pg-rollback-setup")
    assert result.value.outcome is SourceAssertionTransitionOutcome.APPLIED
    # This test uses a fresh target and a pre-existing audit row to fail after staging.
    _seed(engine, "pg-rollback")
    rollback_ref = SourceAssertionRef("old-pg-rollback")
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(AssertionOwner(rollback_ref), OwnerPresent(StateWitness("w1"))),),
        )
    ).value
    command = _command("supersede", token, "pg-rollback")
    with engine.begin() as connection:
        connection.execute(
            mutation_audit.insert().values(
                client_identity=command.key.client_identity.value,
                request_identity=command.key.request_identity.value,
                intent_fingerprint="preexisting",
                operation_key="preexisting",
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
            _count(connection, assertions_source_assertion),
            _count(connection, assertions_history),
            _count(connection, assertions_standing_head),
        )
    rollback_result = operation.execute(command)
    assert rollback_result.value.outcome is SourceAssertionTransitionOutcome.AUDIT_CONFLICT
    with engine.connect() as connection:
        after = (
            _count(connection, assertions_source_assertion),
            _count(connection, assertions_history),
            _count(connection, assertions_standing_head),
        )
    assert after == before


class _BarrierCandidates(Candidates):
    def __init__(self, barrier: threading.Barrier, prefix: str) -> None:
        super().__init__()
        self._barrier = barrier
        self._prefix = prefix
        self._waited = False
        self.calls = sum((index + 1) * ord(char) for index, char in enumerate(prefix))

    def new_source_assertion_ref(self):
        if not self._waited:
            self._waited = True
            self._barrier.wait(timeout=10)
        self.calls += 1
        return SourceAssertionRef(f"{self._prefix}-new-{self.calls}")


def _race(engine, first_kind: str, second_kind: str, request: str):
    _seed(engine, request)
    old_ref = SourceAssertionRef(f"old-{request}")
    codec = FakeMutationBasisCodec()
    token = codec.issue(
        MutationBasisClaims(
            RecoveryIncarnation("r1"),
            (ObservedOwnerState(AssertionOwner(old_ref), OwnerPresent(StateWitness("w1"))),),
        )
    ).value
    barrier = threading.Barrier(2)
    results = []

    def run(kind: str, suffix: str):
        command = _command(kind, token, f"{request}-{suffix}")
        command = replace(
            command,
            target_source_assertion_ref=old_ref,
            key=IdempotencyBindingKey(
                OpaqueClientIdentity(f"step10-{suffix}"), OpaqueRequestIdentity(request)
            ),
            evidence_lookup_key=EvidenceLookupKey(f"step10-{request}-{suffix}"),
        )
        candidates = _BarrierCandidates(barrier, suffix)
        operation_cls = SupersedeSourceAssertion if kind == "supersede" else CorrectSourceAssertion
        operation = operation_cls(
            PostgresMutationUnitOfWorkFactory(DATABASE_URL),
            FakeEvidence(),
            Gate(),
            codec,
            candidates,
            FakeTransitionClock(),
        )
        results.append(operation.execute(command))

    threads = [
        threading.Thread(target=run, args=(first_kind, "left")),
        threading.Thread(target=run, args=(second_kind, "right")),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=20)
    assert all(not thread.is_alive() for thread in threads)
    return results, old_ref


def _assert_one_branch(engine, old_ref: SourceAssertionRef, results) -> None:
    outcomes = [item.value.outcome for item in results if hasattr(item, "value")]
    assert outcomes.count(SourceAssertionTransitionOutcome.APPLIED) <= 1
    with engine.connect() as connection:
        facts = connection.execute(
            select(assertions_history).where(
                assertions_history.c.source_assertion_ref == old_ref.token
            )
        ).all()
        assert sum(fact.fact_type == SUPERSESSION_FACT_TYPE for fact in facts) == 1
        assert _count(connection, assertions_standing_head) >= 1


def test_postgres_concurrent_supersede_supersede_has_one_winner(engine) -> None:
    results, old_ref = _race(engine, "supersede", "supersede", "pg-race-ss")
    _assert_one_branch(engine, old_ref, results)


def test_postgres_concurrent_supersede_correct_has_one_winner(engine) -> None:
    results, old_ref = _race(engine, "supersede", "correct", "pg-race-sc")
    _assert_one_branch(engine, old_ref, results)
