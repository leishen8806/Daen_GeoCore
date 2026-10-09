from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol, cast

from daen_geocore.application.mutation_runtime import (
    AuthoritativeReadSetCapture,
    MutationBasisClaims,
    MutationBasisCodec,
    ReadSetRevalidator,
    ReadSetValidation,
)
from daen_geocore.domain.references import PlaceRef
from daen_geocore.ports.audit.store import MutationAuditRecord, MutationAuditStore
from daen_geocore.ports.clock import Clock
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
    MutationBasisToken,
    OwnerPresent,
    OwnerStateReader,
    PlaceOwner,
)
from daen_geocore.ports.persistence.commit import CommitAccepted, CommitNotCommitted, CommitOutcome
from daen_geocore.ports.persistence.records import (
    ConditionalWriteDisposition,
    InsertDisposition,
    OpaqueEncodedPayload,
    PlaceHistoryFact,
    PlaceHistoryFactRef,
    RecordAbsent,
)
from daen_geocore.ports.persistence.repositories import (
    AssertionsRepository,
    IdentityRepository,
    RepresentationRepository,
)
from daen_geocore.ports.recovery.gate import RecoveryGate
from daen_geocore.ports.references.generation import StateWitnessGenerator
from daen_geocore.ports.result import PortError, PortResult, PortSuccess
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueReplayMetadata,
    TechnicalOperationKey,
)

CLOSE_OPERATION = TechnicalOperationKey("place.close")
WITHDRAW_OPERATION = TechnicalOperationKey("place.withdraw")
CLOSE_FACT_TYPE = "place.closed"
WITHDRAW_FACT_TYPE = "place.withdrawn_from_new_use"


@dataclass(frozen=True, slots=True)
class ClosePlaceCommand:
    key: IdempotencyBindingKey
    intent_fingerprint: IntentFingerprint
    place_ref: PlaceRef
    mutation_basis: MutationBasisToken
    mutation_provenance: OpaqueEncodedPayload


@dataclass(frozen=True, slots=True)
class WithdrawPlaceCommand:
    key: IdempotencyBindingKey
    intent_fingerprint: IntentFingerprint
    place_ref: PlaceRef
    mutation_basis: MutationBasisToken
    mutation_provenance: OpaqueEncodedPayload


class PlaceMutationOutcome(StrEnum):
    APPLIED = "applied"
    ALREADY_HOLDS = "already_holds"
    REPLAY = "replay"
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"
    TARGET_PLACE_NOT_FOUND = "target_place_not_found"
    TARGET_PLACE_HEAD_MISSING = "target_place_head_missing"
    INVALID_BASIS = "invalid_basis"
    RECOVERY_NOT_READY = "recovery_not_ready"
    RECOVERY_INCARNATION_MISMATCH = "recovery_incarnation_mismatch"
    INSUFFICIENT_BASIS = "insufficient_basis"
    STALE_BASIS = "stale_basis"
    HISTORY_CONFLICT = "history_conflict"
    AUDIT_CONFLICT = "audit_conflict"
    NOT_COMMITTED = "not_committed"
    COMMIT_OUTCOME_UNKNOWN = "commit_outcome_unknown"


@dataclass(frozen=True, slots=True)
class PlaceMutationResult:
    outcome: PlaceMutationOutcome
    place_ref: PlaceRef
    replayed_outcome: PlaceMutationOutcome | None = None


class _PlaceGenerator(StateWitnessGenerator, Protocol):
    def new_place_history_fact_ref(self) -> PlaceHistoryFactRef: ...


class _PlaceUow(Protocol):
    identity: IdentityRepository
    assertions: AssertionsRepository
    representation: RepresentationRepository
    committed_idempotency: CommittedIdempotencyStore
    mutation_audit: MutationAuditStore

    def __enter__(self) -> _PlaceUow: ...
    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: ...
    def commit(self) -> CommitOutcome: ...
    def rollback(self) -> None: ...


class _PlaceFactory(Protocol):
    def create(self) -> _PlaceUow: ...


def _result(
    outcome: PlaceMutationOutcome,
    place_ref: PlaceRef,
    replayed: PlaceMutationOutcome | None = None,
) -> PortSuccess[PlaceMutationResult]:
    return PortSuccess(PlaceMutationResult(outcome, place_ref, replayed))


def _replay_result(
    binding: CommittedMutationBinding, place_ref: PlaceRef
) -> PlaceMutationOutcome | None:
    if binding.result.references != (place_ref,):
        return None
    values = dict(binding.result.replay_metadata.entries)
    if len(binding.result.replay_metadata.entries) != 1:
        return None
    kind = values.get("result_kind")
    if kind in {"place_closed", "place_withdrawn"}:
        return PlaceMutationOutcome.APPLIED
    if kind in {"place_already_closed", "place_already_withdrawn"}:
        return PlaceMutationOutcome.ALREADY_HOLDS
    return None


class _PlaceMutation:
    operation: TechnicalOperationKey
    fact_type: str
    applied_kind: str
    already_kind: str

    def __init__(
        self,
        uow_factory: _PlaceFactory,
        gate: RecoveryGate,
        basis_codec: MutationBasisCodec,
        generator: _PlaceGenerator,
        clock: Clock,
    ) -> None:
        self._factory = uow_factory
        self._gate = gate
        self._basis_codec = basis_codec
        self._generator = generator
        self._clock = clock

    def execute(
        self, command: ClosePlaceCommand | WithdrawPlaceCommand
    ) -> PortResult[PlaceMutationResult]:
        replay = self._read_committed(command)
        if isinstance(replay, PortError) or replay.value is not None:
            return cast(PortResult[PlaceMutationResult], replay)
        with self._factory.create() as uow:
            checked = self._check_target_and_basis(uow, command)
            if checked is not None:
                return checked
            history = uow.identity.list_place_history(command.place_ref)
            if isinstance(history, PortError):
                return history
        observation = self._gate.observation()
        if not observation.may_authoritative_serve:
            return _result(PlaceMutationOutcome.RECOVERY_NOT_READY, command.place_ref)
        serving = self._gate.validate_before_authoritative_serving()
        if isinstance(serving, PortError):
            return serving
        return self._authoritative(command)

    def _read_committed(
        self, command: ClosePlaceCommand | WithdrawPlaceCommand
    ) -> PortResult[PlaceMutationResult | None]:
        with self._factory.create() as uow:
            read = uow.committed_idempotency.read(command.key)
            if isinstance(read, PortError):
                return read
            if not isinstance(read.value, CommittedBindingFound):
                return PortSuccess(None)
            binding = read.value.binding
            if (
                binding.intent_fingerprint != command.intent_fingerprint
                or binding.operation_key != self.operation
            ):
                return _result(PlaceMutationOutcome.IDEMPOTENCY_CONFLICT, command.place_ref)
            outcome = _replay_result(binding, command.place_ref)
            if outcome is None:
                return _result(PlaceMutationOutcome.IDEMPOTENCY_CONFLICT, command.place_ref)
            return _result(PlaceMutationOutcome.REPLAY, command.place_ref, outcome)

    def _check_target_and_basis(
        self, uow: _PlaceUow, command: ClosePlaceCommand | WithdrawPlaceCommand
    ) -> PortResult[PlaceMutationResult] | None:
        place = uow.identity.get_place(command.place_ref)
        if isinstance(place, PortError):
            return place
        if isinstance(place.value, RecordAbsent):
            return _result(PlaceMutationOutcome.TARGET_PLACE_NOT_FOUND, command.place_ref)
        head = uow.identity.get_place_head(command.place_ref)
        if isinstance(head, PortError):
            return head
        if isinstance(head.value, RecordAbsent):
            return _result(PlaceMutationOutcome.TARGET_PLACE_HEAD_MISSING, command.place_ref)
        return self._validate_basis(command.mutation_basis, command.place_ref, uow)

    def _validate_basis(
        self, token: MutationBasisToken, place_ref: PlaceRef, uow: _PlaceUow
    ) -> PortResult[PlaceMutationResult] | None:
        observation = self._gate.observation()
        if not observation.may_authoritative_serve:
            return _result(PlaceMutationOutcome.RECOVERY_NOT_READY, place_ref)
        serving = self._gate.validate_before_authoritative_serving()
        if isinstance(serving, PortError):
            return serving
        if serving.value != observation.incarnation:
            return _result(PlaceMutationOutcome.RECOVERY_INCARNATION_MISMATCH, place_ref)
        decoded = self._basis_codec.verify(token)
        if isinstance(decoded, PortError):
            return decoded
        if not isinstance(decoded.value, MutationBasisClaims):
            return _result(PlaceMutationOutcome.INVALID_BASIS, place_ref)
        if decoded.value.recovery_incarnation != observation.incarnation:
            return _result(PlaceMutationOutcome.RECOVERY_INCARNATION_MISMATCH, place_ref)
        claims = [
            claim
            for claim in decoded.value.observed_owners
            if isinstance(claim.owner, PlaceOwner) and claim.owner.place_ref == place_ref
        ]
        if len(claims) != 1 or not isinstance(claims[0].state, OwnerPresent):
            return _result(PlaceMutationOutcome.INSUFFICIENT_BASIS, place_ref)
        current = OwnerStateReader().read(claims[0].owner, uow)
        if isinstance(current, PortError):
            return current
        if current.value != claims[0].state:
            return _result(PlaceMutationOutcome.STALE_BASIS, place_ref)
        return None

    def _authoritative(
        self, command: ClosePlaceCommand | WithdrawPlaceCommand
    ) -> PortResult[PlaceMutationResult]:
        with self._factory.create() as uow:
            replay = self._read_binding_in_uow(command, uow)
            if isinstance(replay, PortError) or replay.value is not None:
                return cast(PortResult[PlaceMutationResult], replay)
            checked = self._check_target_and_basis(uow, command)
            if checked is not None:
                uow.rollback()
                return checked
            history = uow.identity.list_place_history(command.place_ref)
            if isinstance(history, PortError):
                uow.rollback()
                return history
            if any(fact.fact_type == self.fact_type for fact in history.value):
                return self._commit_metadata_only(uow, command, PlaceMutationOutcome.ALREADY_HOLDS)
            read_set = AuthoritativeReadSetCapture(OwnerStateReader()).capture(
                (PlaceOwner(command.place_ref),), uow
            )
            if isinstance(read_set, PortError):
                uow.rollback()
                return read_set
            current = read_set.value.observed_owners[0].state
            if not isinstance(current, OwnerPresent):
                uow.rollback()
                return _result(PlaceMutationOutcome.TARGET_PLACE_HEAD_MISSING, command.place_ref)
            history_ref = self._generator.new_place_history_fact_ref()
            witness = self._generator.new_state_witness()
            recorded = self._clock.now()
            fact = PlaceHistoryFact(
                history_ref,
                command.place_ref,
                self.fact_type,
                recorded,
                command.mutation_provenance,
            )
            added = uow.identity.append_place_history_if_absent(fact)
            if isinstance(added, PortError):
                uow.rollback()
                return added
            if added.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(PlaceMutationOutcome.HISTORY_CONFLICT, command.place_ref)
            valid = ReadSetRevalidator(OwnerStateReader()).revalidate(read_set.value, uow)
            if isinstance(valid, PortError):
                uow.rollback()
                return valid
            if valid.value is not ReadSetValidation.VALID:
                uow.rollback()
                return _result(PlaceMutationOutcome.STALE_BASIS, command.place_ref)
            cas = uow.identity.compare_and_swap_place_head(
                command.place_ref, current.witness, history_ref, witness
            )
            if isinstance(cas, PortError):
                uow.rollback()
                return cas
            if cas.value is not ConditionalWriteDisposition.APPLIED:
                uow.rollback()
                return _result(PlaceMutationOutcome.STALE_BASIS, command.place_ref)
            return self._commit_metadata_only(uow, command, PlaceMutationOutcome.APPLIED, recorded)

    def _commit_metadata_only(
        self,
        uow: _PlaceUow,
        command: ClosePlaceCommand | WithdrawPlaceCommand,
        outcome: PlaceMutationOutcome,
        recorded: datetime | None = None,
    ) -> PortResult[PlaceMutationResult]:
        timestamp = self._clock.now() if recorded is None else recorded
        details = OpaqueEncodedPayload(
            "daen.step13.audit.v1",
            json.dumps(
                {
                    "kind": self.applied_kind
                    if outcome is PlaceMutationOutcome.APPLIED
                    else self.already_kind,
                    "place_ref": command.place_ref.token,
                },
                separators=(",", ":"),
                sort_keys=True,
            ).encode(),
        )
        audited = uow.mutation_audit.append_if_absent(
            MutationAuditRecord(
                command.key,
                command.intent_fingerprint,
                self.operation,
                timestamp,
                command.mutation_provenance,
                details,
            )
        )
        if isinstance(audited, PortError):
            uow.rollback()
            return audited
        if audited.value is InsertDisposition.CONFLICTING_EXISTING:
            uow.rollback()
            return _result(PlaceMutationOutcome.AUDIT_CONFLICT, command.place_ref)
        binding = CommittedMutationBinding(
            command.key,
            command.intent_fingerprint,
            self.operation,
            CommittedMutationResult(
                (command.place_ref,),
                OpaqueReplayMetadata(
                    (
                        (
                            "result_kind",
                            self.applied_kind
                            if outcome is PlaceMutationOutcome.APPLIED
                            else self.already_kind,
                        ),
                    )
                ),
            ),
            BindingRetention.PUBLIC_REPLAY_HORIZON,
        )
        committed = uow.committed_idempotency.create_if_absent(binding)
        if isinstance(committed, PortError):
            uow.rollback()
            return committed
        if committed.value is IdempotencyCreateDisposition.CONFLICTING_EXISTING:
            uow.rollback()
            return _result(PlaceMutationOutcome.IDEMPOTENCY_CONFLICT, command.place_ref)
        commit = uow.commit()
        if isinstance(commit, CommitAccepted):
            return _result(outcome, command.place_ref)
        if isinstance(commit, CommitNotCommitted):
            return _result(PlaceMutationOutcome.NOT_COMMITTED, command.place_ref)
        return _result(PlaceMutationOutcome.COMMIT_OUTCOME_UNKNOWN, command.place_ref)

    def _read_binding_in_uow(
        self, command: ClosePlaceCommand | WithdrawPlaceCommand, uow: _PlaceUow
    ) -> PortResult[PlaceMutationResult | None]:
        read = uow.committed_idempotency.read(command.key)
        if isinstance(read, PortError):
            return read
        if not isinstance(read.value, CommittedBindingFound):
            return PortSuccess(None)
        binding = read.value.binding
        if (
            binding.intent_fingerprint != command.intent_fingerprint
            or binding.operation_key != self.operation
        ):
            return _result(PlaceMutationOutcome.IDEMPOTENCY_CONFLICT, command.place_ref)
        outcome = _replay_result(binding, command.place_ref)
        return (
            _result(PlaceMutationOutcome.REPLAY, command.place_ref, outcome)
            if outcome is not None
            else _result(PlaceMutationOutcome.IDEMPOTENCY_CONFLICT, command.place_ref)
        )


class ClosePlace(_PlaceMutation):
    operation = CLOSE_OPERATION
    fact_type = CLOSE_FACT_TYPE
    applied_kind = "place_closed"
    already_kind = "place_already_closed"


class WithdrawPlace(_PlaceMutation):
    operation = WITHDRAW_OPERATION
    fact_type = WITHDRAW_FACT_TYPE
    applied_kind = "place_withdrawn"
    already_kind = "place_already_withdrawn"
