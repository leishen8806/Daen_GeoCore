from ast import Import, ImportFrom, parse
from pathlib import Path

SOURCE_PATH = Path("src/daen_geocore/application/source_assertion_withdrawal.py")
SOURCE = SOURCE_PATH.read_text(encoding="utf-8")


def _imports() -> set[str]:
    result: set[str] = set()
    for node in parse(SOURCE).body:
        if isinstance(node, Import):
            result.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ImportFrom) and node.module:
            result.add(node.module.split(".")[0])
    return result


def test_withdraw_is_transport_neutral_and_has_no_basis_or_evidence() -> None:
    assert "class WithdrawSourceAssertionCommand" in SOURCE
    assert "source_assertion.withdraw" in SOURCE
    assert "MutationBasisToken" not in SOURCE
    assert "MutationBasisClaims" not in SOURCE
    assert "EvidenceStore" not in SOURCE
    assert "EvidenceLookupKey" not in SOURCE
    assert "ReferenceReservationCoordinator" not in SOURCE
    assert "/v1" not in SOURCE
    assert not _imports().intersection({"sqlalchemy", "psycopg", "fastapi"})


def test_withdraw_has_no_selection_or_place_mutation() -> None:
    assert "SelectionRecord" not in SOURCE
    assert "insert_selection" not in SOURCE
    assert "PlaceOwner" not in SOURCE
    assert "identity.get_place_head" not in SOURCE


def test_step11_has_no_schema_or_generic_mutation_framework() -> None:
    revisions = sorted(path.name for path in Path("alembic/versions").glob("*.py"))
    assert revisions == ["0001_authoritative_persistence.py", "0002_correctness_persistence.py"]
    assert "MutationExecutor" not in SOURCE
    assert "CommandBus" not in SOURCE
    assert "GenericRepository" not in SOURCE
