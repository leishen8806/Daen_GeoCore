from dataclasses import dataclass
from enum import StrEnum

from daen_geocore.ports.evidence.store import (
    EvidenceLookupKey,
    RequestReferenceRecoveryMapping,
    StableReference,
)


@dataclass(frozen=True, slots=True)
class ReferenceReservationPlan:
    lookup_key: EvidenceLookupKey
    candidates: tuple[StableReference, ...]
    correlation: str | None = None


class ReservationOutcome(StrEnum):
    PREPARED = "prepared"
    BLOCKED = "blocked"
    CONFLICTING_EVIDENCE = "conflicting_evidence"


class RecoveryMappingOutcome(StrEnum):
    CREATED = "created"
    REUSED = "reused"
    CONFLICT = "conflict"


@dataclass(frozen=True, slots=True)
class RecoveryMappingResult:
    outcome: RecoveryMappingOutcome
    mapping: RequestReferenceRecoveryMapping | None
