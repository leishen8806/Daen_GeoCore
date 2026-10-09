import os
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from threading import Barrier
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, select

from daen_geocore.domain.references import PlaceRef, SelectionRecordRef, SourceAssertionRef
from daen_geocore.infrastructure.postgres.engine import create_postgres_engine
from daen_geocore.infrastructure.postgres.schema import identity_place
from daen_geocore.infrastructure.postgres.uow import PostgresUnitOfWork
from daen_geocore.ports.persistence.commit import CommitAccepted
from daen_geocore.ports.persistence.records import (
    AssertionStandingHead,
    ConditionalWriteDisposition,
    InsertDisposition,
    OpaqueEncodedPayload,
    PersistedExplicitScope,
    PersistedQualityKnown,
    PersistedTypedValue,
    PlaceHead,
    PlaceIdentityRecord,
    RecordAbsent,
    SelectionRecord,
    SelectionSlotHead,
    SelectionSlotKey,
    SourceAssertionRecord,
    StateWitness,
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


def test_all_module_repositories_round_trip_and_cas(engine) -> None:
    prefix = uuid4().hex
    now = datetime(2026, 10, 9, 12, 0, tzinfo=UTC)
    place = PlaceRef(f"step6-place-{prefix}")
    assertion = SourceAssertionRef(f"step6-assertion-{prefix}")
    selection = SelectionRecordRef(f"step6-selection-{prefix}")
    payload = OpaqueEncodedPayload("utf8", b"value")
    scope = PersistedExplicitScope("language", OpaqueEncodedPayload("utf8", b"km"), b"km")
    with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
        assert (
            uow.identity._connection is uow.assertions._connection is uow.representation._connection
        )
        assert (
            uow.identity.insert_place_if_absent(PlaceIdentityRecord(place, now)).value
            is InsertDisposition.INSERTED
        )
        assert (
            uow.identity.insert_place_if_absent(PlaceIdentityRecord(place, now)).value
            is InsertDisposition.ALREADY_PRESENT_SAME
        )
        head = PlaceHead(place, None, StateWitness("p1"))
        assert uow.identity.insert_place_head_if_absent(head).value is InsertDisposition.INSERTED
        assert (
            uow.identity.compare_and_swap_place_head(
                place, StateWitness("p1"), None, StateWitness("p2")
            ).value
            is ConditionalWriteDisposition.APPLIED
        )
        assert uow.identity.get_place(place).value.record.place_ref == place
        source = SourceAssertionRecord(
            assertion,
            place,
            "name",
            PersistedTypedValue("text", payload),
            scope,
            payload,
            PersistedQualityKnown(payload),
            now,
        )
        assert uow.assertions.insert_assertion_if_absent(source).value is InsertDisposition.INSERTED
        assert (
            uow.assertions.insert_assertion_if_absent(source).value
            is InsertDisposition.ALREADY_PRESENT_SAME
        )
        standing = AssertionStandingHead(assertion, None, StateWitness("a1"))
        assert (
            uow.assertions.insert_standing_head_if_absent(standing).value
            is InsertDisposition.INSERTED
        )
        assert (
            uow.assertions.compare_and_swap_standing_head(
                assertion, StateWitness("a1"), None, StateWitness("a2")
            ).value
            is ConditionalWriteDisposition.APPLIED
        )
        selected = SelectionRecord(
            selection,
            place,
            "name",
            PersistedTypedValue("text", payload),
            scope,
            payload,
            payload,
            PersistedQualityKnown(payload),
            now,
        )
        assert (
            uow.representation.insert_selection_record_if_absent(selected).value
            is InsertDisposition.INSERTED
        )
        assert (
            uow.representation.insert_support_link_if_absent(selection, assertion).value
            is InsertDisposition.INSERTED
        )
        slot = SelectionSlotKey(place, "name", "language", b"km")
        slot_head = SelectionSlotHead(slot, selection, StateWitness("s1"))
        assert (
            uow.representation.insert_selection_slot_head_if_absent(slot_head).value
            is InsertDisposition.INSERTED
        )
        assert (
            uow.representation.compare_and_swap_selection_slot_head(
                slot, selection, StateWitness("s1"), selection, StateWitness("s2")
            ).value
            is ConditionalWriteDisposition.APPLIED
        )
        assert isinstance(uow.commit(), CommitAccepted)
    with engine.connect() as connection:
        assert (
            connection.execute(
                select(identity_place.c.place_ref).where(identity_place.c.place_ref == place.token)
            ).scalar_one()
            == place.token
        )


def test_cross_module_rollback_leaves_no_rows(engine) -> None:
    prefix = uuid4().hex
    place = PlaceRef(f"step6-rollback-{prefix}")
    assertion = SourceAssertionRef(f"step6-rollback-assertion-{prefix}")
    selection = SelectionRecordRef(f"step6-rollback-selection-{prefix}")
    now = datetime(2026, 10, 9, 12, 0, tzinfo=UTC)
    payload = OpaqueEncodedPayload("utf8", b"value")
    scope = PersistedExplicitScope("language", payload, b"km")
    source = SourceAssertionRecord(
        assertion,
        place,
        "name",
        PersistedTypedValue("text", payload),
        scope,
        payload,
        PersistedQualityKnown(payload),
        now,
    )
    selected = SelectionRecord(
        selection,
        place,
        "name",
        PersistedTypedValue("text", payload),
        scope,
        payload,
        payload,
        PersistedQualityKnown(payload),
        now,
    )
    with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
        uow.identity.insert_place_if_absent(PlaceIdentityRecord(place, now))
        uow.assertions.insert_assertion_if_absent(source)
        uow.representation.insert_selection_record_if_absent(selected)
    with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
        assert isinstance(uow.identity.get_place(place).value, RecordAbsent)
        assert isinstance(uow.assertions.get_assertion(assertion).value, RecordAbsent)
        assert (
            uow.representation.get_selection_record(selection).value.__class__.__name__
            == "RecordAbsent"
        )
        uow.rollback()


def test_conditional_write_competes_on_one_witness(engine) -> None:
    prefix = uuid4().hex
    place = PlaceRef(f"step6-cas-{prefix}")
    now = datetime(2026, 10, 9, 12, 0, tzinfo=UTC)
    with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
        uow.identity.insert_place_if_absent(PlaceIdentityRecord(place, now))
        uow.identity.insert_place_head_if_absent(PlaceHead(place, None, StateWitness("start")))
        assert isinstance(uow.commit(), CommitAccepted)

    barrier = Barrier(2)

    def worker(witness: str):
        with PostgresUnitOfWork(create_postgres_engine(DATABASE_URL)) as uow:
            barrier.wait(timeout=10)
            result = uow.identity.compare_and_swap_place_head(
                place, StateWitness("start"), None, StateWitness(witness)
            )
            outcome = uow.commit()
            return result.value, outcome

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = list(executor.map(worker, ("winner-a", "winner-b")))
    dispositions = [result for result, _ in outcomes]
    assert dispositions.count(ConditionalWriteDisposition.APPLIED) == 1
    assert dispositions.count(ConditionalWriteDisposition.PRECONDITION_NOT_MET) == 1
