from typing import Protocol

from daen_geocore.domain.references import (
    AccessPointRef,
    PlaceRef,
    SelectionRecordRef,
    SourceAssertionRef,
)
from daen_geocore.ports.persistence.records import (
    AssertionHistoryFactRef,
    PlaceHistoryFactRef,
    StateWitness,
)


class ReferenceCandidateGenerator(Protocol):
    def new_place_ref(self) -> PlaceRef: ...
    def new_source_assertion_ref(self) -> SourceAssertionRef: ...
    def new_selection_record_ref(self) -> SelectionRecordRef: ...
    def new_access_point_ref(self) -> AccessPointRef: ...
    def new_place_history_fact_ref(self) -> PlaceHistoryFactRef: ...
    def new_assertion_history_fact_ref(self) -> AssertionHistoryFactRef: ...


class StateWitnessGenerator(Protocol):
    def new_state_witness(self) -> StateWitness: ...
