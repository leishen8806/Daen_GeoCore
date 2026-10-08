from dataclasses import dataclass
from typing import Protocol

from daen_geocore.domain.references import (
    AccessPointRef,
    PlaceRef,
    SelectionRecordRef,
    SourceAssertionRef,
)
from daen_geocore.ports.result import PortResult
from daen_geocore.ports.technical import (
    EvidenceLookupKey,
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueReplayMetadata,
    OpaqueRequestIdentity,
    TechnicalOperationKey,
)

type StableReference = PlaceRef | SourceAssertionRef | SelectionRecordRef | AccessPointRef


@dataclass(frozen=True, slots=True)
class ReferenceReservationEvidence:
    """Permanent non-reuse evidence; not a request mapping or commit proof."""

    references: tuple[StableReference, ...]
    correlation: str | None = None


@dataclass(frozen=True, slots=True)
class RequestReferenceRecoveryMapping:
    """Typed request-to-reference recovery evidence, not Domain truth."""

    client_identity: OpaqueClientIdentity
    request_identity: OpaqueRequestIdentity
    intent_fingerprint: IntentFingerprint
    operation_key: TechnicalOperationKey
    references: tuple[StableReference, ...]
    replay_metadata: OpaqueReplayMetadata = OpaqueReplayMetadata()


@dataclass(frozen=True, slots=True)
class EvidenceCreated:
    pass


@dataclass(frozen=True, slots=True)
class EvidenceAlreadyPresentSame:
    pass


@dataclass(frozen=True, slots=True)
class EvidenceAlreadyPresentConflict:
    pass


@dataclass(frozen=True, slots=True)
class EvidenceFound[EvidenceT]:
    record: EvidenceT


@dataclass(frozen=True, slots=True)
class EvidenceAbsent:
    pass


class EvidenceStore(Protocol):
    """Provider-neutral evidence capability, never Domain authority."""

    def create_reservation_if_absent(
        self, key: EvidenceLookupKey, record: ReferenceReservationEvidence
    ) -> PortResult[
        EvidenceCreated | EvidenceAlreadyPresentSame | EvidenceAlreadyPresentConflict
    ]: ...

    def create_request_mapping_if_absent(
        self, key: EvidenceLookupKey, record: RequestReferenceRecoveryMapping
    ) -> PortResult[
        EvidenceCreated | EvidenceAlreadyPresentSame | EvidenceAlreadyPresentConflict
    ]: ...

    def read_reservation(
        self, key: EvidenceLookupKey
    ) -> PortResult[EvidenceFound[ReferenceReservationEvidence] | EvidenceAbsent]: ...

    def read_request_mapping(
        self, key: EvidenceLookupKey
    ) -> PortResult[EvidenceFound[RequestReferenceRecoveryMapping] | EvidenceAbsent]: ...
