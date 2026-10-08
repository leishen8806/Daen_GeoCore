from dataclasses import dataclass
from typing import Protocol

from daen_geocore.ports.result import PortResult


@dataclass(frozen=True, slots=True)
class RecoveryReadiness:
    """Provider-neutral observation retained for diagnostics."""

    ready: bool
    reason: str | None = None


class RecoveryGate(Protocol):
    """Fail-closed capability for the recovery serving gate."""

    def validate_before_serving(self) -> PortResult[None]: ...

    def readiness(self) -> RecoveryReadiness: ...
