from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import TypeVar

from daen_geocore.domain.references import PlaceRef, SelectionRecordRef, SourceAssertionRef

RecordT = TypeVar("RecordT")


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError("recorded_at must be UTC-aware")
    return value


@dataclass(frozen=True, slots=True)
class OpaqueEncodedPayload:
    encoding_id: str
    payload: bytes

    def __post_init__(self) -> None:
        if type(self.encoding_id) is not str or type(self.payload) is not bytes:
            raise TypeError("opaque encoded payload requires string encoding and bytes payload")


@dataclass(frozen=True, slots=True)
class PersistedTypedValue:
    type_id: str
    encoded: OpaqueEncodedPayload


@dataclass(frozen=True, slots=True)
class PersistedUnknownScope:
    pass


@dataclass(frozen=True, slots=True)
class PersistedExplicitScope:
    type_id: str
    encoded: OpaqueEncodedPayload
    equality_key: bytes | None = None


type PersistedScope = PersistedUnknownScope | PersistedExplicitScope


@dataclass(frozen=True, slots=True)
class PersistedQualityUnknown:
    pass


@dataclass(frozen=True, slots=True)
class PersistedQualityKnown:
    encoded: OpaqueEncodedPayload


type PersistedQuality = PersistedQualityUnknown | PersistedQualityKnown


@dataclass(frozen=True, slots=True)
class PlaceHistoryFactRef:
    value: str


@dataclass(frozen=True, slots=True)
class AssertionHistoryFactRef:
    value: str


@dataclass(frozen=True, slots=True)
class StateWitness:
    value: str


class InsertDisposition(StrEnum):
    INSERTED = "inserted"
    ALREADY_PRESENT_SAME = "already_present_same"
    CONFLICTING_EXISTING = "conflicting_existing"


class ConditionalWriteDisposition(StrEnum):
    APPLIED = "applied"
    PRECONDITION_NOT_MET = "precondition_not_met"


@dataclass(frozen=True, slots=True)
class RecordFound[RecordT]:
    record: RecordT


@dataclass(frozen=True, slots=True)
class RecordAbsent:
    pass


@dataclass(frozen=True, slots=True)
class PlaceIdentityRecord:
    place_ref: PlaceRef
    recorded_at: datetime

    def __post_init__(self) -> None:
        _utc(self.recorded_at)


@dataclass(frozen=True, slots=True)
class PlaceHistoryFact:
    history_fact_ref: PlaceHistoryFactRef
    place_ref: PlaceRef
    fact_type: str
    recorded_at: datetime
    metadata: OpaqueEncodedPayload | None = None

    def __post_init__(self) -> None:
        _utc(self.recorded_at)


@dataclass(frozen=True, slots=True)
class PlaceHead:
    place_ref: PlaceRef
    latest_history_fact_ref: PlaceHistoryFactRef | None
    state_witness: StateWitness


@dataclass(frozen=True, slots=True)
class SourceAssertionRecord:
    source_assertion_ref: SourceAssertionRef
    place_ref: PlaceRef
    fact_purpose: str
    value: PersistedTypedValue
    scope: PersistedScope
    provenance: OpaqueEncodedPayload
    quality: PersistedQuality
    recorded_at: datetime

    def __post_init__(self) -> None:
        _utc(self.recorded_at)


@dataclass(frozen=True, slots=True)
class AssertionHistoryFact:
    history_fact_ref: AssertionHistoryFactRef
    source_assertion_ref: SourceAssertionRef
    fact_type: str
    recorded_at: datetime
    related_source_assertion_ref: SourceAssertionRef | None = None
    metadata: OpaqueEncodedPayload | None = None

    def __post_init__(self) -> None:
        _utc(self.recorded_at)


@dataclass(frozen=True, slots=True)
class AssertionStandingHead:
    source_assertion_ref: SourceAssertionRef
    latest_history_fact_ref: AssertionHistoryFactRef | None
    state_witness: StateWitness


@dataclass(frozen=True, slots=True)
class SelectionRecord:
    selection_record_ref: SelectionRecordRef
    place_ref: PlaceRef
    fact_purpose: str
    value: PersistedTypedValue
    scope: PersistedScope
    attribution: OpaqueEncodedPayload
    provenance: OpaqueEncodedPayload
    quality: PersistedQuality
    recorded_at: datetime

    def __post_init__(self) -> None:
        _utc(self.recorded_at)


@dataclass(frozen=True, slots=True)
class SelectionSlotKey:
    place_ref: PlaceRef
    fact_purpose: str
    scope_type_id: str
    equality_key: bytes


@dataclass(frozen=True, slots=True)
class SelectionSlotHead:
    slot: SelectionSlotKey
    selection_record_ref: SelectionRecordRef
    state_witness: StateWitness


type SupportLink = tuple[SelectionRecordRef, SourceAssertionRef]
