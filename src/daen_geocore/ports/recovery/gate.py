from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class RecoveryReadiness:
    """Provider-neutral readiness observation for authoritative serving."""

    ready: bool
    reason: str | None = None


class RecoveryGate(Protocol):
    """Recovery-lineage gate; implementation owns reconciliation mechanics."""

    def readiness(self) -> RecoveryReadiness: ...
