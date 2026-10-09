import os
from datetime import UTC, datetime
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.exc import IntegrityError

from daen_geocore.infrastructure.postgres.schema import (
    assertions_history,
    assertions_source_assertion,
    identity_place,
    identity_place_head,
    representation_selection_record,
    representation_selection_slot_head,
    representation_selection_support,
)

DATABASE_URL = os.getenv("DAEN_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(
    not DATABASE_URL,
    reason="DAEN_TEST_DATABASE_URL is not configured",
)

EXPECTED_TABLES = {
    "identity_place",
    "identity_place_history",
    "identity_place_head",
    "assertions_source_assertion",
    "assertions_history",
    "assertions_standing_head",
    "representation_selection_record",
    "representation_selection_support",
    "representation_selection_slot_head",
}


def _alembic_config() -> Config:
    config = Config(str(Path("alembic.ini").resolve()))
    config.set_main_option("sqlalchemy.url", DATABASE_URL or "")
    return config


def _fixture(prefix: str) -> dict[str, str]:
    return {
        "place": f"place-{prefix}",
        "assertion": f"assert-{prefix}",
        "selection": f"selection-{prefix}",
        "history": f"history-{prefix}",
    }


@pytest.fixture(scope="module")
def engine():
    assert DATABASE_URL is not None
    config = _alembic_config()
    command.upgrade(config, "head")
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    yield engine
    command.downgrade(config, "base")
    engine.dispose()


def test_migration_schema_and_repeatable_downgrade(engine) -> None:
    names = set(inspect(engine).get_table_names())
    assert names == EXPECTED_TABLES | {"alembic_version"}
    config = _alembic_config()
    command.downgrade(config, "base")
    assert set(inspect(engine).get_table_names()) == {"alembic_version"}
    command.upgrade(config, "head")
    assert set(inspect(engine).get_table_names()) == EXPECTED_TABLES | {"alembic_version"}


def test_opaque_round_trip_and_history_append(engine) -> None:
    refs = _fixture("roundtrip")
    recorded_at = datetime(2026, 10, 9, 12, 0, tzinfo=UTC)
    with engine.begin() as connection:
        connection.execute(
            identity_place.insert().values(place_ref=refs["place"], recorded_at=recorded_at)
        )
        connection.execute(
            identity_place_head.insert().values(place_ref=refs["place"], state_witness="witness-1")
        )
        connection.execute(
            assertions_source_assertion.insert().values(
                source_assertion_ref=refs["assertion"],
                place_ref=refs["place"],
                fact_purpose="unknown-purpose",
                value_type_id="future.type",
                value_encoding="future.v1",
                value_payload=b"opaque-value",
                scope_is_explicit=False,
                provenance_encoding="prov.v1",
                provenance_payload=b"opaque-provenance",
                quality_is_known=False,
                recorded_at=recorded_at,
            )
        )
        connection.execute(
            assertions_history.insert().values(
                history_fact_ref=refs["history"],
                source_assertion_ref=refs["assertion"],
                fact_type="open-history-fact",
                recorded_at=recorded_at,
            )
        )
        connection.execute(
            representation_selection_record.insert().values(
                selection_record_ref=refs["selection"],
                place_ref=refs["place"],
                fact_purpose="name",
                value_type_id="future.name",
                value_encoding="future.bytes.v1",
                value_payload=b"name-bytes",
                scope_is_explicit=True,
                scope_type_id="language",
                scope_encoding="scope.v1",
                scope_payload=b"km",
                scope_equality_key=b"km-key",
                selection_attribution_encoding="selection.v1",
                selection_attribution_payload=b"attribution",
                provenance_encoding="prov.v1",
                provenance_payload=b"selection-prov",
                quality_is_known=True,
                quality_encoding="quality.v1",
                quality_payload=b"quality",
                recorded_at=recorded_at,
            )
        )
        connection.execute(
            representation_selection_support.insert().values(
                selection_record_ref=refs["selection"],
                source_assertion_ref=refs["assertion"],
            )
        )
        selected = connection.execute(
            select(
                assertions_source_assertion.c.value_payload,
                assertions_source_assertion.c.scope_is_explicit,
                assertions_source_assertion.c.provenance_payload,
                assertions_source_assertion.c.quality_is_known,
                assertions_source_assertion.c.recorded_at,
            ).where(assertions_source_assertion.c.source_assertion_ref == refs["assertion"])
        ).one()
    assert selected.value_payload == b"opaque-value"
    assert selected.scope_is_explicit is False
    assert selected.provenance_payload == b"opaque-provenance"
    assert selected.quality_is_known is False
    assert selected.recorded_at.tzinfo is not None


def test_slot_exact_uniqueness_and_different_key_coexist(engine) -> None:
    refs = _fixture("slot")
    with engine.begin() as connection:
        connection.execute(
            identity_place.insert().values(place_ref=refs["place"], recorded_at=datetime.now(UTC))
        )
        for suffix, key in (("one", b"key-1"), ("two", b"key-2")):
            connection.execute(
                representation_selection_record.insert().values(
                    selection_record_ref=f"{refs['selection']}-{suffix}",
                    place_ref=refs["place"],
                    fact_purpose="address",
                    value_type_id="text",
                    value_encoding="utf8",
                    value_payload=suffix.encode(),
                    scope_is_explicit=True,
                    scope_type_id="default",
                    scope_encoding="scope.v1",
                    scope_payload=b"default",
                    scope_equality_key=key,
                    selection_attribution_encoding="selection.v1",
                    selection_attribution_payload=b"attr",
                    provenance_encoding="prov.v1",
                    provenance_payload=b"prov",
                    quality_is_known=False,
                    recorded_at=datetime.now(UTC),
                )
            )
            connection.execute(
                representation_selection_slot_head.insert().values(
                    place_ref=refs["place"],
                    fact_purpose="address",
                    scope_type_id="default",
                    scope_equality_key=key,
                    selection_record_ref=f"{refs['selection']}-{suffix}",
                    state_witness=f"witness-{suffix}",
                )
            )
        with pytest.raises(IntegrityError):
            connection.execute(
                representation_selection_slot_head.insert().values(
                    place_ref=refs["place"],
                    fact_purpose="address",
                    scope_type_id="default",
                    scope_equality_key=b"key-1",
                    selection_record_ref=f"{refs['selection']}-one",
                    state_witness="duplicate",
                )
            )


def test_history_facts_append_without_overwrite(engine) -> None:
    refs = _fixture("history")
    with engine.begin() as connection:
        connection.execute(
            identity_place.insert().values(place_ref=refs["place"], recorded_at=datetime.now(UTC))
        )
        connection.execute(
            assertions_source_assertion.insert().values(
                source_assertion_ref=refs["assertion"],
                place_ref=refs["place"],
                fact_purpose="address",
                value_type_id="text",
                value_encoding="utf8",
                value_payload=b"address",
                scope_is_explicit=False,
                provenance_encoding="prov.v1",
                provenance_payload=b"prov",
                quality_is_known=False,
                recorded_at=datetime.now(UTC),
            )
        )
        for suffix in ("one", "two"):
            connection.execute(
                assertions_history.insert().values(
                    history_fact_ref=f"{refs['history']}-{suffix}",
                    source_assertion_ref=refs["assertion"],
                    fact_type=f"open-{suffix}",
                    recorded_at=datetime.now(UTC),
                )
            )
        assert (
            connection.execute(
                select(assertions_history.c.history_fact_ref).where(
                    assertions_history.c.source_assertion_ref == refs["assertion"]
                )
            )
            .all()
            .__len__()
            == 2
        )
