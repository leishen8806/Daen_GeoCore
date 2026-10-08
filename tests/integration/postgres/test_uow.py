import os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import uuid4

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
from daen_geocore.ports.failures import TechnicalFailureClass
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
    prefix = uuid4().hex
    key_a = f"{prefix}-a"
    key_b = f"{prefix}-b"
    with engine.begin() as connection:
        connection.execute(
            table.insert(),
            [{"key": key_a, "value": 1}, {"key": key_b, "value": 1}],
        )
    barrier = Barrier(2)

    def worker(key: str) -> object:
        with PostgresUnitOfWork(
            create_postgres_engine(DATABASE_URL, TransactionProfile.MUTATION)
        ) as uow:
            assert uow._connection is not None
            rows = uow._connection.execute(
                select(table.c.key, table.c.value).where(table.c.key.in_([key_a, key_b]))
            ).all()
            assert len(rows) == 2
            uow._connection.execute(update(table).where(table.c.key == key).values(value=2))
            barrier.wait(timeout=10)
            return uow.commit()

    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            outcomes = list(executor.map(worker, (key_a, key_b)))
        accepted = [outcome for outcome in outcomes if isinstance(outcome, CommitAccepted)]
        aborted = [outcome for outcome in outcomes if isinstance(outcome, CommitNotCommitted)]
        assert len(accepted) == 1
        assert len(aborted) == 1
        assert aborted[0].failure is not None
        assert (
            aborted[0].failure.classification is TechnicalFailureClass.RETRYABLE_TRANSACTION_ABORT
        )
        with engine.connect() as connection:
            values = (
                connection.execute(select(table.c.value).where(table.c.key.in_([key_a, key_b])))
                .scalars()
                .all()
            )
        assert sorted(values) == [1, 2]
    finally:
        with engine.begin() as connection:
            connection.execute(delete(table).where(table.c.key.in_([key_a, key_b])))
