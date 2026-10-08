from dataclasses import dataclass

from daen_geocore.ports.evidence.store import (
    EvidenceAbsent,
    EvidenceAlreadyPresent,
    EvidenceCreated,
    EvidenceFound,
    ReferenceReservationEvidence,
    RequestReferenceRecoveryMapping,
)
from daen_geocore.ports.persistence.commit import CommitAccepted, CommitRejected, CommitUnknown
from daen_geocore.ports.recovery.gate import RecoveryReadiness
from daen_geocore.ports.result import PortError, PortFailure, PortSuccess


@dataclass
class DeterministicCommit:
    outcome: CommitAccepted | CommitRejected | CommitUnknown

    def commit(self):
        return self.outcome

    def rollback(self) -> None:
        pass


@dataclass
class DeterministicEvidence:
    reservation: object = EvidenceAbsent()
    mapping: object = EvidenceAbsent()

    def create_reservation_if_absent(self, key, record):
        if isinstance(self.reservation, EvidenceFound):
            return PortSuccess(EvidenceAlreadyPresent())
        self.reservation = EvidenceFound(record)
        return PortSuccess(EvidenceCreated())

    def create_request_mapping_if_absent(self, key, record):
        if isinstance(self.mapping, EvidenceFound):
            return PortSuccess(EvidenceAlreadyPresent())
        self.mapping = EvidenceFound(record)
        return PortSuccess(EvidenceCreated())

    def read_reservation(self, key):
        return PortSuccess(self.reservation)

    def read_request_mapping(self, key):
        return PortSuccess(self.mapping)


def test_commit_unknown_is_explicit() -> None:
    assert DeterministicCommit(CommitUnknown(reason="timeout")).commit().status == "unknown"
    assert DeterministicCommit(CommitRejected(reason="conflict")).commit().status == "rejected"
    assert DeterministicCommit(CommitAccepted()).commit().status == "committed"


def test_evidence_categories_and_absence_are_distinct() -> None:
    evidence = DeterministicEvidence()
    assert isinstance(evidence.read_reservation("r"), PortSuccess)
    assert isinstance(evidence.read_reservation("r").value, EvidenceAbsent)
    assert isinstance(evidence.read_request_mapping("m").value, EvidenceAbsent)
    evidence.create_reservation_if_absent("r", ReferenceReservationEvidence(b"reserve"))
    evidence.create_request_mapping_if_absent("m", RequestReferenceRecoveryMapping(b"map"))
    assert isinstance(evidence.read_reservation("r").value, EvidenceFound)
    assert isinstance(evidence.read_request_mapping("m").value, EvidenceFound)
    assert evidence.read_reservation("r").value.record.payload == b"reserve"
    assert evidence.read_request_mapping("m").value.record.payload == b"map"


def test_failure_is_not_safe_absence() -> None:
    unavailable = PortError(PortFailure("unavailable"))
    absent = PortSuccess(EvidenceAbsent())
    assert unavailable != absent
    assert RecoveryReadiness(ready=False, reason="unavailable").ready is False


@dataclass
class DeterministicUnitOfWork:
    outcome: CommitAccepted | CommitRejected | CommitUnknown
    active: bool = False
    rolled_back: bool = False

    def begin(self) -> None:
        self.active = True

    def commit(self):
        self.active = False
        return self.outcome

    def rollback(self) -> None:
        self.active = False
        self.rolled_back = True


def test_unit_of_work_lifecycle_is_explicit() -> None:
    unit = DeterministicUnitOfWork(CommitAccepted())
    unit.begin()
    assert unit.active
    assert unit.commit().status == "committed"
    assert not unit.active
    unit.begin()
    unit.rollback()
    assert unit.rolled_back and not unit.active
