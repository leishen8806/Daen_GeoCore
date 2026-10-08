from dataclasses import dataclass, field
from datetime import UTC, datetime

from daen_geocore.ports.evidence.store import (
    EvidenceAbsent,
    EvidenceAlreadyPresentConflict,
    EvidenceAlreadyPresentSame,
    EvidenceCreated,
    EvidenceFound,
    ReferenceReservationEvidence,
    RequestReferenceRecoveryMapping,
)
from daen_geocore.ports.failures import TechnicalFailureClass
from daen_geocore.ports.persistence.commit import (
    CommitAccepted,
    CommitNotCommitted,
    CommitOutcome,
    CommitUnknown,
)
from daen_geocore.ports.recovery.gate import RecoveryIncarnation, RecoveryObservation, RecoveryState
from daen_geocore.ports.result import PortError, PortFailure, PortSuccess
from daen_geocore.ports.technical import EvidenceLookupKey


@dataclass
class FakeCommitPort:
    outcome: CommitOutcome

    def commit(self) -> CommitOutcome:
        return self.outcome

    def rollback(self) -> None:
        pass


@dataclass
class FakeUnitOfWork:
    outcome: CommitOutcome = CommitAccepted()
    state: str = "new"
    last_outcome: CommitOutcome | None = None

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.state == "active":
            self.rollback()
        elif self.state not in {"committed", "not_committed", "unknown", "rolled_back"}:
            raise RuntimeError("unit of work is not active")
        if self.state == "unknown":
            self.state = "unknown_closed"
        else:
            self.state = "closed"

    def begin(self) -> None:
        if self.state != "new":
            raise RuntimeError("unit of work is not new")
        self.state = "active"

    def commit(self) -> CommitOutcome:
        if self.state != "active":
            raise RuntimeError("unit of work is not active")
        self.last_outcome = self.outcome
        if isinstance(self.outcome, CommitAccepted):
            self.state = "committed"
        elif isinstance(self.outcome, CommitNotCommitted):
            self.state = "not_committed"
        elif isinstance(self.outcome, CommitUnknown):
            self.state = "unknown"
        else:
            raise TypeError("unsupported commit outcome")
        return self.outcome

    def rollback(self) -> None:
        if self.state in {"committed", "closed", "unknown", "unknown_closed", "not_committed"}:
            raise RuntimeError("unit of work cannot roll back")
        self.state = "rolled_back"


@dataclass
class InMemoryEvidenceStore:
    available: bool = True
    reservations: dict[EvidenceLookupKey, ReferenceReservationEvidence] = field(
        default_factory=dict
    )
    mappings: dict[EvidenceLookupKey, RequestReferenceRecoveryMapping] = field(default_factory=dict)

    def _unavailable(self):
        return PortError(
            PortFailure("evidence_unavailable", TechnicalFailureClass.TRANSIENT_UNAVAILABLE)
        )

    def create_reservation_if_absent(self, key: EvidenceLookupKey, record):
        if not self.available:
            return self._unavailable()
        existing = self.reservations.get(key)
        if existing is None:
            self.reservations[key] = record
            return PortSuccess(EvidenceCreated())
        return PortSuccess(
            EvidenceAlreadyPresentSame() if existing == record else EvidenceAlreadyPresentConflict()
        )

    def create_request_mapping_if_absent(self, key: EvidenceLookupKey, record):
        if not self.available:
            return self._unavailable()
        existing = self.mappings.get(key)
        if existing is None:
            self.mappings[key] = record
            return PortSuccess(EvidenceCreated())
        return PortSuccess(
            EvidenceAlreadyPresentSame() if existing == record else EvidenceAlreadyPresentConflict()
        )

    def read_reservation(self, key: EvidenceLookupKey):
        if not self.available:
            return self._unavailable()
        record = self.reservations.get(key)
        return PortSuccess(EvidenceAbsent() if record is None else EvidenceFound(record))

    def read_request_mapping(self, key: EvidenceLookupKey):
        if not self.available:
            return self._unavailable()
        record = self.mappings.get(key)
        return PortSuccess(EvidenceAbsent() if record is None else EvidenceFound(record))


@dataclass
class FakeRecoveryGate:
    state: RecoveryState
    incarnation: RecoveryIncarnation | None
    reason: str | None = None

    def observation(self) -> RecoveryObservation:
        return RecoveryObservation(self.state, self.incarnation, self.reason)

    def validate_before_authoritative_serving(self):
        observation = self.observation()
        if observation.may_authoritative_serve:
            return PortSuccess(observation.incarnation)
        return PortError(PortFailure("recovery_not_ready"))


@dataclass
class FakeClock:
    instant: datetime

    def __post_init__(self) -> None:
        if self.instant.tzinfo is None or self.instant.utcoffset() != UTC.utcoffset(self.instant):
            raise ValueError("FakeClock requires UTC-aware datetime")

    def now(self) -> datetime:
        return self.instant
