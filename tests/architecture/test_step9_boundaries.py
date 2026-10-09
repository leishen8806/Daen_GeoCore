from ast import Import, ImportFrom
from pathlib import Path

ROOT = Path(__file__).parents[2] / "src" / "daen_geocore"


def imports(path: Path) -> set[str]:
    result: set[str] = set()
    for node in __import__("ast").parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, Import):
            result.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ImportFrom) and node.module:
            result.add(node.module.split(".")[0])
    return result


def test_create_has_no_mutation_basis_or_infrastructure_dependency() -> None:
    source = (ROOT / "application" / "source_assertion_create.py").read_text(encoding="utf-8")
    assert "MutationBasisToken" not in source
    assert "MutationBasisClaims" not in source
    assert "MutationBasisValidator" not in source
    assert not imports(ROOT / "application" / "source_assertion_create.py").intersection(
        {"sqlalchemy", "psycopg", "fastapi"}
    )


def test_step9_has_no_http_or_new_migration() -> None:
    assert not any(
        '"/v1' in path.read_text(encoding="utf-8") for path in (ROOT / "transport").rglob("*.py")
    )
    versions = list((Path(__file__).parents[2] / "alembic" / "versions").glob("*.py"))
    assert {path.name for path in versions} == {
        "0001_authoritative_persistence.py",
        "0002_correctness_persistence.py",
    }


def test_create_has_no_selection_or_history_write() -> None:
    source = (ROOT / "application" / "source_assertion_create.py").read_text(encoding="utf-8")
    assert "insert_selection" not in source
    assert "append_assertion_history" not in source
