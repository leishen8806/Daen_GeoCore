from dataclasses import dataclass
from typing import Literal, Protocol

from daen_geocore.ports.result import PortResult


@dataclass(frozen=True, slots=True)
class RecoveryIncarnation:
    """Opaque incarnation observed from recovery control state."""

    value: str


@dataclass(frozen=True, slots=True)
class RecoveryReadiness:
    state: Literal["recovering", "ready", "blocked"]
    incarnation: RecoveryIncarnation | None = None
    reason: str | None = None


class RecoveryGate(Protocol):
    """Fail-closed capability for the recovery serving gate."""

    def validate_before_serving(self) -> PortResult[RecoveryIncarnation]: ...

    def readiness(self) -> RecoveryReadiness: ...
