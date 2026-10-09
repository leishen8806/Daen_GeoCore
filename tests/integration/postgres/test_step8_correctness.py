import os
from datetime import UTC, datetime
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, select

from daen_geocore.domain.references import PlaceRef, SelectionRecordRef, SourceAssertionRef
from daen_geocore.infrastructure.postgres.engine import create_postgres_engine
from daen_geocore.infrastructure.postgres.schema import (
    identity_place,
    mutation_audit,
    mutation_committed_binding,
)
from daen_geocore.infrastructure.postgres.uow import PostgresUnitOfWork
from daen_geocore.ports.audit.store import MutationAuditRecord
from daen_geocore.ports.idempotency.store import (
    CommittedBindingFound,
    CommittedMutationBinding,
    CommittedMutationResult,
    IdempotencyBindingKey,
    IdempotencyCreateDisposition,
)
from daen_geocore.ports.persistence.records import (
    InsertDisposition,
    OpaqueEncodedPayload,
    PlaceIdentityRecord,
)
from daen_geocore.ports.result import PortSuccess
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueReplayMetadata,
    OpaqueRequestIdentity,
    TechnicalOperationKey,
)

DATABASE_URL = os.getenv("DAEN_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="DAEN_TEST_DATABASE_URL is not configured")


def _config() -> Config:
    config = Config(str(Path("alembic.ini").resolve()))
    config.set_main_option("sqlalchemy.url", DATABASE_URL or "")
    return config


@pytest.fixture(scope="module")
def engine():
    assert DATABASE_URL is not None
    command.upgrade(_config(), "head")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    yield engine
    command.downgrade(_config(), "base")
    engine.dispose()


def _binding(suffix: str) -> CommittedMutationBinding:
    key = IdempotencyBindingKey(
        OpaqueClientIdentity(f"client-{suffix}"), OpaqueRequestIdentity(f"request-{suffix}")
    )
    return CommittedMutationBinding(
        key,
        IntentFingerprint("intent-1"),
        TechnicalOperationKey("operation-1"),
        CommittedMutationResult(
            (
                PlaceRef("place-replay"),
                SourceAssertionRef("assertion-1"),
                SelectionRecordRef("selection-1"),
            ),
            OpaqueReplayMetadata((("result", "ok"), ("version", "1"))),
        ),
    )


def _audit(binding: CommittedMutationBinding, detail: bytes = b"audit") -> MutationAuditRecord:
    payload = OpaqueEncodedPayload("test.v1", detail)
    return MutationAuditRecord(
        binding.key,
        binding.intent_fingerprint,
        binding.operation_key,
        datetime(2026, 10, 9, 12, 0, tzinfo=UTC),
        payload,
        payload,
    )


def test_step8_tables_and_downgrade_keep_step5(engine) -> None:
    names = set(inspect(engine).get_table_names())
    assert {
        "mutation_committed_binding",
        "mutation_committed_result_reference",
        "mutation_committed_replay_metadata",
        "mutation_audit",
    } <= names
    command.downgrade(_config(), "0001_authoritative_persistence")
    names = set(inspect(engine).get_table_names())
    assert "mutation_audit" not in names
    assert "identity_place" in names
    command.upgrade(_config(), "head")


def test_committed_binding_and_audit_share_uow_and_rollback(engine) -> None:
    binding = _binding("rollback")
    with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
        assert uow._connection is not None
        assert uow.identity._connection is uow._connection
        assert uow.assertions._connection is uow._connection
        assert uow.representation._connection is uow._connection
        assert uow.committed_idempotency._connection is uow._connection
        assert uow.mutation_audit._connection is uow._connection
        assert uow.identity.insert_place_if_absent(
            PlaceIdentityRecord(PlaceRef("place-rollback"), datetime(2026, 10, 9, tzinfo=UTC))
        ) == PortSuccess(InsertDisposition.INSERTED)
        assert uow.committed_idempotency.create_if_absent(binding) == PortSuccess(
            IdempotencyCreateDisposition.CREATED
        )
        assert uow.mutation_audit.append_if_absent(_audit(binding)) == PortSuccess(
            InsertDisposition.INSERTED
        )
    with engine.connect() as connection:
        assert (
            connection.execute(
                select(identity_place).where(identity_place.c.place_ref == "place-rollback")
            ).first()
            is None
        )
        assert (
            connection.execute(
                select(mutation_committed_binding).where(
                    mutation_committed_binding.c.client_identity == "client-rollback"
                )
            ).first()
            is None
        )
        assert (
            connection.execute(
                select(mutation_audit).where(mutation_audit.c.client_identity == "client-rollback")
            ).first()
            is None
        )


def test_committed_binding_replay_and_audit_conflict(engine) -> None:
    binding = _binding("commit")
    with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
        assert uow.committed_idempotency.create_if_absent(binding) == PortSuccess(
            IdempotencyCreateDisposition.CREATED
        )
        assert uow.mutation_audit.append_if_absent(_audit(binding)) == PortSuccess(
            InsertDisposition.INSERTED
        )
        uow.commit()
    with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
        found = uow.committed_idempotency.read(binding.key)
        assert isinstance(found, PortSuccess)
        assert isinstance(found.value, CommittedBindingFound)
        assert found.value.binding == binding
        assert uow.committed_idempotency.create_if_absent(binding) == PortSuccess(
            IdempotencyCreateDisposition.ALREADY_PRESENT_SAME
        )
        assert uow.mutation_audit.append_if_absent(_audit(binding, b"changed")) == PortSuccess(
            InsertDisposition.CONFLICTING_EXISTING
        )
        uow.rollback()
