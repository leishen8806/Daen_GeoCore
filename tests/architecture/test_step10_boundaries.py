from pathlib import Path

SOURCE = Path("src/daen_geocore/application/source_assertion_transition.py").read_text()


def test_step10_application_boundary_and_distinct_operations() -> None:
    assert "class SupersedeSourceAssertion" in SOURCE
    assert "class CorrectSourceAssertion" in SOURCE
    assert "source_assertion.supersede" in SOURCE
    assert "source_assertion.correct" in SOURCE
    assert "sqlalchemy" not in SOURCE
    assert "psycopg" not in SOURCE
    assert "fastapi" not in SOURCE
    assert "/v1" not in SOURCE
    assert "CorrectionRecordRef" not in SOURCE
    assert "SelectionRecord" not in SOURCE


def test_step10_does_not_add_schema_or_generic_mutation_framework() -> None:
    revisions = sorted(path.name for path in Path("alembic/versions").glob("*.py"))
    assert revisions == ["0001_authoritative_persistence.py", "0002_correctness_persistence.py"]
    assert "MutationExecutor" not in SOURCE
    assert "CommandBus" not in SOURCE
    assert "GenericAssertionMutation" not in SOURCE
