import ast
from pathlib import Path

MODULE = Path(__file__).parents[2] / "src/daen_geocore/ports/geocoding/geocoding.py"


def test_geocoding_port_has_no_forbidden_dependencies_or_concepts() -> None:
    source = MODULE.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    imports = {
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imports.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    )
    assert imports <= {"dataclasses", "enum", "math", "typing", "daen_geocore"}
    forbidden = (
        "fastapi",
        "pydantic",
        "sqlalchemy",
        "psycopg",
        "httpx",
        "opentelemetry",
        "infrastructure",
        "transport",
        "application",
        "google",
        "cloud",
        "placeref",
        "sourceassertionref",
        "selectionrecordref",
        "accesspointref",
        "geoid",
        "evidencestore",
        "mutationbasistoken",
        "cache",
        "/v1",
        "gateway/v1",
    )
    lowered = source.lower()
    assert not any(term in lowered for term in forbidden)


def test_geocoding_provider_exposes_exactly_two_operations() -> None:
    source = MODULE.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    protocol = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "GeocodingProvider"
    )
    methods = [node.name for node in protocol.body if isinstance(node, ast.FunctionDef)]
    assert methods == ["geocode", "reverse_geocode"]
