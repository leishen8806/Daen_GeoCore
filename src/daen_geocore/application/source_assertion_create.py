from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol

from daen_geocore.application.mutation_runtime import (
    RecoveryMappingCoordinator,
    RecoveryMappingOutcome,
    ReferenceReservationCoordinator,
    ReferenceReservationPlan,
    ReservationOutcome,
)
from daen_geocore.domain.references import PlaceRef, SourceAssertionRef
from daen_geocore.ports.audit.store import MutationAuditRecord, MutationAuditStore
from daen_geocore.ports.clock import Clock
from daen_geocore.ports.evidence.store import (
    EvidenceFound,
    EvidenceLookupKey,
    EvidenceStore,
    RequestReferenceRecoveryMapping,
)
from daen_geocore.ports.idempotency.store import (
    BindingRetention,
    CommittedBindingFound,
    CommittedIdempotencyStore,
    CommittedMutationBinding,
    CommittedMutationResult,
    IdempotencyBindingKey,
    IdempotencyCreateDisposition,
)
from daen_geocore.ports.persistence.commit import CommitAccepted, CommitNotCommitted, CommitUnknown
from daen_geocore.ports.persistence.records import (
    AssertionStandingHead,
    InsertDisposition,
    OpaqueEncodedPayload,
    PersistedQuality,
    PersistedScope,
    PersistedTypedValue,
    RecordAbsent,
    SourceAssertionRecord,
    StateWitness,
)
from daen_geocore.ports.persistence.repositories import AssertionsRepository, IdentityRepository
from daen_geocore.ports.recovery.gate import RecoveryGate
from daen_geocore.ports.references.generation import (
    ReferenceCandidateGenerator,
    StateWitnessGenerator,
)
from daen_geocore.ports.result import PortError, PortResult, PortSuccess
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueReplayMetadata,
    TechnicalOperationKey,
)

SOURCE_ASSERTION_CREATE_OPERATION = TechnicalOperationKey("source_assertion.create")
_AUDIT_ENCODING = "daen.step9.audit.v1"


@dataclass(frozen=True, slots=True)
class CreateSourceAssertionCommand:
    key: IdempotencyBindingKey
    evidence_lookup_key: EvidenceLookupKey
    intent_fingerprint: IntentFingerprint
    place_ref: PlaceRef
    fact_purpose: str
    value: PersistedTypedValue
    scope: PersistedScope
    source_provenance: OpaqueEncodedPayload
    quality: PersistedQuality
    mutation_provenance: OpaqueEncodedPayload


class SourceAssertionCreateOutcome(StrEnum):
    APPLIED = "applied"
    REPLAY = "replay"
    TARGET_PLACE_NOT_FOUND = "target_place_not_found"
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"
    RECOVERY_MAPPING_CONFLICT = "recovery_mapping_conflict"
    RECOVERY_NOT_READY = "recovery_not_ready"
    REFERENCE_EVIDENCE_CONFLICT = "reference_evidence_conflict"
    REFERENCE_COLLISION_OR_RECOVERY_CONFLICT = "reference_collision_or_recovery_conflict"
    AUDIT_CONFLICT = "audit_conflict"
    MALFORMED_RECOVERY_METADATA = "malformed_recovery_metadata"
    NOT_COMMITTED = "not_committed"
    COMMIT_OUTCOME_UNKNOWN = "commit_outcome_unknown"


@dataclass(frozen=True, slots=True)
class SourceAssertionCreateResult:
    outcome: SourceAssertionCreateOutcome
    source_assertion_ref: SourceAssertionRef | None = None


class SourceAssertionReferenceGenerator(
    ReferenceCandidateGenerator, StateWitnessGenerator, Protocol
):
    pass


class MutationUnitOfWork(Protocol):
    identity: IdentityRepository
    assertions: AssertionsRepository
    committed_idempotency: CommittedIdempotencyStore
    mutation_audit: MutationAuditStore

    def __enter__(self) -> MutationUnitOfWork: ...
    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: ...
    def commit(self) -> CommitAccepted | CommitNotCommitted | CommitUnknown: ...
    def rollback(self) -> None: ...


class MutationUnitOfWorkFactory(Protocol):
    def create(self) -> MutationUnitOfWork: ...


def _result(
    outcome: SourceAssertionCreateOutcome, ref: SourceAssertionRef | None = None
) -> PortSuccess[SourceAssertionCreateResult]:
    return PortSuccess(SourceAssertionCreateResult(outcome, ref))


def _mapping_metadata(witness: StateWitness, recorded_at: datetime) -> OpaqueReplayMetadata:
    return OpaqueReplayMetadata(
        (
            ("initial_state_witness", witness.value),
            ("recorded_at", recorded_at.isoformat()),
        )
    )


def _decode_mapping(
    mapping: RequestReferenceRecoveryMapping, command: CreateSourceAssertionCommand
) -> tuple[SourceAssertionRef, StateWitness, datetime] | None:
    if len(mapping.references) != 1 or not isinstance(mapping.references[0], SourceAssertionRef):
        return None
    raw_entries = mapping.replay_metadata.entries
    entries = dict(raw_entries)
    if (
        len(raw_entries) != 2
        or len(entries) != 2
        or set(entries) != {"initial_state_witness", "recorded_at"}
        or not entries["initial_state_witness"]
        or not entries["recorded_at"]
    ):
        return None
    try:
        recorded_at = datetime.fromisoformat(entries["recorded_at"])
        if recorded_at.tzinfo is None or recorded_at.utcoffset() != UTC.utcoffset(recorded_at):
            return None
        return mapping.references[0], StateWitness(entries["initial_state_witness"]), recorded_at
    except (TypeError, ValueError):
        return None


def _audit_details(
    command: CreateSourceAssertionCommand, ref: SourceAssertionRef
) -> OpaqueEncodedPayload:
    payload = json.dumps(
        {
            "fact_purpose": command.fact_purpose,
            "place_ref": command.place_ref.token,
            "source_assertion_ref": ref.token,
        },
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    return OpaqueEncodedPayload(_AUDIT_ENCODING, payload)


def _replay_reference(binding: CommittedMutationBinding) -> SourceAssertionRef | None:
    if (
        len(binding.result.references) != 1
        or not isinstance(binding.result.references[0], SourceAssertionRef)
        or binding.result.replay_metadata.entries != (("result_kind", "source_assertion_created"),)
    ):
        return None
    return binding.result.references[0]


class CreateSourceAssertion:
    def __init__(
        self,
        uow_factory: MutationUnitOfWorkFactory,
        evidence: EvidenceStore,
        recovery_gate: RecoveryGate,
        candidate_generator: SourceAssertionReferenceGenerator,
        clock: Clock,
    ) -> None:
        self._uow_factory = uow_factory
        self._evidence = evidence
        self._recovery_gate = recovery_gate
        self._candidate_generator = candidate_generator
        self._clock = clock
        self._mapping = RecoveryMappingCoordinator(evidence)
        self._reservation = ReferenceReservationCoordinator(recovery_gate, evidence)

    def execute(
        self, command: CreateSourceAssertionCommand
    ) -> PortResult[SourceAssertionCreateResult]:
        preflight = self._preflight(command)
        if isinstance(preflight, PortError):
            return preflight
        if preflight.value is not None:
            return PortSuccess(preflight.value)
        recovery = self._recover(command)
        if isinstance(recovery, PortError):
            return recovery
        if isinstance(recovery.value, SourceAssertionCreateResult):
            return PortSuccess(recovery.value)
        source_ref, witness, recorded_at = recovery.value
        reservation = self._reservation.reserve(
            ReferenceReservationPlan(command.evidence_lookup_key, (source_ref,))
        )
        if isinstance(reservation, PortError):
            return reservation
        if reservation.value is ReservationOutcome.BLOCKED:
            return _result(SourceAssertionCreateOutcome.RECOVERY_NOT_READY)
        if reservation.value is ReservationOutcome.CONFLICTING_EVIDENCE:
            return _result(SourceAssertionCreateOutcome.REFERENCE_EVIDENCE_CONFLICT)
        return self._authoritative(command, source_ref, witness, recorded_at)

    def _preflight(
        self, command: CreateSourceAssertionCommand
    ) -> PortResult[SourceAssertionCreateResult | None]:
        with self._uow_factory.create() as uow:
            committed = uow.committed_idempotency.read(command.key)
            if isinstance(committed, PortError):
                return committed
            if isinstance(committed.value, CommittedBindingFound):
                binding = committed.value.binding
                if (
                    binding.intent_fingerprint != command.intent_fingerprint
                    or binding.operation_key != SOURCE_ASSERTION_CREATE_OPERATION
                ):
                    return _result(SourceAssertionCreateOutcome.IDEMPOTENCY_CONFLICT)
                replay_ref = _replay_reference(binding)
                if replay_ref is None:
                    return _result(SourceAssertionCreateOutcome.MALFORMED_RECOVERY_METADATA)
                return _result(SourceAssertionCreateOutcome.REPLAY, replay_ref)
            place = uow.identity.get_place(command.place_ref)
            if isinstance(place, PortError):
                return place
            if isinstance(place.value, RecordAbsent):
                return _result(SourceAssertionCreateOutcome.TARGET_PLACE_NOT_FOUND)
        return PortSuccess(None)

    def _recover(
        self, command: CreateSourceAssertionCommand
    ) -> PortResult[
        tuple[SourceAssertionRef, StateWitness, datetime] | SourceAssertionCreateResult
    ]:
        existing = self._evidence.read_request_mapping(command.evidence_lookup_key)
        if isinstance(existing, PortError):
            return existing
        if isinstance(existing.value, EvidenceFound):
            mapping = existing.value.record
            if mapping.client_identity != command.key.client_identity:
                return _result(SourceAssertionCreateOutcome.RECOVERY_MAPPING_CONFLICT)
            if mapping.request_identity != command.key.request_identity:
                return _result(SourceAssertionCreateOutcome.RECOVERY_MAPPING_CONFLICT)
            if (
                mapping.intent_fingerprint != command.intent_fingerprint
                or mapping.operation_key != SOURCE_ASSERTION_CREATE_OPERATION
            ):
                return _result(SourceAssertionCreateOutcome.IDEMPOTENCY_CONFLICT)
            decoded = _decode_mapping(mapping, command)
            return (
                PortSuccess(decoded)
                if decoded is not None
                else _result(SourceAssertionCreateOutcome.MALFORMED_RECOVERY_METADATA)
            )
        source_ref = self._candidate_generator.new_source_assertion_ref()
        witness = self._candidate_generator.new_state_witness()
        recorded_at = self._clock.now()
        proposal = RequestReferenceRecoveryMapping(
            command.key.client_identity,
            command.key.request_identity,
            command.intent_fingerprint,
            SOURCE_ASSERTION_CREATE_OPERATION,
            (source_ref,),
            _mapping_metadata(witness, recorded_at),
        )
        resolved = self._mapping.resolve(command.evidence_lookup_key, proposal)
        if isinstance(resolved, PortError):
            return resolved
        if resolved.value.outcome is RecoveryMappingOutcome.CONFLICT:
            current = self._evidence.read_request_mapping(command.evidence_lookup_key)
            if isinstance(current, PortError):
                return current
            if not isinstance(current.value, EvidenceFound):
                return _result(SourceAssertionCreateOutcome.RECOVERY_MAPPING_CONFLICT)
            mapping = current.value.record
            if (
                mapping.client_identity == command.key.client_identity
                and mapping.request_identity == command.key.request_identity
                and (
                    mapping.intent_fingerprint != command.intent_fingerprint
                    or mapping.operation_key != SOURCE_ASSERTION_CREATE_OPERATION
                )
            ):
                return _result(SourceAssertionCreateOutcome.IDEMPOTENCY_CONFLICT)
            return _result(SourceAssertionCreateOutcome.RECOVERY_MAPPING_CONFLICT)
        mapping = resolved.value.mapping
        if mapping is None:
            return _result(SourceAssertionCreateOutcome.MALFORMED_RECOVERY_METADATA)
        decoded = _decode_mapping(mapping, command)
        return (
            PortSuccess(decoded)
            if decoded is not None
            else _result(SourceAssertionCreateOutcome.MALFORMED_RECOVERY_METADATA)
        )

    def _authoritative(
        self,
        command: CreateSourceAssertionCommand,
        source_ref: SourceAssertionRef,
        witness: StateWitness,
        recorded_at: datetime,
    ) -> PortResult[SourceAssertionCreateResult]:
        with self._uow_factory.create() as uow:
            committed = uow.committed_idempotency.read(command.key)
            if isinstance(committed, PortError):
                return committed
            if isinstance(committed.value, CommittedBindingFound):
                binding = committed.value.binding
                if (
                    binding.intent_fingerprint != command.intent_fingerprint
                    or binding.operation_key != SOURCE_ASSERTION_CREATE_OPERATION
                ):
                    uow.rollback()
                    return _result(SourceAssertionCreateOutcome.IDEMPOTENCY_CONFLICT)
                replay_ref = _replay_reference(binding)
                if replay_ref is None:
                    uow.rollback()
                    return _result(SourceAssertionCreateOutcome.MALFORMED_RECOVERY_METADATA)
                uow.rollback()
                return _result(SourceAssertionCreateOutcome.REPLAY, replay_ref)
            place = uow.identity.get_place(command.place_ref)
            if isinstance(place, PortError):
                uow.rollback()
                return place
            if isinstance(place.value, RecordAbsent):
                uow.rollback()
                return _result(SourceAssertionCreateOutcome.TARGET_PLACE_NOT_FOUND)
            assertion = SourceAssertionRecord(
                source_ref,
                command.place_ref,
                command.fact_purpose,
                command.value,
                command.scope,
                command.source_provenance,
                command.quality,
                recorded_at,
            )
            inserted = uow.assertions.insert_assertion_if_absent(assertion)
            if isinstance(inserted, PortError):
                uow.rollback()
                return inserted
            if inserted.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(
                    SourceAssertionCreateOutcome.REFERENCE_COLLISION_OR_RECOVERY_CONFLICT
                )
            headed = uow.assertions.insert_standing_head_if_absent(
                AssertionStandingHead(source_ref, None, witness)
            )
            if isinstance(headed, PortError):
                uow.rollback()
                return headed
            if headed.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(
                    SourceAssertionCreateOutcome.REFERENCE_COLLISION_OR_RECOVERY_CONFLICT
                )
            audit = MutationAuditRecord(
                command.key,
                command.intent_fingerprint,
                SOURCE_ASSERTION_CREATE_OPERATION,
                recorded_at,
                command.mutation_provenance,
                _audit_details(command, source_ref),
            )
            audited = uow.mutation_audit.append_if_absent(audit)
            if isinstance(audited, PortError):
                uow.rollback()
                return audited
            if audited.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(SourceAssertionCreateOutcome.AUDIT_CONFLICT)
            binding = CommittedMutationBinding(
                command.key,
                command.intent_fingerprint,
                SOURCE_ASSERTION_CREATE_OPERATION,
                CommittedMutationResult(
                    (source_ref,),
                    OpaqueReplayMetadata((("result_kind", "source_assertion_created"),)),
                ),
                BindingRetention.PUBLIC_REPLAY_HORIZON,
            )
            committed_result = uow.committed_idempotency.create_if_absent(binding)
            if isinstance(committed_result, PortError):
                uow.rollback()
                return committed_result
            if committed_result.value is IdempotencyCreateDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(SourceAssertionCreateOutcome.IDEMPOTENCY_CONFLICT)
            outcome = uow.commit()
            if isinstance(outcome, CommitAccepted):
                return _result(SourceAssertionCreateOutcome.APPLIED, source_ref)
            if isinstance(outcome, CommitNotCommitted):
                return _result(SourceAssertionCreateOutcome.NOT_COMMITTED)
            return _result(SourceAssertionCreateOutcome.COMMIT_OUTCOME_UNKNOWN)
