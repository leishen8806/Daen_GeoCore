from ast import ClassDef, FunctionDef, parse
from pathlib import Path

ROOT = Path(__file__).parents[2] / "src" / "daen_geocore"
REPO_DIR = ROOT / "infrastructure" / "postgres" / "repositories"
FORBIDDEN_TYPES = {
    "GenericRepository",
    "CRUDRepository",
    "Repository",
    "BaseRepository",
    "AbstractRepository",
    "EntityRepository",
}
FORBIDDEN_METHODS = {
    "save",
    "update",
    "delete",
    "find_all",
    "list_all",
    "store",
    "persist",
    "remove",
    "upsert",
}


def test_only_module_owned_repositories_exist() -> None:
    classes = []
    for path in REPO_DIR.glob("*.py"):
        for node in parse(path.read_text()).body:
            if isinstance(node, ClassDef) and node.name.startswith("Postgres"):
                classes.append(node.name)
    assert sorted(classes) == [
        "PostgresAssertionsRepository",
        "PostgresIdentityRepository",
        "PostgresRepresentationRepository",
    ]


def test_no_generic_crud_public_surface() -> None:
    for path in [ROOT / "ports" / "persistence" / "repositories.py", *REPO_DIR.glob("*.py")]:
        for node in parse(path.read_text()).body:
            if isinstance(node, ClassDef):
                assert node.name not in FORBIDDEN_TYPES
                for method in node.body:
                    if isinstance(method, (FunctionDef,)):
                        assert method.name not in FORBIDDEN_METHODS


def test_no_production_delete_and_single_migration() -> None:
    assert all("delete(" not in p.read_text() for p in REPO_DIR.glob("*.py"))
    migrations = list((Path(__file__).parents[2] / "alembic" / "versions").glob("*.py"))
    assert {p.name for p in migrations} == {
        "0001_authoritative_persistence.py",
        "0002_correctness_persistence.py",
    }


def test_owner_table_boundaries() -> None:
    expected = {
        "identity.py": ("identity_place", "identity_place_history", "identity_place_head"),
        "assertions.py": (
            "assertions_source_assertion",
            "assertions_history",
            "assertions_standing_head",
        ),
        "representation.py": (
            "representation_selection_record",
            "representation_selection_support",
            "representation_selection_slot_head",
        ),
    }
    for name, tables in expected.items():
        source = (REPO_DIR / name).read_text()
        for table in tables:
            assert table in source
        foreign = {t for group in expected.values() for t in group if t not in tables}
        assert not any(t in source for t in foreign)
