from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from daen_geocore.ports.result import PortResult


class RecoveryState(StrEnum):
    READY = "ready"
    RECOVERY_REQUIRED = "recovery_required"
    RECONCILING = "reconciling"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class RecoveryIncarnation:
    """Opaque incarnation observed from recovery control state."""

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("recovery incarnation must be a string")


@dataclass(frozen=True, slots=True)
class RecoveryObservation:
    state: RecoveryState
    incarnation: RecoveryIncarnation | None = None
    reason: str | None = None

    @property
    def may_authoritative_serve(self) -> bool:
        return self.state is RecoveryState.READY

    @property
    def may_issue_stable_references(self) -> bool:
        return self.state is RecoveryState.READY

    @property
    def recovery_required(self) -> bool:
        return self.state is not RecoveryState.READY


class RecoveryGate(Protocol):
    """Fail-closed capability for the recovery serving gate."""

    def observation(self) -> RecoveryObservation: ...

    def validate_before_authoritative_serving(self) -> PortResult[RecoveryIncarnation]: ...
