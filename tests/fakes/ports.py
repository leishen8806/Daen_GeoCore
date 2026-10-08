from dataclasses import dataclass
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
from daen_geocore.ports.persistence.commit import (
    CommitAccepted,
    CommitOutcome,
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

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.state == "active":
            self.rollback()
        self.state = "closed"

    def begin(self) -> None:
        if self.state != "new":
            raise RuntimeError("unit of work is not new")
        self.state = "active"

    def commit(self) -> CommitOutcome:
        if self.state != "active":
            raise RuntimeError("unit of work is not active")
        self.state = "committed"
        return self.outcome

    def rollback(self) -> None:
        if self.state in {"committed", "closed"}:
            raise RuntimeError("unit of work cannot roll back")
        self.state = "rolled_back"


@dataclass
class InMemoryEvidenceStore:
    available: bool = True
    reservation: ReferenceReservationEvidence | None = None
    mapping: RequestReferenceRecoveryMapping | None = None

    def _unavailable(self):
        return PortError(PortFailure("evidence_unavailable"))

    def create_reservation_if_absent(self, key: EvidenceLookupKey, record):
        if not self.available:
            return self._unavailable()
        if self.reservation is None:
            self.reservation = record
            return PortSuccess(EvidenceCreated())
        return PortSuccess(
            EvidenceAlreadyPresentSame()
            if self.reservation == record
            else EvidenceAlreadyPresentConflict()
        )

    def create_request_mapping_if_absent(self, key: EvidenceLookupKey, record):
        if not self.available:
            return self._unavailable()
        if self.mapping is None:
            self.mapping = record
            return PortSuccess(EvidenceCreated())
        return PortSuccess(
            EvidenceAlreadyPresentSame()
            if self.mapping == record
            else EvidenceAlreadyPresentConflict()
        )

    def read_reservation(self, key: EvidenceLookupKey):
        if not self.available:
            return self._unavailable()
        return PortSuccess(
            EvidenceAbsent() if self.reservation is None else EvidenceFound(self.reservation)
        )

    def read_request_mapping(self, key: EvidenceLookupKey):
        if not self.available:
            return self._unavailable()
        return PortSuccess(
            EvidenceAbsent() if self.mapping is None else EvidenceFound(self.mapping)
        )


@dataclass
class FakeRecoveryGate:
    state: RecoveryState
    incarnation: RecoveryIncarnation | None
    reason: str | None = None

    def observation(self) -> RecoveryObservation:
        return RecoveryObservation(self.state, self.incarnation, self.reason)

    def validate_before_authoritative_serving(self):
        if self.observation().may_authoritative_serve and self.incarnation is not None:
            return PortSuccess(self.incarnation)
        return PortError(PortFailure("recovery_not_ready"))


@dataclass
class FakeClock:
    instant: datetime

    def __post_init__(self) -> None:
        if self.instant.tzinfo is None or self.instant.utcoffset() != UTC.utcoffset(self.instant):
            raise ValueError("FakeClock requires UTC-aware datetime")

    def now(self) -> datetime:
        return self.instant
