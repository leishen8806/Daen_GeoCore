import base64
import secrets

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
from daen_geocore.ports.references.generation import (
    ReferenceCandidateGenerator,
    StateWitnessGenerator,
)

REFERENCE_ENTROPY_BYTES = 16


def _token() -> str:
    return (
        base64.urlsafe_b64encode(secrets.token_bytes(REFERENCE_ENTROPY_BYTES))
        .rstrip(b"=")
        .decode("ascii")
    )


class SecureReferenceCandidateGenerator(ReferenceCandidateGenerator, StateWitnessGenerator):
    def new_place_ref(self) -> PlaceRef:
        return PlaceRef(_token())

    def new_source_assertion_ref(self) -> SourceAssertionRef:
        return SourceAssertionRef(_token())

    def new_selection_record_ref(self) -> SelectionRecordRef:
        return SelectionRecordRef(_token())

    def new_access_point_ref(self) -> AccessPointRef:
        return AccessPointRef(_token())

    def new_place_history_fact_ref(self) -> PlaceHistoryFactRef:
        return PlaceHistoryFactRef(_token())

    def new_assertion_history_fact_ref(self) -> AssertionHistoryFactRef:
        return AssertionHistoryFactRef(_token())

    def new_state_witness(self) -> StateWitness:
        return StateWitness(_token())
