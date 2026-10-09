from datetime import UTC, datetime

from daen_geocore.application.mutation_runtime import ReferenceReservationCoordinator
from daen_geocore.application.mutation_runtime.ports import (
    ReferenceReservationPlan,
    ReservationOutcome,
)
from daen_geocore.domain.references import (
    AccessPointRef,
    PlaceRef,
    SelectionRecordRef,
    SourceAssertionRef,
)
from daen_geocore.infrastructure.runtime.reference_generation import (
    REFERENCE_ENTROPY_BYTES,
    SecureReferenceCandidateGenerator,
)
from daen_geocore.ports.audit.store import MutationAuditRecord
from daen_geocore.ports.evidence.store import EvidenceLookupKey
from daen_geocore.ports.idempotency.store import IdempotencyBindingKey
from daen_geocore.ports.persistence.records import OpaqueEncodedPayload
from daen_geocore.ports.recovery.gate import RecoveryIncarnation, RecoveryState
from daen_geocore.ports.result import PortError
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueRequestIdentity,
    TechnicalOperationKey,
)
from tests.fakes.ports import FakeRecoveryGate, InMemoryEvidenceStore


def test_reference_generator_uses_explicit_secure_entropy(monkeypatch) -> None:
    requested: list[int] = []

    def entropy(size: int) -> bytes:
        requested.append(size)
        return b"\x01" * size

    monkeypatch.setattr(
        "daen_geocore.infrastructure.runtime.reference_generation.secrets.token_bytes",
        entropy,
    )
    generator = SecureReferenceCandidateGenerator()
    assert isinstance(generator.new_place_ref(), PlaceRef)
    assert isinstance(generator.new_source_assertion_ref(), SourceAssertionRef)
    assert isinstance(generator.new_selection_record_ref(), SelectionRecordRef)
    assert isinstance(generator.new_access_point_ref(), AccessPointRef)
    assert generator.new_place_history_fact_ref().value
    assert generator.new_assertion_history_fact_ref().value
    assert generator.new_state_witness().value
    assert requested == [REFERENCE_ENTROPY_BYTES] * 7


def test_mutation_audit_requires_utc_timestamp() -> None:
    key = IdempotencyBindingKey(OpaqueClientIdentity("client"), OpaqueRequestIdentity("request"))
    payload = OpaqueEncodedPayload("test.v1", b"opaque")
    record = MutationAuditRecord(
        key,
        IntentFingerprint("intent"),
        TechnicalOperationKey("operation"),
        datetime(2026, 10, 9, tzinfo=UTC),
        payload,
        payload,
    )
    assert record.recorded_at.tzinfo is UTC


def test_candidate_requires_reservation_evidence(monkeypatch) -> None:
    monkeypatch.setattr(
        "daen_geocore.infrastructure.runtime.reference_generation.secrets.token_bytes",
        lambda size: bytes([2]) * size,
    )
    candidate = SecureReferenceCandidateGenerator().new_place_ref()
    plan = ReferenceReservationPlan(EvidenceLookupKey("candidate"), (candidate,))
    coordinator = ReferenceReservationCoordinator(
        FakeRecoveryGate(RecoveryState.READY, RecoveryIncarnation("R1")),
        InMemoryEvidenceStore(),
    )
    assert coordinator.reserve(plan).value is ReservationOutcome.PREPARED
    unavailable = InMemoryEvidenceStore(available=False)
    blocked = ReferenceReservationCoordinator(
        FakeRecoveryGate(RecoveryState.READY, RecoveryIncarnation("R1")), unavailable
    )
    result = blocked.reserve(ReferenceReservationPlan(EvidenceLookupKey("other"), (candidate,)))
    assert isinstance(result, PortError)
