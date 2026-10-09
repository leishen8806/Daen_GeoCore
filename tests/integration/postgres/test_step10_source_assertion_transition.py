# pyright: basic, reportArgumentType=false, reportAttributeAccessIssue=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportUnknownVariableType=false, reportMissingParameterType=false, reportReturnType=false, reportUnusedImport=false

import os
from datetime import UTC, datetime
from pathlib import Path

import pytest
from alembic import command as alembic_command
from alembic.config import Config
from sqlalchemy import create_engine, select

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
    candidates.calls = 10 if kind == "correct" else 0
    operation = (SupersedeSourceAssertion if kind == "supersede" else CorrectSourceAssertion)(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        FakeEvidence(),
        Gate(),
        codec,
        candidates,
        FakeTransitionClock(),
    )
    return operation.execute(command), old_ref


def test_postgres_supersede_happy_path(engine) -> None:
    result, old_ref = _run(engine, "supersede", "pg-supersede")
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
    result, old_ref = _run(engine, "correct", "pg-correct")
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
