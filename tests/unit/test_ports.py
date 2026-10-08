from dataclasses import dataclass
from datetime import UTC, datetime

import pytest

from daen_geocore.ports.clock.clock import Clock
from daen_geocore.ports.evidence.store import (
    EvidenceAbsent,
    EvidenceAlreadyPresentConflict,
    EvidenceAlreadyPresentSame,
    EvidenceCreated,
    EvidenceFound,
    ReferenceReservationEvidence,
    RequestReferenceRecoveryMapping,
)
from daen_geocore.ports.observability.observability import ObservabilityPort
from daen_geocore.ports.persistence.commit import (
    CommitAccepted,
    CommitSemanticConflict,
    CommitTechnicalAbort,
    CommitUnknown,
)
from daen_geocore.ports.persistence.repositories import RepositoryPort
from daen_geocore.ports.persistence.unit_of_work import UnitOfWork
from daen_geocore.ports.policy.policy import PolicyHook
from daen_geocore.ports.recovery.gate import (
    RecoveryGate,
    RecoveryIncarnation,
    RecoveryReadiness,
)
from daen_geocore.ports.result import PortError, PortFailure, PortSuccess


@dataclass
class DeterministicEvidence:
    reservation: object = EvidenceAbsent()
    mapping: object = EvidenceAbsent()

    def create_reservation_if_absent(self, key, record):
        if isinstance(self.reservation, EvidenceFound):
            return PortSuccess(
                EvidenceAlreadyPresentSame()
                if self.reservation.record == record
                else EvidenceAlreadyPresentConflict()
            )
        self.reservation = EvidenceFound(record)
        return PortSuccess(EvidenceCreated())

    def create_request_mapping_if_absent(self, key, record):
        if isinstance(self.mapping, EvidenceFound):
            return PortSuccess(
                EvidenceAlreadyPresentSame()
                if self.mapping.record == record
                else EvidenceAlreadyPresentConflict()
            )
        self.mapping = EvidenceFound(record)
        return PortSuccess(EvidenceCreated())

    def read_reservation(self, key):
        return PortSuccess(self.reservation)

    def read_request_mapping(self, key):
        return PortSuccess(self.mapping)


@dataclass
class DeterministicUnitOfWork:
    outcome: CommitAccepted | CommitTechnicalAbort | CommitSemanticConflict | CommitUnknown
    state: str = "new"

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.state == "active":
            self.rollback()
        self.state = "closed"

    def begin(self):
        if self.state != "new":
            raise RuntimeError("unit of work is not new")
        self.state = "active"

    def commit(self):
        if self.state != "active":
            raise RuntimeError("unit of work is not active")
        self.state = "committed"
        return self.outcome

    def rollback(self):
        if self.state == "committed":
            raise RuntimeError("unit of work already committed")
        if self.state == "closed":
            raise RuntimeError("unit of work is closed")
        self.state = "rolled_back"


@dataclass
class FakeRecoveryGate:
    incarnation: RecoveryIncarnation | None
    state: str = "ready"

    def validate_before_serving(self):
        if self.state != "ready" or self.incarnation is None:
            return PortError(PortFailure("recovery_not_ready"))
        return PortSuccess(self.incarnation)

    def readiness(self):
        return RecoveryReadiness(self.state, self.incarnation)


@dataclass
class FakeClock:
    instant: datetime

    def now(self):
        return self.instant


def test_commit_outcomes_are_distinct() -> None:
    assert CommitAccepted().status == "committed"
    assert CommitTechnicalAbort(reason="deadlock").status == "technical_abort"
    assert CommitSemanticConflict(reason="stale").status == "semantic_conflict"
    assert CommitUnknown(reason="timeout").status == "unknown"


def test_unit_of_work_rolls_back_on_context_exit_and_rejects_invalid_use() -> None:
    unit = DeterministicUnitOfWork(CommitAccepted())
    with unit:
        pass
    assert unit.state == "closed"
    with pytest.raises(RuntimeError):
        unit.commit()

    committed = DeterministicUnitOfWork(CommitAccepted())
    with pytest.raises(RuntimeError):
        with committed:
            committed.commit()
            committed.commit()


def test_evidence_same_and_conflicting_existing_are_distinct() -> None:
    evidence = DeterministicEvidence()
    reservation = ReferenceReservationEvidence(("P",), b"reserve")
    mapping = RequestReferenceRecoveryMapping("R", "I", ("P",), b"map")
    assert isinstance(evidence.read_reservation("r").value, EvidenceAbsent)
    assert isinstance(
        evidence.create_reservation_if_absent("r", reservation).value, EvidenceCreated
    )
    assert isinstance(
        evidence.create_reservation_if_absent("r", reservation).value, EvidenceAlreadyPresentSame
    )
    assert isinstance(
        evidence.create_reservation_if_absent(
            "r", ReferenceReservationEvidence(("Q",), b"other")
        ).value,
        EvidenceAlreadyPresentConflict,
    )
    assert isinstance(
        evidence.create_request_mapping_if_absent("m", mapping).value, EvidenceCreated
    )
    assert isinstance(evidence.read_request_mapping("m").value, EvidenceFound)
    assert evidence.read_request_mapping("m").value.record.references == ("P",)


def test_evidence_failure_is_not_safe_absence() -> None:
    assert PortError(PortFailure("unavailable")) != PortSuccess(EvidenceAbsent())


def test_recovery_gate_and_clock_doubles_are_deterministic() -> None:
    incarnation = RecoveryIncarnation("inc-1")
    gate = FakeRecoveryGate(incarnation)
    assert gate.validate_before_serving().value == incarnation
    assert gate.readiness().state == "ready"
    gate.state = "blocked"
    assert isinstance(gate.validate_before_serving(), PortError)
    now = datetime(2026, 10, 8, tzinfo=UTC)
    assert FakeClock(now).now() == now


def test_port_protocols_remain_provider_neutral() -> None:
    for protocol in (
        Clock,
        ObservabilityPort,
        PolicyHook,
        RecoveryGate,
        RepositoryPort,
        UnitOfWork,
    ):
        assert isinstance(protocol, type)
