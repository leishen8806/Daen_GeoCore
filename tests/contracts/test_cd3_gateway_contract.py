"""Structural contract checks for the CD-3 WP2 candidate."""

import json
from pathlib import Path

ROOT = Path(__file__).parents[2]
SPEC_PATH = ROOT / "docs/daen-geocore/02_PRODUCT/CD3_GATEWAY_OPENAPI.json"


def load_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8-sig"))


def walk(value):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def test_openapi_surface_and_status() -> None:
    spec = load_spec()
    assert spec["openapi"].startswith("3.1.")
    assert set(spec["paths"]) == {
        "/gateway/v1/geocode",
        "/gateway/v1/reverse-geocode",
        "/gateway/v1/status",
    }
    assert set(spec["paths"]["/gateway/v1/geocode"]) == {"post"}
    assert set(spec["paths"]["/gateway/v1/reverse-geocode"]) == {"post"}
    assert set(spec["paths"]["/gateway/v1/status"]) == {"get"}
    assert not any(path.startswith("/v1/") for path in spec["paths"])
    assert "NOT R2 ACCEPTED" in spec["info"]["description"]


def test_request_inputs_are_body_only_and_bounded() -> None:
    spec = load_spec()
    for path in ("/gateway/v1/geocode", "/gateway/v1/reverse-geocode"):
        operation = spec["paths"][path]["post"]
        assert "parameters" not in operation
        assert "requestBody" in operation
    purpose = spec["components"]["schemas"]["ConsumerPurposeCode"]
    assert purpose["minLength"] >= 1
    assert purpose["maxLength"] <= 64
    assert purpose["pattern"]
    location = spec["components"]["schemas"]["Location"]["properties"]
    assert location["latitude"]["minimum"] == -90
    assert location["latitude"]["maximum"] == 90
    assert location["longitude"]["minimum"] == -180
    assert location["longitude"]["maximum"] == 180


def test_identity_cache_and_mutation_fields_are_absent() -> None:
    spec = load_spec()
    keys = {key.lower() for value in walk(spec) if isinstance(value, dict) for key in value}
    for forbidden in (
        "idempotency-key",
        "mutationbasistoken",
        "cachehit",
        "cacheexpiresat",
        "contentexpiresat",
        "geoid",
        "placeref",
        "sourceassertionref",
        "createplace",
        "linkgeoid",
        "persist",
        "save",
        "store",
    ):
        assert forbidden not in keys


def test_success_and_error_envelopes_have_request_id() -> None:
    spec = load_spec()
    success = spec["components"]["schemas"]["LookupSuccess"]["required"]
    status = spec["components"]["schemas"]["StatusResponse"]["required"]
    error = spec["components"]["schemas"]["ErrorEnvelope"]["required"]
    assert "requestId" in success
    assert "requestId" in status
    assert "requestId" in error
    assert spec["components"]["schemas"]["LookupSuccess"]["properties"]["status"]["enum"] == [
        "OK",
        "ZERO_RESULTS",
    ]
    assert (
        spec["components"]["schemas"]["LookupSuccess"]["properties"]["results"]["type"] == "array"
    )


def test_error_responses_use_common_envelope_and_status_is_coarse() -> None:
    spec = load_spec()
    for path_item in spec["paths"].values():
        for operation in path_item.values():
            for response in operation["responses"].values():
                if "content" in response:
                    schema = response["content"]["application/json"]["schema"]
                    if schema.get("$ref", "").endswith("ErrorEnvelope"):
                        assert schema["$ref"] == "#/components/schemas/ErrorEnvelope"
    status_schema_keys = {
        key.lower()
        for value in walk(spec["components"]["schemas"]["StatusResponse"])
        if isinstance(value, dict)
        for key in value
    }
    for forbidden in ("apikey", "secret", "billing", "accountquota", "rawquota"):
        assert forbidden not in status_schema_keys
