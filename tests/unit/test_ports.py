from datetime import UTC, datetime

import pytest

from daen_geocore.domain.references import PlaceRef, SourceAssertionRef
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
    CommitTechnicalAbort,
    CommitUnknown,
)
from daen_geocore.ports.recovery.gate import RecoveryIncarnation, RecoveryState
from daen_geocore.ports.result import PortError, PortFailure, PortSuccess
from daen_geocore.ports.technical import (
    EvidenceLookupKey,
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueReplayMetadata,
    OpaqueRequestIdentity,
    TechnicalOperationKey,
)

from ..fakes.ports import FakeClock, FakeRecoveryGate, FakeUnitOfWork, InMemoryEvidenceStore


def mapping(place_token: str = "P") -> RequestReferenceRecoveryMapping:
    return RequestReferenceRecoveryMapping(
        OpaqueClientIdentity("C"),
        OpaqueRequestIdentity("R"),
        IntentFingerprint("F"),
        TechnicalOperationKey("internal-place-provisioning"),
        (PlaceRef(place_token), SourceAssertionRef("A1"), SourceAssertionRef("A2")),
        OpaqueReplayMetadata((("decision", "new"),)),
    )


def test_commit_knowledge_and_technical_failure_separation() -> None:
    assert CommitAccepted().status == "committed"
    assert CommitTechnicalAbort(reason="deadlock").status == "technical_abort"
    assert CommitUnknown(reason="timeout").status == "unknown"
    failure = PortFailure("deadlock", TechnicalFailureClass.RETRYABLE_TRANSACTION_ABORT)
    assert failure.classification is TechnicalFailureClass.RETRYABLE_TRANSACTION_ABORT


def test_uow_context_rolls_back_and_rejects_double_commit() -> None:
    unit = FakeUnitOfWork()
    with unit:
        pass
    assert unit.state == "closed"
    with pytest.raises(RuntimeError):
        unit.commit()
    unit = FakeUnitOfWork()
    with pytest.raises(RuntimeError):
        with unit:
            unit.commit()
            unit.commit()


def test_cd1_mapping_preserves_typed_references_and_conflicts() -> None:
    store = InMemoryEvidenceStore()
    key = EvidenceLookupKey("lookup")
    value = mapping()
    result = store.create_request_mapping_if_absent(key, value)
    assert isinstance(result.value, EvidenceCreated)
    read = store.read_request_mapping(key)
    assert isinstance(read.value, EvidenceFound)
    assert isinstance(read.value.record.references[0], PlaceRef)
    assert isinstance(read.value.record.references[1], SourceAssertionRef)
    assert isinstance(
        store.create_request_mapping_if_absent(key, value).value, EvidenceAlreadyPresentSame
    )
    assert isinstance(
        store.create_request_mapping_if_absent(key, mapping("Q")).value,
        EvidenceAlreadyPresentConflict,
    )
    assert store.read_request_mapping(key).value.record.references[0] == PlaceRef("P")


def test_reservation_and_mapping_are_distinct_records() -> None:
    store = InMemoryEvidenceStore()
    key = EvidenceLookupKey("lookup")
    reservation = ReferenceReservationEvidence((PlaceRef("P"),))
    assert isinstance(store.create_reservation_if_absent(key, reservation).value, EvidenceCreated)
    assert isinstance(store.read_reservation(key).value, EvidenceFound)
    assert store.read_reservation(key).value.record != mapping()


def test_unavailable_store_is_error_not_absence() -> None:
    store = InMemoryEvidenceStore(available=False)
    key = EvidenceLookupKey("lookup")
    assert isinstance(
        store.create_reservation_if_absent(key, ReferenceReservationEvidence(())), PortError
    )
    assert isinstance(store.create_request_mapping_if_absent(key, mapping()), PortError)
    assert isinstance(store.read_reservation(key), PortError)
    assert isinstance(store.read_request_mapping(key), PortError)
    assert not isinstance(PortSuccess(EvidenceAbsent()), PortError)


def test_recovery_gate_all_states_and_capabilities() -> None:
    incarnation = RecoveryIncarnation("inc-1")
    for state in RecoveryState:
        gate = FakeRecoveryGate(state, incarnation if state is RecoveryState.READY else None)
        observation = gate.observation()
        assert observation.may_authoritative_serve is (state is RecoveryState.READY)
        assert observation.may_issue_stable_references is (state is RecoveryState.READY)
        assert observation.recovery_required is (state is not RecoveryState.READY)
        if state is RecoveryState.READY:
            assert isinstance(gate.validate_before_authoritative_serving(), PortSuccess)
        else:
            assert isinstance(gate.validate_before_authoritative_serving(), PortError)


def test_fake_clock_requires_utc_and_is_deterministic() -> None:
    instant = datetime(2026, 10, 8, tzinfo=UTC)
    clock = FakeClock(instant)
    assert clock.now() == instant == clock.now()
    with pytest.raises(ValueError):
        FakeClock(datetime(2026, 10, 8))
