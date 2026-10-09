from datetime import UTC, datetime

import pytest

from daen_geocore.domain.references import PlaceRef
from daen_geocore.ports.persistence.records import (
    OpaqueEncodedPayload,
    PersistedExplicitScope,
    PersistedQualityKnown,
    PersistedQualityUnknown,
    PersistedTypedValue,
    PersistedUnknownScope,
    PlaceIdentityRecord,
    RecordAbsent,
    RecordFound,
    StateWitness,
)


def test_material_records_preserve_opaque_values_and_status_types() -> None:
    instant = datetime(2026, 10, 9, tzinfo=UTC)
    payload = OpaqueEncodedPayload("json", b'{"x":1}')
    explicit = PersistedExplicitScope("scope", payload, b"key")
    assert explicit.encoded.payload == b'{"x":1}'
    assert PersistedQualityKnown(payload).encoded.encoding_id == "json"
    assert isinstance(PersistedQualityUnknown(), PersistedQualityUnknown)
    record = PlaceIdentityRecord(PlaceRef("P1"), instant)
    assert RecordFound(record).record == record
    assert isinstance(RecordAbsent(), RecordAbsent)
    assert StateWitness("w1").value == "w1"


def test_recorded_at_must_be_utc_aware() -> None:
    with pytest.raises(ValueError):
        PlaceIdentityRecord(PlaceRef("P1"), datetime(2026, 10, 9))


def test_typed_value_requires_opaque_payload() -> None:
    value = PersistedTypedValue("text", OpaqueEncodedPayload("utf8", b"abc"))
    assert value.encoded.payload == b"abc"
    assert isinstance(PersistedUnknownScope(), PersistedUnknownScope)
