from dataclasses import dataclass
from typing import Protocol

from daen_geocore.ports.result import PortResult


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    """Opaque evidence bytes with no provider or Domain interpretation."""

    payload: bytes
    permanent: bool = False


class EvidenceStore(Protocol):
    """Recovery/reservation evidence capability, not Domain authority."""

    def create_if_absent(self, key: str, record: EvidenceRecord) -> PortResult[bool]: ...

    def read(self, key: str) -> PortResult[EvidenceRecord | None]: ...
