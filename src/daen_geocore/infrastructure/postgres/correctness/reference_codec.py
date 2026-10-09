from daen_geocore.domain.references import (
    AccessPointRef,
    PlaceRef,
    SelectionRecordRef,
    SourceAssertionRef,
)
from daen_geocore.ports.evidence.store import StableReference


def reference_kind(value: StableReference) -> tuple[str, str]:
    if isinstance(value, PlaceRef):
        return "place", value.token
    if isinstance(value, SourceAssertionRef):
        return "source_assertion", value.token
    if isinstance(value, SelectionRecordRef):
        return "selection_record", value.token
    return "access_point", value.token


def reference_from_row(kind: str, token: str) -> StableReference:
    constructors = {
        "place": PlaceRef,
        "source_assertion": SourceAssertionRef,
        "selection_record": SelectionRecordRef,
        "access_point": AccessPointRef,
    }
    constructor = constructors.get(kind)
    if constructor is None:
        raise ValueError("unknown reference kind")
    return constructor(token)
