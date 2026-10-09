from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol

from daen_geocore.application.mutation_runtime import (
    BasisValidation,
    ReadSetRevalidator,
    ReadSetValidation,
    RecoveryMappingCoordinator,
    RecoveryMappingOutcome,
    ReferenceReservationCoordinator,
    ReferenceReservationPlan,
    ReservationOutcome,
)
from daen_geocore.domain.references import SourceAssertionRef
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
from daen_geocore.ports.mutation import (
    AssertionOwner,
    AuthoritativeReadSetCapture,
    InvalidMutationBasisToken,
    MutationBasisClaims,
    MutationBasisCodec,
    MutationBasisToken,
    OwnerAbsent,
    OwnerPresent,
    OwnerStateReader,
)
from daen_geocore.ports.persistence.commit import CommitAccepted, CommitNotCommitted, CommitUnknown
from daen_geocore.ports.persistence.records import (
    AssertionHistoryFact,
    AssertionHistoryFactRef,
    AssertionStandingHead,
    ConditionalWriteDisposition,
    InsertDisposition,
    OpaqueEncodedPayload,
    PersistedQuality,
    PersistedScope,
    PersistedTypedValue,
    RecordAbsent,
    SourceAssertionRecord,
    StateWitness,
)
from daen_geocore.ports.persistence.repositories import (
    AssertionsRepository,
    IdentityRepository,
    RepresentationRepository,
)
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

SUPERSEDE_OPERATION = TechnicalOperationKey("source_assertion.supersede")
CORRECT_OPERATION = TechnicalOperationKey("source_assertion.correct")
SUPERSESSION_FACT_TYPE = "source_assertion.superseded_by"
CORRECTION_FACT_TYPE = "source_assertion.corrected"


@dataclass(frozen=True, slots=True)
class SupersedeSourceAssertionCommand:
    key: IdempotencyBindingKey
    evidence_lookup_key: EvidenceLookupKey
    intent_fingerprint: IntentFingerprint
    target_source_assertion_ref: SourceAssertionRef
    mutation_basis: MutationBasisToken
    value: PersistedTypedValue
    scope: PersistedScope
    source_provenance: OpaqueEncodedPayload
    quality: PersistedQuality
    mutation_provenance: OpaqueEncodedPayload


@dataclass(frozen=True, slots=True)
class CorrectSourceAssertionCommand:
    key: IdempotencyBindingKey
    evidence_lookup_key: EvidenceLookupKey
    intent_fingerprint: IntentFingerprint
    target_source_assertion_ref: SourceAssertionRef
    mutation_basis: MutationBasisToken
    value: PersistedTypedValue
    scope: PersistedScope
    source_provenance: OpaqueEncodedPayload
    quality: PersistedQuality
    mutation_provenance: OpaqueEncodedPayload


TransitionCommand = SupersedeSourceAssertionCommand | CorrectSourceAssertionCommand


class SourceAssertionTransitionOutcome(StrEnum):
    APPLIED = "applied"
    REPLAY = "replay"
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"
    TARGET_ASSERTION_NOT_FOUND = "target_assertion_not_found"
    TARGET_STANDING_HEAD_MISSING = "target_standing_head_missing"
    TARGET_ALREADY_SUPERSEDED = "target_already_superseded"
    INSUFFICIENT_BASIS = "insufficient_basis"
    INVALID_BASIS = "invalid_basis"
    RECOVERY_INCARNATION_MISMATCH = "recovery_incarnation_mismatch"
    STALE_BASIS = "stale_basis"
    RECOVERY_MAPPING_CONFLICT = "recovery_mapping_conflict"
    MALFORMED_RECOVERY_METADATA = "malformed_recovery_metadata"
    RECOVERY_NOT_READY = "recovery_not_ready"
    REFERENCE_EVIDENCE_CONFLICT = "reference_evidence_conflict"
    REFERENCE_COLLISION = "reference_collision"
    HISTORY_CONFLICT = "history_conflict"
    STANDING_HEAD_CONFLICT = "standing_head_conflict"
    AUDIT_CONFLICT = "audit_conflict"
    NOT_COMMITTED = "not_committed"
    COMMIT_OUTCOME_UNKNOWN = "commit_outcome_unknown"


@dataclass(frozen=True, slots=True)
class SourceAssertionTransitionResult:
    outcome: SourceAssertionTransitionOutcome
    old_source_assertion_ref: SourceAssertionRef | None = None
    new_source_assertion_ref: SourceAssertionRef | None = None


class _TransitionGenerator(ReferenceCandidateGenerator, StateWitnessGenerator, Protocol):
    pass


class _TransitionUow(Protocol):
    identity: IdentityRepository
    assertions: AssertionsRepository
    representation: RepresentationRepository
    committed_idempotency: CommittedIdempotencyStore
    mutation_audit: MutationAuditStore

    def __enter__(self) -> _TransitionUow: ...
    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: ...
    def commit(self) -> CommitAccepted | CommitNotCommitted | CommitUnknown: ...
    def rollback(self) -> None: ...


class _TransitionFactory(Protocol):
    def create(self) -> _TransitionUow: ...


@dataclass(frozen=True, slots=True)
class _RecoveryMaterial:
    new_ref: SourceAssertionRef
    new_witness: StateWitness
    replacement_witness: StateWitness
    supersession_ref: AssertionHistoryFactRef
    correction_ref: AssertionHistoryFactRef | None
    recorded_at: datetime


def _result(
    outcome: SourceAssertionTransitionOutcome,
    old_ref: SourceAssertionRef | None = None,
    new_ref: SourceAssertionRef | None = None,
) -> PortSuccess[SourceAssertionTransitionResult]:
    return PortSuccess(SourceAssertionTransitionResult(outcome, old_ref, new_ref))


def _metadata(
    material: _RecoveryMaterial, operation: TechnicalOperationKey
) -> OpaqueReplayMetadata:
    entries = [
        ("new_source_assertion_ref", material.new_ref.token),
        ("new_assertion_witness", material.new_witness.value),
        ("replacement_witness", material.replacement_witness.value),
        ("supersession_history_ref", material.supersession_ref.value),
        ("recorded_at", material.recorded_at.isoformat()),
    ]
    if operation == CORRECT_OPERATION:
        entries.insert(
            4,
            (
                "correction_history_ref",
                material.correction_ref.value if material.correction_ref else "",
            ),
        )
    return OpaqueReplayMetadata(tuple(entries))


def _decode_metadata(
    mapping: RequestReferenceRecoveryMapping, operation: TechnicalOperationKey
) -> _RecoveryMaterial | None:
    if len(mapping.references) != 1 or not isinstance(mapping.references[0], SourceAssertionRef):
        return None
    entries = mapping.replay_metadata.entries
    expected = {
        "new_source_assertion_ref",
        "new_assertion_witness",
        "replacement_witness",
        "supersession_history_ref",
        "recorded_at",
    }
    if operation == CORRECT_OPERATION:
        expected.add("correction_history_ref")
    values = dict(entries)
    if len(entries) != len(expected) or len(values) != len(expected) or set(values) != expected:
        return None
    if any(not values[key] for key in expected):
        return None
    try:
        if values["new_source_assertion_ref"] != mapping.references[0].token:
            return None
        recorded_at = datetime.fromisoformat(values["recorded_at"])
        if recorded_at.tzinfo is None or recorded_at.utcoffset() != UTC.utcoffset(recorded_at):
            return None
        return _RecoveryMaterial(
            mapping.references[0],
            StateWitness(values["new_assertion_witness"]),
            StateWitness(values["replacement_witness"]),
            AssertionHistoryFactRef(values["supersession_history_ref"]),
            None
            if operation == SUPERSEDE_OPERATION
            else AssertionHistoryFactRef(values["correction_history_ref"]),
            recorded_at,
        )
    except (TypeError, ValueError):
        return None


def _mapping_conflict(
    mapping: RequestReferenceRecoveryMapping,
    key: IdempotencyBindingKey,
    intent: IntentFingerprint,
    operation: TechnicalOperationKey,
) -> SourceAssertionTransitionOutcome | None:
    if (
        mapping.client_identity != key.client_identity
        or mapping.request_identity != key.request_identity
    ):
        return SourceAssertionTransitionOutcome.RECOVERY_MAPPING_CONFLICT
    if mapping.intent_fingerprint != intent or mapping.operation_key != operation:
        return SourceAssertionTransitionOutcome.IDEMPOTENCY_CONFLICT
    return None


class _SourceAssertionTransition:
    def __init__(
        self,
        operation: TechnicalOperationKey,
        uow_factory: _TransitionFactory,
        evidence: EvidenceStore,
        recovery_gate: RecoveryGate,
        basis_codec: MutationBasisCodec,
        generator: _TransitionGenerator,
        clock: Clock,
    ) -> None:
        self._operation = operation
        self._uow_factory = uow_factory
        self._evidence = evidence
        self._gate = recovery_gate
        self._basis_codec = basis_codec
        self._generator = generator
        self._clock = clock
        self._mapping = RecoveryMappingCoordinator(evidence)
        self._reservation = ReferenceReservationCoordinator(recovery_gate, evidence)

    def execute(self, command: TransitionCommand) -> PortResult[SourceAssertionTransitionResult]:
        replay = self._committed(command)
        if isinstance(replay, PortError):
            return replay
        if replay.value is not None:
            return PortSuccess(replay.value)
        with self._uow_factory.create() as uow:
            target = uow.assertions.get_assertion(command.target_source_assertion_ref)
            if isinstance(target, PortError):
                return target
            if isinstance(target.value, RecordAbsent):
                return _result(SourceAssertionTransitionOutcome.TARGET_ASSERTION_NOT_FOUND)
            head = uow.assertions.get_standing_head(command.target_source_assertion_ref)
            if isinstance(head, PortError):
                return head
            if isinstance(head.value, RecordAbsent):
                return _result(SourceAssertionTransitionOutcome.TARGET_STANDING_HEAD_MISSING)
            history = uow.assertions.list_assertion_history(command.target_source_assertion_ref)
            if isinstance(history, PortError):
                return history
            if any(f.fact_type == SUPERSESSION_FACT_TYPE for f in history.value):
                return _result(SourceAssertionTransitionOutcome.TARGET_ALREADY_SUPERSEDED)
            basis = self._validate_basis(
                command.mutation_basis, command.target_source_assertion_ref, uow
            )
            if isinstance(basis, PortError) or basis.value is not BasisValidation.VALID:
                return self._basis_result(basis)
        recovery = self._recover(command)
        if isinstance(recovery, PortError):
            return recovery
        if isinstance(recovery.value, SourceAssertionTransitionResult):
            return PortSuccess(recovery.value)
        material = recovery.value
        reservation = self._reservation.reserve(
            ReferenceReservationPlan(command.evidence_lookup_key, (material.new_ref,))
        )
        if isinstance(reservation, PortError):
            return reservation
        if reservation.value is ReservationOutcome.BLOCKED:
            return _result(SourceAssertionTransitionOutcome.RECOVERY_NOT_READY)
        if reservation.value is ReservationOutcome.CONFLICTING_EVIDENCE:
            return _result(SourceAssertionTransitionOutcome.REFERENCE_EVIDENCE_CONFLICT)
        return self._authoritative(command, material)

    def _committed(
        self, command: TransitionCommand
    ) -> PortResult[SourceAssertionTransitionResult | None]:
        with self._uow_factory.create() as uow:
            read = uow.committed_idempotency.read(command.key)
            if isinstance(read, PortError):
                return read
            if not isinstance(read.value, CommittedBindingFound):
                return PortSuccess(None)
            binding = read.value.binding
            if (
                binding.intent_fingerprint != command.intent_fingerprint
                or binding.operation_key != self._operation
            ):
                return _result(SourceAssertionTransitionOutcome.IDEMPOTENCY_CONFLICT)
            replay = self._decode_replay(binding, command.target_source_assertion_ref)
            if replay is None:
                return _result(SourceAssertionTransitionOutcome.MALFORMED_RECOVERY_METADATA)
            return _result(SourceAssertionTransitionOutcome.REPLAY, replay[0], replay[1])

    def _decode_replay(
        self, binding: CommittedMutationBinding, old_ref: SourceAssertionRef
    ) -> tuple[SourceAssertionRef, SourceAssertionRef] | None:
        if len(binding.result.references) != 2 or binding.result.references[0] != old_ref:
            return None
        if not isinstance(binding.result.references[1], SourceAssertionRef):
            return None
        expected = "corrected" if self._operation == CORRECT_OPERATION else "superseded"
        if binding.result.replay_metadata.entries != (("result_kind", expected),):
            return None
        return old_ref, binding.result.references[1]

    def _validate_basis(
        self, token: MutationBasisToken, target_ref: SourceAssertionRef, uow: _TransitionUow
    ) -> PortResult[BasisValidation]:
        observation = self._gate.observation()
        if not observation.may_authoritative_serve:
            return PortSuccess(BasisValidation.RECOVERY_INCARNATION_MISMATCH)
        decoded = self._basis_codec.verify(token)
        if isinstance(decoded, PortError):
            return decoded
        if isinstance(decoded.value, InvalidMutationBasisToken):
            return PortSuccess(BasisValidation.INVALID_TOKEN)
        claims: MutationBasisClaims = decoded.value
        if observation.incarnation != claims.recovery_incarnation:
            return PortSuccess(BasisValidation.RECOVERY_INCARNATION_MISMATCH)
        target_owner = next(
            (item for item in claims.observed_owners if item.owner == AssertionOwner(target_ref)),
            None,
        )
        if target_owner is None or isinstance(target_owner.state, OwnerAbsent):
            return PortSuccess(BasisValidation.INSUFFICIENT_OWNER_CLAIM)
        reader = OwnerStateReader()
        for expected in claims.observed_owners:
            current = reader.read(expected.owner, uow)
            if isinstance(current, PortError):
                return current
            if current.value != expected.state:
                return PortSuccess(BasisValidation.OWNER_STATE_MISMATCH)
        return PortSuccess(BasisValidation.VALID)

    def _basis_result(
        self, basis: PortResult[BasisValidation]
    ) -> PortResult[SourceAssertionTransitionResult]:
        if isinstance(basis, PortError):
            return basis
        return _result(
            {
                BasisValidation.INVALID_TOKEN: SourceAssertionTransitionOutcome.INVALID_BASIS,
                BasisValidation.RECOVERY_INCARNATION_MISMATCH: (
                    SourceAssertionTransitionOutcome.RECOVERY_INCARNATION_MISMATCH
                ),
                BasisValidation.OWNER_STATE_MISMATCH: SourceAssertionTransitionOutcome.STALE_BASIS,
                BasisValidation.INSUFFICIENT_OWNER_CLAIM: (
                    SourceAssertionTransitionOutcome.INSUFFICIENT_BASIS
                ),
            }.get(basis.value, SourceAssertionTransitionOutcome.INVALID_BASIS)
        )

    def _recover(
        self, command: TransitionCommand
    ) -> PortResult[_RecoveryMaterial | SourceAssertionTransitionResult]:
        existing = self._evidence.read_request_mapping(command.evidence_lookup_key)
        if isinstance(existing, PortError):
            return existing
        if isinstance(existing.value, EvidenceFound):
            mapping = existing.value.record
            conflict = _mapping_conflict(
                mapping, command.key, command.intent_fingerprint, self._operation
            )
            if conflict is not None:
                return _result(conflict)
            decoded = _decode_metadata(mapping, self._operation)
            return (
                PortSuccess(decoded)
                if decoded is not None
                else _result(SourceAssertionTransitionOutcome.MALFORMED_RECOVERY_METADATA)
            )
        material = _RecoveryMaterial(
            self._generator.new_source_assertion_ref(),
            self._generator.new_state_witness(),
            self._generator.new_state_witness(),
            self._generator.new_assertion_history_fact_ref(),
            self._generator.new_assertion_history_fact_ref()
            if self._operation == CORRECT_OPERATION
            else None,
            self._clock.now(),
        )
        proposal = RequestReferenceRecoveryMapping(
            command.key.client_identity,
            command.key.request_identity,
            command.intent_fingerprint,
            self._operation,
            (material.new_ref,),
            _metadata(material, self._operation),
        )
        resolved = self._mapping.resolve(command.evidence_lookup_key, proposal)
        if isinstance(resolved, PortError):
            return resolved
        if resolved.value.outcome is RecoveryMappingOutcome.CONFLICT:
            current = self._evidence.read_request_mapping(command.evidence_lookup_key)
            if isinstance(current, PortError):
                return current
            if not isinstance(current.value, EvidenceFound):
                return _result(SourceAssertionTransitionOutcome.RECOVERY_MAPPING_CONFLICT)
            mapping = current.value.record
            conflict = _mapping_conflict(
                mapping, command.key, command.intent_fingerprint, self._operation
            )
            if conflict is not None:
                return _result(conflict)
            decoded = _decode_metadata(mapping, self._operation)
            return (
                PortSuccess(decoded)
                if decoded is not None
                else _result(SourceAssertionTransitionOutcome.MALFORMED_RECOVERY_METADATA)
            )
        mapping = resolved.value.mapping
        decoded = _decode_metadata(mapping, self._operation) if mapping is not None else None
        return (
            PortSuccess(decoded)
            if decoded is not None
            else _result(SourceAssertionTransitionOutcome.MALFORMED_RECOVERY_METADATA)
        )

    def _authoritative(
        self, command: TransitionCommand, material: _RecoveryMaterial
    ) -> PortResult[SourceAssertionTransitionResult]:
        with self._uow_factory.create() as uow:
            replay = self._read_binding_in_uow(command, uow)
            if isinstance(replay, PortError):
                return replay
            if replay.value is not None:
                return PortSuccess(replay.value)
            target = uow.assertions.get_assertion(command.target_source_assertion_ref)
            if isinstance(target, PortError):
                uow.rollback()
                return target
            if isinstance(target.value, RecordAbsent):
                uow.rollback()
                return _result(SourceAssertionTransitionOutcome.TARGET_ASSERTION_NOT_FOUND)
            head = uow.assertions.get_standing_head(command.target_source_assertion_ref)
            if isinstance(head, PortError):
                uow.rollback()
                return head
            if isinstance(head.value, RecordAbsent):
                uow.rollback()
                return _result(SourceAssertionTransitionOutcome.TARGET_STANDING_HEAD_MISSING)
            history = uow.assertions.list_assertion_history(command.target_source_assertion_ref)
            if isinstance(history, PortError):
                uow.rollback()
                return history
            if any(f.fact_type == SUPERSESSION_FACT_TYPE for f in history.value):
                uow.rollback()
                return _result(SourceAssertionTransitionOutcome.TARGET_ALREADY_SUPERSEDED)
            basis = self._validate_basis(
                command.mutation_basis, command.target_source_assertion_ref, uow
            )
            if isinstance(basis, PortError) or basis.value is not BasisValidation.VALID:
                uow.rollback()
                return self._basis_result(basis)
            read_set = AuthoritativeReadSetCapture(OwnerStateReader()).capture(
                (AssertionOwner(command.target_source_assertion_ref),), uow
            )
            if isinstance(read_set, PortError):
                uow.rollback()
                return read_set
            current = read_set.value.observed_owners[0].state
            if not isinstance(current, OwnerPresent):
                uow.rollback()
                return _result(SourceAssertionTransitionOutcome.TARGET_STANDING_HEAD_MISSING)
            old = target.value.record
            new = SourceAssertionRecord(
                material.new_ref,
                old.place_ref,
                old.fact_purpose,
                command.value,
                command.scope,
                command.source_provenance,
                command.quality,
                material.recorded_at,
            )
            inserted = uow.assertions.insert_assertion_if_absent(new)
            if isinstance(inserted, PortError):
                uow.rollback()
                return inserted
            if inserted.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(SourceAssertionTransitionOutcome.REFERENCE_COLLISION)
            headed = uow.assertions.insert_standing_head_if_absent(
                AssertionStandingHead(material.new_ref, None, material.new_witness)
            )
            if isinstance(headed, PortError):
                uow.rollback()
                return headed
            if headed.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(SourceAssertionTransitionOutcome.REFERENCE_COLLISION)
            history_fact = AssertionHistoryFact(
                material.supersession_ref,
                command.target_source_assertion_ref,
                SUPERSESSION_FACT_TYPE,
                material.recorded_at,
                material.new_ref,
                command.mutation_provenance,
            )
            added = uow.assertions.append_assertion_history_if_absent(history_fact)
            if isinstance(added, PortError):
                uow.rollback()
                return added
            if added.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(SourceAssertionTransitionOutcome.HISTORY_CONFLICT)
            latest = material.supersession_ref
            if self._operation == CORRECT_OPERATION:
                assert material.correction_ref is not None
                correction = AssertionHistoryFact(
                    material.correction_ref,
                    command.target_source_assertion_ref,
                    CORRECTION_FACT_TYPE,
                    material.recorded_at,
                    material.new_ref,
                    command.mutation_provenance,
                )
                corrected = uow.assertions.append_assertion_history_if_absent(correction)
                if isinstance(corrected, PortError):
                    uow.rollback()
                    return corrected
                if corrected.value is InsertDisposition.CONFLICTING_EXISTING:
                    uow.rollback()
                    return _result(SourceAssertionTransitionOutcome.HISTORY_CONFLICT)
                latest = material.correction_ref
            revalidated = ReadSetRevalidator(OwnerStateReader()).revalidate(read_set.value, uow)
            if isinstance(revalidated, PortError):
                uow.rollback()
                return revalidated
            if revalidated.value is not ReadSetValidation.VALID:
                uow.rollback()
                return _result(SourceAssertionTransitionOutcome.STALE_BASIS)
            cas = uow.assertions.compare_and_swap_standing_head(
                command.target_source_assertion_ref,
                current.witness,
                latest,
                material.replacement_witness,
            )
            if isinstance(cas, PortError):
                uow.rollback()
                return cas
            if cas.value is not ConditionalWriteDisposition.APPLIED:
                uow.rollback()
                return _result(SourceAssertionTransitionOutcome.STANDING_HEAD_CONFLICT)
            details = OpaqueEncodedPayload(
                "daen.step10.audit.v1",
                json.dumps(
                    {
                        "kind": "correct" if self._operation == CORRECT_OPERATION else "supersede",
                        "old": command.target_source_assertion_ref.token,
                        "new": material.new_ref.token,
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode(),
            )
            audited = uow.mutation_audit.append_if_absent(
                MutationAuditRecord(
                    command.key,
                    command.intent_fingerprint,
                    self._operation,
                    material.recorded_at,
                    command.mutation_provenance,
                    details,
                )
            )
            if isinstance(audited, PortError):
                uow.rollback()
                return audited
            if audited.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(SourceAssertionTransitionOutcome.AUDIT_CONFLICT)
            binding = CommittedMutationBinding(
                command.key,
                command.intent_fingerprint,
                self._operation,
                CommittedMutationResult(
                    (command.target_source_assertion_ref, material.new_ref),
                    OpaqueReplayMetadata(
                        (
                            (
                                "result_kind",
                                "corrected"
                                if self._operation == CORRECT_OPERATION
                                else "superseded",
                            ),
                        )
                    ),
                ),
                BindingRetention.PUBLIC_REPLAY_HORIZON,
            )
            created = uow.committed_idempotency.create_if_absent(binding)
            if isinstance(created, PortError):
                uow.rollback()
                return created
            if created.value is IdempotencyCreateDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(SourceAssertionTransitionOutcome.IDEMPOTENCY_CONFLICT)
            outcome = uow.commit()
            if isinstance(outcome, CommitAccepted):
                return _result(
                    SourceAssertionTransitionOutcome.APPLIED,
                    command.target_source_assertion_ref,
                    material.new_ref,
                )
            if isinstance(outcome, CommitNotCommitted):
                return _result(SourceAssertionTransitionOutcome.NOT_COMMITTED)
            return _result(SourceAssertionTransitionOutcome.COMMIT_OUTCOME_UNKNOWN)

    def _read_binding_in_uow(
        self, command: TransitionCommand, uow: _TransitionUow
    ) -> PortResult[SourceAssertionTransitionResult | None]:
        read = uow.committed_idempotency.read(command.key)
        if isinstance(read, PortError):
            return read
        if not isinstance(read.value, CommittedBindingFound):
            return PortSuccess(None)
        binding = read.value.binding
        if (
            binding.intent_fingerprint != command.intent_fingerprint
            or binding.operation_key != self._operation
        ):
            return _result(SourceAssertionTransitionOutcome.IDEMPOTENCY_CONFLICT)
        replay = self._decode_replay(binding, command.target_source_assertion_ref)
        return (
            _result(SourceAssertionTransitionOutcome.REPLAY, *replay)
            if replay
            else _result(SourceAssertionTransitionOutcome.MALFORMED_RECOVERY_METADATA)
        )


class SupersedeSourceAssertion(_SourceAssertionTransition):
    def __init__(
        self,
        uow_factory: _TransitionFactory,
        evidence: EvidenceStore,
        recovery_gate: RecoveryGate,
        basis_codec: MutationBasisCodec,
        generator: _TransitionGenerator,
        clock: Clock,
    ):
        super().__init__(
            SUPERSEDE_OPERATION, uow_factory, evidence, recovery_gate, basis_codec, generator, clock
        )


class CorrectSourceAssertion(_SourceAssertionTransition):
    def __init__(
        self,
        uow_factory: _TransitionFactory,
        evidence: EvidenceStore,
        recovery_gate: RecoveryGate,
        basis_codec: MutationBasisCodec,
        generator: _TransitionGenerator,
        clock: Clock,
    ):
        super().__init__(
            CORRECT_OPERATION, uow_factory, evidence, recovery_gate, basis_codec, generator, clock
        )
