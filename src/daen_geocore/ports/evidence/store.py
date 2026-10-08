from dataclasses import dataclass
from typing import Protocol

from daen_geocore.ports.result import PortResult


@dataclass(frozen=True, slots=True)
class ReferenceReservationEvidence:
    """Permanent non-reuse evidence, separate from request mapping."""

    references: tuple[str, ...]
    payload: bytes = b""


@dataclass(frozen=True, slots=True)
class RequestReferenceRecoveryMapping:
    """Request-to-reference recovery evidence, not commit proof."""

    request_identity: str
    semantic_intent_fingerprint: str
    references: tuple[str, ...]
    payload: bytes = b""


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
        self, key: str, record: ReferenceReservationEvidence
    ) -> PortResult[
        EvidenceCreated | EvidenceAlreadyPresentSame | EvidenceAlreadyPresentConflict
    ]: ...

    def create_request_mapping_if_absent(
        self, key: str, record: RequestReferenceRecoveryMapping
    ) -> PortResult[
        EvidenceCreated | EvidenceAlreadyPresentSame | EvidenceAlreadyPresentConflict
    ]: ...

    def read_reservation(
        self, key: str
    ) -> PortResult[EvidenceFound[ReferenceReservationEvidence] | EvidenceAbsent]: ...

    def read_request_mapping(
        self, key: str
    ) -> PortResult[EvidenceFound[RequestReferenceRecoveryMapping] | EvidenceAbsent]: ...
