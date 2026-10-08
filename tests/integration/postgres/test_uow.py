import os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    delete,
    select,
    text,
    update,
)

from daen_geocore.infrastructure.postgres.engine import TransactionProfile, create_postgres_engine
from daen_geocore.infrastructure.postgres.uow import PostgresUnitOfWork
from daen_geocore.ports.persistence.commit import CommitAccepted, CommitNotCommitted

DATABASE_URL = os.getenv("DAEN_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(
    not DATABASE_URL,
    reason="DAEN_TEST_DATABASE_URL is not configured",
)


@pytest.fixture(scope="module")
def probe():
    assert DATABASE_URL is not None
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    metadata = MetaData()
    table = Table(
        "uow_probe",
        metadata,
        Column("key", String(80), primary_key=True),
        Column("value", Integer, nullable=False),
    )
    metadata.create_all(engine)
    yield engine, table
    metadata.drop_all(engine)
    engine.dispose()


def test_commit_is_visible_to_separate_connection(probe) -> None:
    engine, table = probe
    with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
        assert uow._connection is not None
        uow._connection.execute(table.insert().values(key="commit", value=1))
        outcome = uow.commit()
    assert isinstance(outcome, CommitAccepted)
    with engine.connect() as connection:
        assert (
            connection.execute(select(table.c.value).where(table.c.key == "commit")).scalar_one()
            == 1
        )


def test_exit_without_commit_and_exception_roll_back(probe) -> None:
    engine, table = probe
    with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
        assert uow._connection is not None
        uow._connection.execute(table.insert().values(key="rollback", value=1))
    with pytest.raises(RuntimeError):
        with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
            assert uow._connection is not None
            uow._connection.execute(table.insert().values(key="exception", value=1))
            raise RuntimeError("abort")
    with engine.connect() as connection:
        assert (
            connection.execute(
                select(table.c.key).where(table.c.key.in_(["rollback", "exception"]))
            ).all()
            == []
        )


def test_uow_reuse_is_rejected(probe) -> None:
    engine, _ = probe
    uow = PostgresUnitOfWork(create_postgres_engine(DATABASE_URL))
    with uow:
        uow.rollback()
    with pytest.raises(RuntimeError):
        uow.commit()
    with pytest.raises(RuntimeError):
        uow.begin()


def test_transaction_profiles_are_real_postgres_isolation(probe) -> None:
    engine, _ = probe
    for profile, expected in (
        (TransactionProfile.READ, "read committed"),
        (TransactionProfile.MUTATION, "serializable"),
    ):
        with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL, profile)) as uow:
            assert uow._connection is not None
            assert (
                uow._connection.execute(text("SHOW transaction_isolation")).scalar_one() == expected
            )
            uow.commit()


def test_serializable_conflict_maps_to_retryable_not_committed(probe) -> None:
    engine, table = probe
    with engine.begin() as connection:
        connection.execute(delete(table).where(table.c.key == "conflict"))
        connection.execute(table.insert().values(key="conflict", value=0))
    barrier = Barrier(2)

    def worker() -> object:
        with PostgresUnitOfWork(
            create_postgres_engine(DATABASE_URL, TransactionProfile.MUTATION)
        ) as uow:
            assert uow._connection is not None
            row = uow._connection.execute(
                select(table.c.value).where(table.c.key == "conflict")
            ).scalar_one()
            uow._connection.execute(
                update(table).where(table.c.key == "conflict").values(value=row + 1)
            )
            barrier.wait(timeout=10)
            return uow.commit()

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = list(executor.map(lambda _: worker(), (1, 2)))
    assert any(isinstance(outcome, CommitNotCommitted) for outcome in outcomes)
