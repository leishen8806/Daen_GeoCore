from pathlib import Path

ROOT = Path(__file__).parents[2] / "src" / "daen_geocore"


def test_step8_has_no_reference_parser_or_production_evidence_adapter() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / "infrastructure").rglob("*.py")
    )
    for forbidden in (
        "parse_place_ref",
        "decode_reference",
        "extract_region_from_ref",
        "extract_timestamp_from_ref",
        "validate_ref_prefix",
        "PostgresEvidenceStore",
        "S3EvidenceStore",
        "boto3",
    ):
        assert forbidden not in source


def test_step8_migration_contains_only_correctness_tables() -> None:
    migration = (
        Path(__file__).parents[2] / "alembic" / "versions" / "0002_correctness_persistence.py"
    ).read_text(encoding="utf-8")
    for table in (
        "mutation_committed_binding",
        "mutation_committed_result_reference",
        "mutation_committed_replay_metadata",
        "mutation_audit",
    ):
        assert f'"{table}"' in migration
    for forbidden in ("SERIAL(", "sa.Identity", "gen_random_uuid", "now()", "CASCADE"):
        assert forbidden.lower() not in migration.lower()
    assert "EvidenceStore" not in migration
