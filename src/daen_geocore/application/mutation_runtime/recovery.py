from daen_geocore.ports.evidence.store import (
    EvidenceAlreadyPresentSame,
    EvidenceCreated,
    EvidenceFound,
    EvidenceLookupKey,
    EvidenceStore,
    ReferenceReservationEvidence,
    RequestReferenceRecoveryMapping,
)
from daen_geocore.ports.recovery.gate import RecoveryGate
from daen_geocore.ports.result import PortError, PortResult, PortSuccess

from .ports import (
    RecoveryMappingOutcome,
    RecoveryMappingResult,
    ReferenceReservationPlan,
    ReservationOutcome,
)


class ReferenceReservationCoordinator:
    def __init__(self, gate: RecoveryGate, evidence: EvidenceStore) -> None:
        self._gate, self._evidence = gate, evidence

    def reserve(self, plan: ReferenceReservationPlan) -> PortResult[ReservationOutcome]:
        if not self._gate.observation().may_issue_stable_references:
            return PortSuccess(ReservationOutcome.BLOCKED)
        result = self._evidence.create_reservation_if_absent(
            plan.lookup_key, ReferenceReservationEvidence(plan.candidates, plan.correlation)
        )
        if isinstance(result, PortError):
            return result
        if isinstance(result.value, (EvidenceCreated, EvidenceAlreadyPresentSame)):
            return PortSuccess(ReservationOutcome.PREPARED)
        return PortSuccess(ReservationOutcome.CONFLICTING_EVIDENCE)


class RecoveryMappingCoordinator:
    def __init__(self, evidence: EvidenceStore) -> None:
        self._evidence = evidence

    def resolve(
        self, key: EvidenceLookupKey, mapping: RequestReferenceRecoveryMapping
    ) -> PortResult[RecoveryMappingResult]:
        result = self._evidence.create_request_mapping_if_absent(key, mapping)
        if isinstance(result, PortError):
            return result
        if isinstance(result.value, EvidenceCreated):
            return PortSuccess(RecoveryMappingResult(RecoveryMappingOutcome.CREATED, mapping))
        existing = self._evidence.read_request_mapping(key)
        if isinstance(existing, PortError):
            return existing
        if not isinstance(existing.value, EvidenceFound):
            return PortSuccess(RecoveryMappingResult(RecoveryMappingOutcome.CONFLICT, None))
        stored = existing.value.record
        same_identity = (
            stored.client_identity == mapping.client_identity
            and stored.request_identity == mapping.request_identity
            and stored.intent_fingerprint == mapping.intent_fingerprint
            and stored.operation_key == mapping.operation_key
        )
        if same_identity:
            return PortSuccess(RecoveryMappingResult(RecoveryMappingOutcome.REUSED, stored))
        return PortSuccess(RecoveryMappingResult(RecoveryMappingOutcome.CONFLICT, None))
