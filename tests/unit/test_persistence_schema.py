from pathlib import Path

from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint

from daen_geocore.infrastructure.postgres.metadata import metadata

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


def test_step5_metadata_has_exact_table_set() -> None:
    assert set(metadata.tables) == EXPECTED_TABLES


def test_schema_has_no_generated_ids_or_server_time() -> None:
    for table in metadata.tables.values():
        for column in table.columns:
            assert column.server_default is None
            assert column.autoincrement is False or column.autoincrement == "auto"
            if column.name == "recorded_at":
                assert column.server_default is None


def test_schema_has_no_cascade_and_expected_primary_keys() -> None:
    for table in metadata.tables.values():
        for foreign_key in table.foreign_key_constraints:
            assert foreign_key.ondelete is None
        assert any(isinstance(constraint, PrimaryKeyConstraint) for constraint in table.constraints)
    assert {
        (fk.parent.name, fk.column.table.name, fk.column.name)
        for table_name in ("identity_place_history", "identity_place_head")
        for fk_constraint in metadata.tables[table_name].foreign_key_constraints
        for fk in fk_constraint.elements
    } >= {
        ("place_ref", "identity_place", "place_ref"),
    }


def test_cross_module_foreign_keys_are_not_frozen() -> None:
    cross_module_tables = {
        "assertions_source_assertion",
        "representation_selection_record",
        "representation_selection_support",
    }
    for table_name in cross_module_tables:
        for constraint in metadata.tables[table_name].constraints:
            if isinstance(constraint, ForeignKeyConstraint):
                assert all(
                    element.column.table.name.startswith(table_name.split("_")[0])
                    or table_name == "representation_selection_support"
                    for element in constraint.elements
                )


def test_migration_static_review_has_no_deferred_or_generated_storage() -> None:
    migration = Path("alembic/versions/0001_authoritative_persistence.py").read_text()
    for forbidden in ("CASCADE", "SERIAL(", "IDENTITY(", "gen_random_uuid", "now()"):
        assert forbidden not in migration.upper()
