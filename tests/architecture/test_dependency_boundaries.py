from ast import Import, ImportFrom, parse
from pathlib import Path

ROOT = Path(__file__).parents[2] / "src" / "daen_geocore"

FORBIDDEN = {
    "domain": {
        "fastapi",
        "pydantic",
        "sqlalchemy",
        "psycopg",
        "opentelemetry",
        "application",
        "transport",
        "infrastructure",
    },
    "application": {"transport", "infrastructure", "fastapi", "sqlalchemy", "psycopg"},
    "ports": {"infrastructure"},
}


def imports_for(path: Path) -> set[str]:
    tree = parse(path.read_text(encoding="utf-8"))
    result: set[str] = set()
    for node in tree.body:
        if isinstance(node, Import):
            result.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ImportFrom) and node.module:
            result.add(node.module.split(".")[0])
    return result


def test_dependency_boundaries() -> None:
    for layer, forbidden in FORBIDDEN.items():
        base = ROOT / layer
        for path in base.rglob("*.py"):
            imported = imports_for(path)
            assert not imported.intersection(forbidden), (
                f"{path}: {imported.intersection(forbidden)}"
            )

    for path in (ROOT / "transport").rglob("*.py"):
        assert "infrastructure" not in imports_for(path)


def test_postgres_infrastructure_uses_core_not_orm() -> None:
    for path in (ROOT / "infrastructure" / "postgres").rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "sqlalchemy.orm" not in source
        assert "DeclarativeBase" not in source
        assert "Session" not in source
