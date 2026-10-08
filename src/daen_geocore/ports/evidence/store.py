from dataclasses import dataclass
from typing import Protocol, TypeVar

from daen_geocore.ports.result import PortResult


@dataclass(frozen=True, slots=True)
class ReferenceReservationEvidence:
    """Permanent non-reuse reservation evidence; not a request mapping."""

    payload: bytes


@dataclass(frozen=True, slots=True)
class RequestReferenceRecoveryMapping:
    """Request-to-reference recovery evidence; not commit proof."""

    payload: bytes


EvidenceT = TypeVar("EvidenceT")


@dataclass(frozen=True, slots=True)
class EvidenceCreated:
    pass


@dataclass(frozen=True, slots=True)
class EvidenceAlreadyPresent:
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
    ) -> PortResult[EvidenceCreated | EvidenceAlreadyPresent]: ...

    def create_request_mapping_if_absent(
        self, key: str, record: RequestReferenceRecoveryMapping
    ) -> PortResult[EvidenceCreated | EvidenceAlreadyPresent]: ...

    def read_reservation(
        self, key: str
    ) -> PortResult[EvidenceFound[ReferenceReservationEvidence] | EvidenceAbsent]: ...

    def read_request_mapping(
        self, key: str
    ) -> PortResult[EvidenceFound[RequestReferenceRecoveryMapping] | EvidenceAbsent]: ...
