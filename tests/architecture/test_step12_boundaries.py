from pathlib import Path

ROOT = Path(__file__).parents[2]
SOURCE = (ROOT / "src/daen_geocore/application/selection_mutations.py").read_text()


def test_selection_mutations_are_transport_neutral_and_non_generic() -> None:
    assert 'TechnicalOperationKey("selection.add")' in SOURCE
    assert 'TechnicalOperationKey("selection.replace")' in SOURCE
    assert "FastAPI" not in SOURCE
    assert "SQLAlchemy" not in SOURCE
    assert "psycopg" not in SOURCE
    assert "MutationExecutor" not in SOURCE
    assert "GenericRepository" not in SOURCE
    assert "EvidenceStore" in SOURCE


def test_selection_mutations_preserve_lifecycle_boundaries() -> None:
    assert "WITHDRAWN_FACT_TYPE" in SOURCE
    assert "source_assertion.withdrawn" in SOURCE
    assert "insert_support_link_if_absent" in SOURCE
    assert "insert_selection_slot_head_if_absent" in SOURCE
    assert "compare_and_swap_selection_slot_head" in SOURCE
