import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

from daen_geocore.application.mutation_runtime import (
    AuthoritativeReadSetCapture,
    ReadSetRevalidator,
)
from daen_geocore.domain.references import PlaceRef
from daen_geocore.infrastructure.postgres.engine import create_postgres_engine
from daen_geocore.infrastructure.postgres.uow import PostgresUnitOfWork
from daen_geocore.ports.mutation import OwnerStateReader, PlaceOwner, ReadSetValidation
from daen_geocore.ports.persistence.commit import CommitAccepted
from daen_geocore.ports.persistence.records import PlaceHead, PlaceIdentityRecord, StateWitness

DATABASE_URL = os.getenv("DAEN_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="DAEN_TEST_DATABASE_URL is not configured")


def _config() -> Config:
    config = Config(str(Path("alembic.ini").resolve()))
    config.set_main_option("sqlalchemy.url", DATABASE_URL or "")
    return config


@pytest.fixture(scope="module")
def database():
    assert DATABASE_URL is not None
    command.upgrade(_config(), "head")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    yield engine
    command.downgrade(_config(), "base")
    engine.dispose()


def test_readset_revalidation_uses_active_uow(database) -> None:
    place = PlaceRef(f"step7-readset-{uuid4().hex}")
    now = datetime(2026, 10, 9, 12, 0, tzinfo=UTC)
    with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
        uow.identity.insert_place_if_absent(PlaceIdentityRecord(place, now))
        uow.identity.insert_place_head_if_absent(PlaceHead(place, None, StateWitness("w1")))
        assert isinstance(uow.commit(), CommitAccepted)
    with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
        reader = OwnerStateReader()
        owner = PlaceOwner(place)
        read_set = AuthoritativeReadSetCapture(reader).capture((owner,), uow).value
        assert (
            uow.identity.compare_and_swap_place_head(
                place, StateWitness("w1"), None, StateWitness("w2")
            ).value.value
            == "applied"
        )
        assert (
            ReadSetRevalidator(reader).revalidate(read_set, uow).value
            is ReadSetValidation.OWNER_STATE_MISMATCH
        )
        uow.rollback()
