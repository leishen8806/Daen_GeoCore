import os
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import pytest
from alembic import command as alembic_command
from alembic.config import Config
from sqlalchemy import create_engine, func, select

from daen_geocore.application.source_assertion_create import SourceAssertionCreateOutcome
from daen_geocore.domain.references import PlaceRef
from daen_geocore.infrastructure.postgres.mutation_factory import PostgresMutationUnitOfWorkFactory
from daen_geocore.infrastructure.postgres.schema import (
    assertions_history,
    assertions_source_assertion,
    assertions_standing_head,
    identity_place,
    mutation_audit,
    mutation_committed_binding,
    representation_selection_record,
)
from tests.unit.test_source_assertion_create import (
    FakeCandidates,
    FakeClock,
    FakeEvidence,
    FakeGate,
    command,
)

NOW = datetime(2026, 10, 9, 12, 0, tzinfo=UTC)
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


def test_source_assertion_create_happy_replay_and_distinct_request(engine) -> None:
    evidence = FakeEvidence()
    with engine.begin() as connection:
        connection.execute(
            identity_place.insert().values(
                place_ref="place-1", recorded_at=datetime(2026, 10, 9, tzinfo=UTC)
            )
        )
    operation = __import__(
        "daen_geocore.application.source_assertion_create", fromlist=["CreateSourceAssertion"]
    ).CreateSourceAssertion(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        evidence,
        FakeGate(),
        FakeCandidates(),
        FakeClock(),
    )
    first = operation.execute(command())
    assert first.value.outcome is SourceAssertionCreateOutcome.APPLIED
    first_ref = first.value.source_assertion_ref
    assert first_ref is not None
    writes = evidence.reservation_writes
    replay = operation.execute(command())
    assert replay.value.outcome is SourceAssertionCreateOutcome.REPLAY
    assert replay.value.source_assertion_ref == first_ref
    assert evidence.reservation_writes == writes
    second = operation.execute(command(request="request-2"))
    assert second.value.outcome is SourceAssertionCreateOutcome.APPLIED
    assert second.value.source_assertion_ref != first_ref
    with engine.connect() as connection:
        assert (
            connection.execute(
                select(func.count()).select_from(assertions_source_assertion)
            ).scalar_one()
            == 2
        )
        assert (
            connection.execute(
                select(func.count()).select_from(assertions_standing_head)
            ).scalar_one()
            == 2
        )
        assert (
            connection.execute(select(func.count()).select_from(assertions_history)).scalar_one()
            == 0
        )
        assert (
            connection.execute(select(func.count()).select_from(mutation_audit)).scalar_one() == 2
        )
        assert (
            connection.execute(
                select(func.count()).select_from(mutation_committed_binding)
            ).scalar_one()
            == 2
        )
        assert (
            connection.execute(
                select(func.count()).select_from(representation_selection_record)
            ).scalar_one()
            == 0
        )


def test_source_assertion_create_rolls_back_after_audit_conflict(engine) -> None:
    with engine.begin() as connection:
        connection.execute(
            identity_place.insert().values(place_ref="place-rollback", recorded_at=NOW)
        )
        connection.execute(
            mutation_audit.insert().values(
                client_identity="client",
                request_identity="request-rollback",
                intent_fingerprint="intent-1",
                operation_key="source_assertion.create",
                recorded_at=NOW,
                mutation_provenance_encoding="test.v1",
                mutation_provenance_payload=b"existing",
                audit_details_encoding="test.v1",
                audit_details_payload=b"existing",
            )
        )
    candidates = FakeCandidates()
    candidates.count = 10
    operation = __import__(
        "daen_geocore.application.source_assertion_create", fromlist=["CreateSourceAssertion"]
    ).CreateSourceAssertion(
        PostgresMutationUnitOfWorkFactory(DATABASE_URL),
        FakeEvidence(),
        FakeGate(),
        candidates,
        FakeClock(),
    )
    result = operation.execute(
        replace(command(request="request-rollback"), place_ref=PlaceRef("place-rollback"))
    )
    assert result.value.outcome is SourceAssertionCreateOutcome.AUDIT_CONFLICT
    with engine.connect() as connection:
        assert (
            connection.execute(
                select(func.count())
                .select_from(assertions_source_assertion)
                .where(assertions_source_assertion.c.place_ref == "place-rollback")
            ).scalar_one()
            == 0
        )
        assert (
            connection.execute(
                select(func.count()).select_from(assertions_standing_head)
            ).scalar_one()
            == 2
        )
        assert (
            connection.execute(
                select(func.count())
                .select_from(mutation_committed_binding)
                .where(mutation_committed_binding.c.request_identity == "request-rollback")
            ).scalar_one()
            == 0
        )
