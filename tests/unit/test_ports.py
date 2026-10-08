from datetime import UTC, datetime

from daen_geocore.ports.clock.clock import Clock
from daen_geocore.ports.evidence.store import EvidenceRecord, EvidenceStore
from daen_geocore.ports.observability.observability import ObservabilityPort
from daen_geocore.ports.persistence.commit import CommitPort
from daen_geocore.ports.persistence.repositories import RepositoryPort
from daen_geocore.ports.persistence.unit_of_work import UnitOfWork
from daen_geocore.ports.policy.policy import PolicyHook
from daen_geocore.ports.recovery.gate import RecoveryGate, RecoveryReadiness
from daen_geocore.ports.result import PortFailure, PortResult


def test_port_results_are_typed_and_transport_neutral() -> None:
    success = PortResult(value=None)
    failure = PortResult(failure=PortFailure("unavailable"))
    assert success.succeeded
    assert not failure.succeeded
    assert EvidenceRecord(b"opaque", permanent=True).permanent


def test_port_protocols_expose_no_provider_types() -> None:
    for protocol in (
        Clock,
        CommitPort,
        EvidenceStore,
        ObservabilityPort,
        PolicyHook,
        RecoveryGate,
        RepositoryPort,
        UnitOfWork,
    ):
        assert isinstance(protocol, type)
    readiness = RecoveryReadiness(ready=True)
    assert readiness.ready
    assert datetime.now(UTC).tzinfo is not None
