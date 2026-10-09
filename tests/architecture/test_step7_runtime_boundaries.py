from ast import Import, ImportFrom, parse
from pathlib import Path

ROOT = Path(__file__).parents[2] / "src" / "daen_geocore"


def imports(path: Path) -> set[str]:
    result: set[str] = set()
    for node in parse(path.read_text()).body:
        if isinstance(node, Import):
            result.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ImportFrom) and node.module:
            result.add(node.module.split(".")[0])
    return result


def test_mutation_runtime_is_provider_neutral() -> None:
    runtime = ROOT / "application" / "mutation_runtime"
    for path in runtime.rglob("*.py"):
        assert not imports(path).intersection({"sqlalchemy", "psycopg", "fastapi"})


def test_idempotency_is_a_store_capability_not_a_repository() -> None:
    for path in (ROOT / "ports" / "idempotency").glob("*.py"):
        text = path.read_text()
        assert "Repository" not in text
        assert "CRUD" not in text
        assert "save(" not in text and "delete(" not in text


def test_no_public_v1_route_added() -> None:
    for path in (ROOT / "transport").rglob("*.py"):
        assert '"/v1' not in path.read_text() and "'/v1" not in path.read_text()


def test_step7_does_not_add_schema_or_migration() -> None:
    versions = list((Path(__file__).parents[2] / "alembic" / "versions").glob("*.py"))
    assert len(versions) == 1
    assert not any(path.name.startswith("0002") for path in versions)
