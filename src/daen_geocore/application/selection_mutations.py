from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol, cast

from daen_geocore.application.mutation_runtime import (
    AuthoritativeReadSetCapture,
    MutationBasisClaims,
    MutationBasisCodec,
    ReadSetRevalidator,
    ReadSetValidation,
    RecoveryMappingCoordinator,
    RecoveryMappingOutcome,
    ReferenceReservationCoordinator,
    ReferenceReservationPlan,
    ReservationOutcome,
)
from daen_geocore.domain.references import PlaceRef, SelectionRecordRef, SourceAssertionRef
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
    MutationBasisToken,
    MutationOwner,
    OwnerAbsent,
    OwnerPresent,
    OwnerStateReader,
    SelectionSlotOwner,
)
from daen_geocore.ports.persistence.commit import CommitAccepted, CommitNotCommitted, CommitOutcome
from daen_geocore.ports.persistence.records import (
    ConditionalWriteDisposition,
    InsertDisposition,
    OpaqueEncodedPayload,
    PersistedExplicitScope,
    PersistedQuality,
    PersistedTypedValue,
    RecordAbsent,
    RecordFound,
    SelectionRecord,
    SelectionSlotHead,
    SelectionSlotKey,
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

ADD_OPERATION = TechnicalOperationKey("selection.add")
REPLACE_OPERATION = TechnicalOperationKey("selection.replace")
WITHDRAWN_FACT_TYPE = "source_assertion.withdrawn"
SUPERSESSION_FACT_TYPE = "source_assertion.superseded_by"
_AUDIT_ENCODING = "daen.step12.audit.v1"


@dataclass(frozen=True, slots=True)
class AddSelectionCommand:
    key: IdempotencyBindingKey
    evidence_lookup_key: EvidenceLookupKey
    intent_fingerprint: IntentFingerprint
    place_ref: PlaceRef
    fact_purpose: str
    mutation_basis: MutationBasisToken
    scope: PersistedExplicitScope
    value: PersistedTypedValue
    supporting_assertion_refs: tuple[SourceAssertionRef, ...]
    attribution: OpaqueEncodedPayload
    provenance: OpaqueEncodedPayload
    quality: PersistedQuality
    mutation_provenance: OpaqueEncodedPayload


@dataclass(frozen=True, slots=True)
class ReplaceSelectionCommand:
    key: IdempotencyBindingKey
    evidence_lookup_key: EvidenceLookupKey
    intent_fingerprint: IntentFingerprint
    place_ref: PlaceRef
    prior_selection_record_ref: SelectionRecordRef
    fact_purpose: str
    mutation_basis: MutationBasisToken
    scope: PersistedExplicitScope
    value: PersistedTypedValue
    supporting_assertion_refs: tuple[SourceAssertionRef, ...]
    attribution: OpaqueEncodedPayload
    provenance: OpaqueEncodedPayload
    quality: PersistedQuality
    mutation_provenance: OpaqueEncodedPayload


class SelectionMutationOutcome(StrEnum):
    APPLIED = "applied"
    REPLAY = "replay"
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"
    TARGET_PLACE_NOT_FOUND = "target_place_not_found"
    SUPPORTING_ASSERTIONS_REQUIRED = "supporting_assertions_required"
    SUPPORT_ASSERTION_NOT_FOUND = "support_assertion_not_found"
    SUPPORT_ASSERTION_PLACE_MISMATCH = "support_assertion_place_mismatch"
    SUPPORT_ASSERTION_WITHDRAWN = "support_assertion_withdrawn"
    SUPPORT_STANDING_HEAD_MISSING = "support_standing_head_missing"
    SCOPE_EQUALITY_UNESTABLISHED = "scope_equality_unestablished"
    INSUFFICIENT_BASIS = "insufficient_basis"
    INVALID_BASIS = "invalid_basis"
    RECOVERY_NOT_READY = "recovery_not_ready"
    RECOVERY_INCARNATION_MISMATCH = "recovery_incarnation_mismatch"
    STALE_SLOT_BASIS = "stale_slot_basis"
    PRIOR_SELECTION_NOT_FOUND = "prior_selection_not_found"
    PRIOR_SELECTION_NOT_CURRENT = "prior_selection_not_current"
    CURRENT_SELECTION_MISSING = "current_selection_missing"
    PLACE_INVARIANT_FAILED = "place_invariant_failed"
    FACT_PURPOSE_INVARIANT_FAILED = "fact_purpose_invariant_failed"
    SCOPE_INVARIANT_FAILED = "scope_invariant_failed"
    RECOVERY_MAPPING_CONFLICT = "recovery_mapping_conflict"
    MALFORMED_RECOVERY_METADATA = "malformed_recovery_metadata"
    REFERENCE_EVIDENCE_CONFLICT = "reference_evidence_conflict"
    REFERENCE_COLLISION = "reference_collision"
    SUPPORT_ASSERTION_STATE_CHANGED = "support_assertion_state_changed"
    SLOT_CONFLICT = "slot_conflict"
    AUDIT_CONFLICT = "audit_conflict"
    NOT_COMMITTED = "not_committed"
    COMMIT_OUTCOME_UNKNOWN = "commit_outcome_unknown"


@dataclass(frozen=True, slots=True)
class SelectionMutationResult:
    outcome: SelectionMutationOutcome
    selection_record_ref: SelectionRecordRef | None = None
    prior_selection_record_ref: SelectionRecordRef | None = None


class _SelectionGenerator(ReferenceCandidateGenerator, StateWitnessGenerator, Protocol):
    pass


class _SelectionUow(Protocol):
    identity: IdentityRepository
    assertions: AssertionsRepository
    representation: RepresentationRepository
    committed_idempotency: CommittedIdempotencyStore
    mutation_audit: MutationAuditStore

    def __enter__(self) -> _SelectionUow: ...
    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: ...
    def commit(self) -> CommitOutcome: ...
    def rollback(self) -> None: ...


class _SelectionFactory(Protocol):
    def create(self) -> _SelectionUow: ...


def _result(
    outcome: SelectionMutationOutcome,
    ref: SelectionRecordRef | None = None,
    prior: SelectionRecordRef | None = None,
) -> PortSuccess[SelectionMutationResult]:
    return PortSuccess(SelectionMutationResult(outcome, ref, prior))


def _slot(
    place: PlaceRef, purpose: str, scope: PersistedExplicitScope | object
) -> SelectionSlotKey | None:
    if not isinstance(scope, PersistedExplicitScope) or scope.equality_key is None:
        return None
    return SelectionSlotKey(place, purpose, scope.type_id, scope.equality_key)


def _metadata(witness: StateWitness, recorded_at: datetime) -> OpaqueReplayMetadata:
    return OpaqueReplayMetadata(
        (("state_witness", witness.value), ("recorded_at", recorded_at.isoformat()))
    )


def _decode_mapping(
    mapping: RequestReferenceRecoveryMapping,
) -> tuple[SelectionRecordRef, StateWitness, datetime] | None:
    if len(mapping.references) != 1 or not isinstance(mapping.references[0], SelectionRecordRef):
        return None
    raw_entries = mapping.replay_metadata.entries
    values = dict(raw_entries)
    if (
        len(raw_entries) != 2
        or len(values) != 2
        or set(values) != {"state_witness", "recorded_at"}
        or not values["state_witness"]
        or not values["recorded_at"]
    ):
        return None
    try:
        recorded = datetime.fromisoformat(values["recorded_at"])
    except (TypeError, ValueError):
        return None
    if recorded.tzinfo is None or recorded.utcoffset() != UTC.utcoffset(recorded):
        return None
    return mapping.references[0], StateWitness(values["state_witness"]), recorded


def _audit(
    command: AddSelectionCommand | ReplaceSelectionCommand,
    operation: TechnicalOperationKey,
    ref: SelectionRecordRef,
) -> OpaqueEncodedPayload:
    body = {
        "kind": "selection_add" if operation == ADD_OPERATION else "selection_replace",
        "place_ref": command.place_ref.token,
        "fact_purpose": command.fact_purpose,
        "selection_record_ref": ref.token,
        "supporting_assertion_refs": [item.token for item in command.supporting_assertion_refs],
    }
    if isinstance(command, ReplaceSelectionCommand):
        body["prior_selection_record_ref"] = command.prior_selection_record_ref.token
    return OpaqueEncodedPayload(
        _AUDIT_ENCODING, json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    )


class _SelectionMutation:
    operation: TechnicalOperationKey

    def __init__(
        self,
        factory: _SelectionFactory,
        evidence: EvidenceStore,
        gate: RecoveryGate,
        codec: MutationBasisCodec,
        generator: _SelectionGenerator,
        clock: Clock,
    ) -> None:
        self._factory, self._evidence, self._gate = factory, evidence, gate
        self._codec, self._generator, self._clock = codec, generator, clock
        self._mapping = RecoveryMappingCoordinator(evidence)
        self._reservation = ReferenceReservationCoordinator(gate, evidence)

    def execute(
        self, command: AddSelectionCommand | ReplaceSelectionCommand
    ) -> PortResult[SelectionMutationResult]:
        preflight = self._preflight(command)
        if isinstance(preflight, PortError) or preflight.value is not None:
            return cast(PortResult[SelectionMutationResult], preflight)
        recovered = self._recover(command)
        if isinstance(recovered, PortError) or isinstance(recovered.value, SelectionMutationResult):
            return cast(PortResult[SelectionMutationResult], recovered)
        ref, witness, recorded = recovered.value
        reservation = self._reservation.reserve(
            ReferenceReservationPlan(command.evidence_lookup_key, (ref,))
        )
        if isinstance(reservation, PortError):
            return reservation
        if reservation.value is ReservationOutcome.BLOCKED:
            return _result(SelectionMutationOutcome.RECOVERY_NOT_READY)
        if reservation.value is ReservationOutcome.CONFLICTING_EVIDENCE:
            return _result(SelectionMutationOutcome.REFERENCE_EVIDENCE_CONFLICT)
        return self._authoritative(command, ref, witness, recorded)

    def _preflight(
        self, command: AddSelectionCommand | ReplaceSelectionCommand
    ) -> PortResult[SelectionMutationResult | None]:
        with self._factory.create() as uow:
            replay = self._replay(uow, command)
            if isinstance(replay, PortError) or replay.value is not None:
                return replay
            scope = _slot(command.place_ref, command.fact_purpose, command.scope)
            if scope is None:
                return _result(SelectionMutationOutcome.SCOPE_EQUALITY_UNESTABLISHED)
            if not command.supporting_assertion_refs:
                return _result(SelectionMutationOutcome.SUPPORTING_ASSERTIONS_REQUIRED)
            place = uow.identity.get_place(command.place_ref)
            if isinstance(place, PortError):
                return place
            if isinstance(place.value, RecordAbsent):
                return _result(SelectionMutationOutcome.TARGET_PLACE_NOT_FOUND)
            basis = self._basis(
                command.mutation_basis, scope, uow, isinstance(command, ReplaceSelectionCommand)
            )
            if basis is not None:
                return basis
            if isinstance(command, ReplaceSelectionCommand):
                prior = uow.representation.get_selection_record(command.prior_selection_record_ref)
                if isinstance(prior, PortError):
                    return prior
                if isinstance(prior.value, RecordAbsent):
                    return _result(SelectionMutationOutcome.PRIOR_SELECTION_NOT_FOUND)
                record = prior.value.record
                if record.place_ref != command.place_ref:
                    return _result(SelectionMutationOutcome.PLACE_INVARIANT_FAILED)
                if record.fact_purpose != command.fact_purpose:
                    return _result(SelectionMutationOutcome.FACT_PURPOSE_INVARIANT_FAILED)
                old_slot = (
                    _slot(record.place_ref, record.fact_purpose, record.scope)
                    if isinstance(record.scope, PersistedExplicitScope)
                    else None
                )
                if old_slot != scope:
                    return _result(SelectionMutationOutcome.SCOPE_INVARIANT_FAILED)
                head = uow.representation.get_selection_slot_head(scope)
                if isinstance(head, PortError):
                    return head
                if isinstance(head.value, RecordAbsent):
                    return _result(SelectionMutationOutcome.CURRENT_SELECTION_MISSING)
                if head.value.record.selection_record_ref != command.prior_selection_record_ref:
                    return _result(SelectionMutationOutcome.PRIOR_SELECTION_NOT_CURRENT)
            else:
                head = uow.representation.get_selection_slot_head(scope)
                if isinstance(head, PortError):
                    return head
                if isinstance(head.value, RecordFound):
                    return _result(SelectionMutationOutcome.STALE_SLOT_BASIS)
            support = self._validate_supports(uow, command)
            if support is not None:
                return support
        return PortSuccess(None)

    def _basis(
        self,
        token: MutationBasisToken,
        scope: SelectionSlotKey,
        uow: _SelectionUow,
        replace: bool,
    ) -> PortResult[SelectionMutationResult] | None:
        observation = self._gate.observation()
        if not observation.may_authoritative_serve:
            return _result(SelectionMutationOutcome.RECOVERY_NOT_READY)
        serving = self._gate.validate_before_authoritative_serving()
        if isinstance(serving, PortError):
            return serving
        if serving.value != observation.incarnation:
            return _result(SelectionMutationOutcome.RECOVERY_INCARNATION_MISMATCH)
        decoded = self._codec.verify(token)
        if not isinstance(decoded, PortSuccess):
            return decoded
        if not isinstance(decoded.value, MutationBasisClaims):
            return _result(SelectionMutationOutcome.INVALID_BASIS)
        if observation.incarnation != decoded.value.recovery_incarnation:
            return _result(SelectionMutationOutcome.RECOVERY_INCARNATION_MISMATCH)
        claims = decoded.value.observed_owners
        expected = OwnerPresent if replace else OwnerAbsent
        exact = [
            claim
            for claim in claims
            if isinstance(claim.owner, SelectionSlotOwner) and claim.owner.slot == scope
        ]
        if len(exact) != 1 or type(exact[0].state) is not expected:
            return _result(SelectionMutationOutcome.INSUFFICIENT_BASIS)
        current = OwnerStateReader().read(exact[0].owner, uow)
        if isinstance(current, PortError):
            return current
        if current.value != exact[0].state:
            return _result(SelectionMutationOutcome.STALE_SLOT_BASIS)
        return None

    def _validate_supports(
        self, uow: _SelectionUow, command: AddSelectionCommand | ReplaceSelectionCommand
    ) -> PortResult[SelectionMutationResult] | None:
        for ref in command.supporting_assertion_refs:
            assertion = uow.assertions.get_assertion(ref)
            if isinstance(assertion, PortError):
                return assertion
            if isinstance(assertion.value, RecordAbsent):
                return _result(SelectionMutationOutcome.SUPPORT_ASSERTION_NOT_FOUND)
            record: SourceAssertionRecord = assertion.value.record
            if record.place_ref != command.place_ref:
                return _result(SelectionMutationOutcome.SUPPORT_ASSERTION_PLACE_MISMATCH)
            history = uow.assertions.list_assertion_history(ref)
            if isinstance(history, PortError):
                return history
            if any(fact.fact_type == WITHDRAWN_FACT_TYPE for fact in history.value):
                return _result(SelectionMutationOutcome.SUPPORT_ASSERTION_WITHDRAWN)
            head = uow.assertions.get_standing_head(ref)
            if isinstance(head, PortError):
                return head
            if isinstance(head.value, RecordAbsent):
                return _result(SelectionMutationOutcome.SUPPORT_STANDING_HEAD_MISSING)
        return None

    def _replay(
        self, uow: _SelectionUow, command: AddSelectionCommand | ReplaceSelectionCommand
    ) -> PortResult[SelectionMutationResult | None]:
        result = uow.committed_idempotency.read(command.key)
        if isinstance(result, PortError):
            return result
        if not isinstance(result.value, CommittedBindingFound):
            return PortSuccess(None)
        binding = result.value.binding
        if (
            binding.intent_fingerprint != command.intent_fingerprint
            or binding.operation_key != self.operation
        ):
            return _result(SelectionMutationOutcome.IDEMPOTENCY_CONFLICT)
        expected = 1 if self.operation == ADD_OPERATION else 2
        if len(binding.result.references) != expected or not all(
            isinstance(item, SelectionRecordRef) for item in binding.result.references
        ):
            return _result(SelectionMutationOutcome.MALFORMED_RECOVERY_METADATA)
        kind = "selection_added" if self.operation == ADD_OPERATION else "selection_replaced"
        if binding.result.replay_metadata.entries != (("result_kind", kind),):
            return _result(SelectionMutationOutcome.MALFORMED_RECOVERY_METADATA)
        if (
            self.operation == REPLACE_OPERATION
            and isinstance(command, ReplaceSelectionCommand)
            and binding.result.references[0] != command.prior_selection_record_ref
        ):
            return _result(SelectionMutationOutcome.MALFORMED_RECOVERY_METADATA)
        prior = (
            cast(SelectionRecordRef, binding.result.references[0])
            if self.operation == REPLACE_OPERATION
            else None
        )
        ref = cast(SelectionRecordRef, binding.result.references[-1])
        return _result(SelectionMutationOutcome.REPLAY, ref, prior)

    def _recover(
        self, command: AddSelectionCommand | ReplaceSelectionCommand
    ) -> PortResult[SelectionMutationResult | tuple[SelectionRecordRef, StateWitness, datetime]]:
        existing = self._evidence.read_request_mapping(command.evidence_lookup_key)
        if isinstance(existing, PortError):
            return existing
        if isinstance(existing.value, EvidenceFound):
            mapping = existing.value.record
            if (
                mapping.client_identity != command.key.client_identity
                or mapping.request_identity != command.key.request_identity
            ):
                return _result(SelectionMutationOutcome.RECOVERY_MAPPING_CONFLICT)
            if (
                mapping.intent_fingerprint != command.intent_fingerprint
                or mapping.operation_key != self.operation
            ):
                return _result(SelectionMutationOutcome.IDEMPOTENCY_CONFLICT)
            decoded = _decode_mapping(mapping)
            return (
                PortSuccess(decoded)
                if decoded
                else _result(SelectionMutationOutcome.MALFORMED_RECOVERY_METADATA)
            )
        ref = self._generator.new_selection_record_ref()
        witness = self._generator.new_state_witness()
        recorded = self._clock.now()
        proposal = RequestReferenceRecoveryMapping(
            command.key.client_identity,
            command.key.request_identity,
            command.intent_fingerprint,
            self.operation,
            (ref,),
            _metadata(witness, recorded),
        )
        resolved = self._mapping.resolve(command.evidence_lookup_key, proposal)
        if isinstance(resolved, PortError):
            return resolved
        if resolved.value.outcome is RecoveryMappingOutcome.CONFLICT:
            current = self._evidence.read_request_mapping(command.evidence_lookup_key)
            if isinstance(current, PortError):
                return current
            if not isinstance(current.value, EvidenceFound):
                return _result(SelectionMutationOutcome.RECOVERY_MAPPING_CONFLICT)
            stored = current.value.record
            if (
                stored.client_identity == command.key.client_identity
                and stored.request_identity == command.key.request_identity
            ):
                if (
                    stored.intent_fingerprint != command.intent_fingerprint
                    or stored.operation_key != self.operation
                ):
                    return _result(SelectionMutationOutcome.IDEMPOTENCY_CONFLICT)
                decoded = _decode_mapping(stored)
                return (
                    PortSuccess(decoded)
                    if decoded is not None
                    else _result(SelectionMutationOutcome.MALFORMED_RECOVERY_METADATA)
                )
            return _result(SelectionMutationOutcome.RECOVERY_MAPPING_CONFLICT)
        mapping = resolved.value.mapping
        decoded = _decode_mapping(mapping) if mapping else None
        return (
            PortSuccess(decoded)
            if decoded
            else _result(SelectionMutationOutcome.MALFORMED_RECOVERY_METADATA)
        )

    def _authoritative(
        self,
        command: AddSelectionCommand | ReplaceSelectionCommand,
        ref: SelectionRecordRef,
        witness: StateWitness,
        recorded: datetime,
    ) -> PortResult[SelectionMutationResult]:
        with self._factory.create() as uow:
            replay = self._replay(uow, command)
            if isinstance(replay, PortError) or replay.value is not None:
                uow.rollback()
                return cast(PortResult[SelectionMutationResult], replay)
            scope = _slot(command.place_ref, command.fact_purpose, command.scope)
            if scope is None:
                uow.rollback()
                return _result(SelectionMutationOutcome.SCOPE_EQUALITY_UNESTABLISHED)
            place = uow.identity.get_place(command.place_ref)
            if isinstance(place, PortError):
                uow.rollback()
                return place
            if isinstance(place.value, RecordAbsent):
                uow.rollback()
                return _result(SelectionMutationOutcome.TARGET_PLACE_NOT_FOUND)
            basis = self._basis(
                command.mutation_basis, scope, uow, isinstance(command, ReplaceSelectionCommand)
            )
            if basis is not None:
                uow.rollback()
                return basis
            if isinstance(command, ReplaceSelectionCommand):
                prior = uow.representation.get_selection_record(command.prior_selection_record_ref)
                if isinstance(prior, PortError):
                    uow.rollback()
                    return prior
                if isinstance(prior.value, RecordAbsent):
                    uow.rollback()
                    return _result(SelectionMutationOutcome.PRIOR_SELECTION_NOT_FOUND)
                prior_record = prior.value.record
                if prior_record.place_ref != command.place_ref:
                    uow.rollback()
                    return _result(SelectionMutationOutcome.PLACE_INVARIANT_FAILED)
                if prior_record.fact_purpose != command.fact_purpose:
                    uow.rollback()
                    return _result(SelectionMutationOutcome.FACT_PURPOSE_INVARIANT_FAILED)
                prior_scope = (
                    _slot(prior_record.place_ref, prior_record.fact_purpose, prior_record.scope)
                    if isinstance(prior_record.scope, PersistedExplicitScope)
                    else None
                )
                if prior_scope != scope:
                    uow.rollback()
                    return _result(SelectionMutationOutcome.SCOPE_INVARIANT_FAILED)
                head = uow.representation.get_selection_slot_head(scope)
                if isinstance(head, PortError):
                    uow.rollback()
                    return head
                if (
                    isinstance(head.value, RecordAbsent)
                    or head.value.record.selection_record_ref != command.prior_selection_record_ref
                ):
                    uow.rollback()
                    return _result(SelectionMutationOutcome.PRIOR_SELECTION_NOT_CURRENT)
                expected = head.value.record.state_witness
            else:
                head = uow.representation.get_selection_slot_head(scope)
                if isinstance(head, PortError):
                    uow.rollback()
                    return head
                if isinstance(head.value, RecordFound):
                    uow.rollback()
                    return _result(SelectionMutationOutcome.STALE_SLOT_BASIS)
                expected = None
            support = self._validate_supports(uow, command)
            if support is not None:
                uow.rollback()
                return support
            owners: tuple[MutationOwner, ...] = (SelectionSlotOwner(scope),) + tuple(
                AssertionOwner(item) for item in command.supporting_assertion_refs
            )
            captured = AuthoritativeReadSetCapture(OwnerStateReader()).capture(owners, uow)
            if isinstance(captured, PortError):
                uow.rollback()
                return captured
            record = SelectionRecord(
                ref,
                command.place_ref,
                command.fact_purpose,
                command.value,
                command.scope,
                command.attribution,
                command.provenance,
                command.quality,
                recorded,
            )
            inserted = uow.representation.insert_selection_record_if_absent(record)
            if isinstance(inserted, PortError):
                uow.rollback()
                return inserted
            if inserted.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(SelectionMutationOutcome.REFERENCE_COLLISION)
            for support_ref in command.supporting_assertion_refs:
                linked = uow.representation.insert_support_link_if_absent(ref, support_ref)
                if isinstance(linked, PortError):
                    uow.rollback()
                    return linked
                if linked.value is InsertDisposition.CONFLICTING_EXISTING:
                    uow.rollback()
                    return _result(SelectionMutationOutcome.REFERENCE_COLLISION)
            valid = ReadSetRevalidator(OwnerStateReader()).revalidate(captured.value, uow)
            if isinstance(valid, PortError):
                uow.rollback()
                return valid
            if valid.value is not ReadSetValidation.VALID:
                for observed in captured.value.observed_owners:
                    if isinstance(observed.owner, SelectionSlotOwner):
                        current_slot = uow.representation.get_selection_slot_head(
                            observed.owner.slot
                        )
                        if isinstance(current_slot, PortError):
                            uow.rollback()
                            return current_slot
                        current_state = (
                            OwnerAbsent()
                            if isinstance(current_slot.value, RecordAbsent)
                            else OwnerPresent(current_slot.value.record.state_witness)
                        )
                        if current_state != observed.state:
                            uow.rollback()
                            return _result(SelectionMutationOutcome.STALE_SLOT_BASIS)
                    elif isinstance(observed.owner, AssertionOwner):
                        history = uow.assertions.list_assertion_history(
                            observed.owner.source_assertion_ref
                        )
                        if isinstance(history, PortError):
                            uow.rollback()
                            return history
                        if any(fact.fact_type == WITHDRAWN_FACT_TYPE for fact in history.value):
                            uow.rollback()
                            return _result(SelectionMutationOutcome.SUPPORT_ASSERTION_WITHDRAWN)
                        head = uow.assertions.get_standing_head(observed.owner.source_assertion_ref)
                        if isinstance(head, PortError):
                            uow.rollback()
                            return head
                        if isinstance(head.value, RecordAbsent):
                            uow.rollback()
                            return _result(SelectionMutationOutcome.SUPPORT_STANDING_HEAD_MISSING)
                uow.rollback()
                return _result(SelectionMutationOutcome.SUPPORT_ASSERTION_STATE_CHANGED)
            if isinstance(command, AddSelectionCommand):
                write = uow.representation.insert_selection_slot_head_if_absent(
                    SelectionSlotHead(scope, ref, witness)
                )
                if isinstance(write, PortError):
                    uow.rollback()
                    return write
                if write.value is InsertDisposition.CONFLICTING_EXISTING:
                    uow.rollback()
                    return _result(SelectionMutationOutcome.SLOT_CONFLICT)
            else:
                if expected is None:
                    uow.rollback()
                    return _result(SelectionMutationOutcome.CURRENT_SELECTION_MISSING)
                write = uow.representation.compare_and_swap_selection_slot_head(
                    scope, command.prior_selection_record_ref, expected, ref, witness
                )
                if isinstance(write, PortError):
                    uow.rollback()
                    return write
                if write.value is ConditionalWriteDisposition.PRECONDITION_NOT_MET:
                    uow.rollback()
                    return _result(SelectionMutationOutcome.STALE_SLOT_BASIS)
            audited = uow.mutation_audit.append_if_absent(
                MutationAuditRecord(
                    command.key,
                    command.intent_fingerprint,
                    self.operation,
                    recorded,
                    command.mutation_provenance,
                    _audit(command, self.operation, ref),
                )
            )
            if isinstance(audited, PortError):
                uow.rollback()
                return audited
            if audited.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(SelectionMutationOutcome.AUDIT_CONFLICT)
            refs = (
                (ref,)
                if isinstance(command, AddSelectionCommand)
                else (command.prior_selection_record_ref, ref)
            )
            kind = (
                "selection_added"
                if isinstance(command, AddSelectionCommand)
                else "selection_replaced"
            )
            binding = CommittedMutationBinding(
                command.key,
                command.intent_fingerprint,
                self.operation,
                CommittedMutationResult(refs, OpaqueReplayMetadata((("result_kind", kind),))),
                BindingRetention.PUBLIC_REPLAY_HORIZON,
            )
            committed = uow.committed_idempotency.create_if_absent(binding)
            if isinstance(committed, PortError):
                uow.rollback()
                return committed
            if committed.value is IdempotencyCreateDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(SelectionMutationOutcome.IDEMPOTENCY_CONFLICT)
            outcome = uow.commit()
            if isinstance(outcome, CommitAccepted):
                return _result(
                    SelectionMutationOutcome.APPLIED,
                    ref,
                    command.prior_selection_record_ref
                    if isinstance(command, ReplaceSelectionCommand)
                    else None,
                )
            if isinstance(outcome, CommitNotCommitted):
                return _result(SelectionMutationOutcome.NOT_COMMITTED)
            return _result(SelectionMutationOutcome.COMMIT_OUTCOME_UNKNOWN)


class AddSelection(_SelectionMutation):
    operation = ADD_OPERATION


class ReplaceSelection(_SelectionMutation):
    operation = REPLACE_OPERATION
