from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from daen_geocore.application.mutation_runtime import ReadSetRevalidator, ReadSetValidation
from daen_geocore.domain.references import SourceAssertionRef
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
    AssertionOwner,
    AuthoritativeReadSetCapture,
    OwnerPresent,
    OwnerStateReader,
)
from daen_geocore.ports.persistence.commit import CommitAccepted, CommitNotCommitted, CommitUnknown
from daen_geocore.ports.persistence.records import (
    AssertionHistoryFact,
    AssertionHistoryFactRef,
    ConditionalWriteDisposition,
    InsertDisposition,
    OpaqueEncodedPayload,
    RecordAbsent,
    StateWitness,
)
from daen_geocore.ports.persistence.repositories import (
    AssertionsRepository,
    IdentityRepository,
    RepresentationRepository,
)
from daen_geocore.ports.recovery.gate import RecoveryGate
from daen_geocore.ports.result import PortError, PortResult, PortSuccess
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueReplayMetadata,
    TechnicalOperationKey,
)

WITHDRAW_OPERATION = TechnicalOperationKey("source_assertion.withdraw")
WITHDRAW_FACT_TYPE = "source_assertion.withdrawn"


@dataclass(frozen=True, slots=True)
class WithdrawSourceAssertionCommand:
    key: IdempotencyBindingKey
    intent_fingerprint: IntentFingerprint
    target_source_assertion_ref: SourceAssertionRef
    mutation_provenance: OpaqueEncodedPayload


class SourceAssertionWithdrawalOutcome(StrEnum):
    APPLIED = "applied"
    ALREADY_HOLDS = "already_holds"
    REPLAY = "replay"
    IDEMPOTENCY_CONFLICT = "idempotency_conflict"
    TARGET_ASSERTION_NOT_FOUND = "target_assertion_not_found"
    TARGET_STANDING_HEAD_MISSING = "target_standing_head_missing"
    RECOVERY_NOT_READY = "recovery_not_ready"
    HISTORY_CONFLICT = "history_conflict"
    STANDING_STATE_CHANGED = "standing_state_changed"
    AUDIT_CONFLICT = "audit_conflict"
    NOT_COMMITTED = "not_committed"
    COMMIT_OUTCOME_UNKNOWN = "commit_outcome_unknown"


@dataclass(frozen=True, slots=True)
class SourceAssertionWithdrawalResult:
    outcome: SourceAssertionWithdrawalOutcome
    target_source_assertion_ref: SourceAssertionRef
    replayed_outcome: SourceAssertionWithdrawalOutcome | None = None


class _WithdrawalGenerator(Protocol):
    def new_assertion_history_fact_ref(self) -> AssertionHistoryFactRef: ...
    def new_state_witness(self) -> StateWitness: ...


class _WithdrawalUow(Protocol):
    identity: IdentityRepository
    assertions: AssertionsRepository
    representation: RepresentationRepository
    committed_idempotency: CommittedIdempotencyStore
    mutation_audit: MutationAuditStore

    def __enter__(self) -> _WithdrawalUow: ...
    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None: ...
    def commit(self) -> CommitAccepted | CommitNotCommitted | CommitUnknown: ...
    def rollback(self) -> None: ...


class _WithdrawalFactory(Protocol):
    def create(self) -> _WithdrawalUow: ...


def _result(
    outcome: SourceAssertionWithdrawalOutcome,
    target: SourceAssertionRef,
    replayed_outcome: SourceAssertionWithdrawalOutcome | None = None,
) -> PortSuccess[SourceAssertionWithdrawalResult]:
    return PortSuccess(SourceAssertionWithdrawalResult(outcome, target, replayed_outcome))


def _replay_result(
    binding: CommittedMutationBinding, target: SourceAssertionRef
) -> SourceAssertionWithdrawalOutcome | None:
    if binding.result.references != (target,):
        return None
    kind = dict(binding.result.replay_metadata.entries).get("result_kind")
    if kind == "withdrawn":
        return SourceAssertionWithdrawalOutcome.APPLIED
    if kind == "already_withdrawn":
        return SourceAssertionWithdrawalOutcome.ALREADY_HOLDS
    return None


class WithdrawSourceAssertion:
    def __init__(
        self,
        uow_factory: _WithdrawalFactory,
        recovery_gate: RecoveryGate,
        generator: _WithdrawalGenerator,
        clock: Clock,
    ) -> None:
        self._uow_factory = uow_factory
        self._gate = recovery_gate
        self._generator = generator
        self._clock = clock

    def execute(
        self, command: WithdrawSourceAssertionCommand
    ) -> PortResult[SourceAssertionWithdrawalResult]:
        replay = self._read_committed(command)
        if isinstance(replay, PortError):
            return replay
        if replay.value is not None:
            return PortSuccess(replay.value)
        with self._uow_factory.create() as uow:
            target = uow.assertions.get_assertion(command.target_source_assertion_ref)
            if isinstance(target, PortError):
                return target
            if isinstance(target.value, RecordAbsent):
                return _result(
                    SourceAssertionWithdrawalOutcome.TARGET_ASSERTION_NOT_FOUND,
                    command.target_source_assertion_ref,
                )
            head = uow.assertions.get_standing_head(command.target_source_assertion_ref)
            if isinstance(head, PortError):
                return head
            if isinstance(head.value, RecordAbsent):
                return _result(
                    SourceAssertionWithdrawalOutcome.TARGET_STANDING_HEAD_MISSING,
                    command.target_source_assertion_ref,
                )
            history = uow.assertions.list_assertion_history(command.target_source_assertion_ref)
            if isinstance(history, PortError):
                return history
        observation = self._gate.observation()
        if not observation.may_authoritative_serve:
            return _result(
                SourceAssertionWithdrawalOutcome.RECOVERY_NOT_READY,
                command.target_source_assertion_ref,
            )
        serving = self._gate.validate_before_authoritative_serving()
        if isinstance(serving, PortError):
            return serving
        return self._authoritative(command)

    def _read_committed(
        self, command: WithdrawSourceAssertionCommand
    ) -> PortResult[SourceAssertionWithdrawalResult | None]:
        with self._uow_factory.create() as uow:
            read = uow.committed_idempotency.read(command.key)
            if isinstance(read, PortError):
                return read
            if not isinstance(read.value, CommittedBindingFound):
                return PortSuccess(None)
            binding = read.value.binding
            if (
                binding.intent_fingerprint != command.intent_fingerprint
                or binding.operation_key != WITHDRAW_OPERATION
            ):
                return _result(
                    SourceAssertionWithdrawalOutcome.IDEMPOTENCY_CONFLICT,
                    command.target_source_assertion_ref,
                )
            outcome = _replay_result(binding, command.target_source_assertion_ref)
            if outcome is None:
                return _result(
                    SourceAssertionWithdrawalOutcome.IDEMPOTENCY_CONFLICT,
                    command.target_source_assertion_ref,
                )
            return _result(
                SourceAssertionWithdrawalOutcome.REPLAY,
                command.target_source_assertion_ref,
                outcome,
            )

    def _authoritative(
        self, command: WithdrawSourceAssertionCommand
    ) -> PortResult[SourceAssertionWithdrawalResult]:
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
                return _result(
                    SourceAssertionWithdrawalOutcome.TARGET_ASSERTION_NOT_FOUND,
                    command.target_source_assertion_ref,
                )
            head = uow.assertions.get_standing_head(command.target_source_assertion_ref)
            if isinstance(head, PortError):
                uow.rollback()
                return head
            if isinstance(head.value, RecordAbsent):
                uow.rollback()
                return _result(
                    SourceAssertionWithdrawalOutcome.TARGET_STANDING_HEAD_MISSING,
                    command.target_source_assertion_ref,
                )
            history = uow.assertions.list_assertion_history(command.target_source_assertion_ref)
            if isinstance(history, PortError):
                uow.rollback()
                return history
            already = any(f.fact_type == WITHDRAW_FACT_TYPE for f in history.value)
            if already:
                return self._commit_metadata_only(
                    uow, command, SourceAssertionWithdrawalOutcome.ALREADY_HOLDS
                )
            read_set = AuthoritativeReadSetCapture(OwnerStateReader()).capture(
                (AssertionOwner(command.target_source_assertion_ref),), uow
            )
            if isinstance(read_set, PortError):
                uow.rollback()
                return read_set
            current = read_set.value.observed_owners[0].state
            if not isinstance(current, OwnerPresent):
                uow.rollback()
                return _result(
                    SourceAssertionWithdrawalOutcome.TARGET_STANDING_HEAD_MISSING,
                    command.target_source_assertion_ref,
                )
            history_ref = self._generator.new_assertion_history_fact_ref()
            replacement_witness = self._generator.new_state_witness()
            recorded_at = self._clock.now()
            fact = AssertionHistoryFact(
                history_ref,
                command.target_source_assertion_ref,
                WITHDRAW_FACT_TYPE,
                recorded_at,
                None,
                command.mutation_provenance,
            )
            added = uow.assertions.append_assertion_history_if_absent(fact)
            if isinstance(added, PortError):
                uow.rollback()
                return added
            if added.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(
                    SourceAssertionWithdrawalOutcome.HISTORY_CONFLICT,
                    command.target_source_assertion_ref,
                )
            revalidated = ReadSetRevalidator(OwnerStateReader()).revalidate(read_set.value, uow)
            if isinstance(revalidated, PortError):
                uow.rollback()
                return revalidated
            if revalidated.value is not ReadSetValidation.VALID:
                uow.rollback()
                return _result(
                    SourceAssertionWithdrawalOutcome.STANDING_STATE_CHANGED,
                    command.target_source_assertion_ref,
                )
            cas = uow.assertions.compare_and_swap_standing_head(
                command.target_source_assertion_ref,
                current.witness,
                history_ref,
                replacement_witness,
            )
            if isinstance(cas, PortError):
                uow.rollback()
                return cas
            if cas.value is not ConditionalWriteDisposition.APPLIED:
                uow.rollback()
                return _result(
                    SourceAssertionWithdrawalOutcome.STANDING_STATE_CHANGED,
                    command.target_source_assertion_ref,
                )
            audited = self._append_audit(uow, command, recorded_at, "withdrawn")
            if isinstance(audited, PortError):
                uow.rollback()
                return audited
            if audited.value is InsertDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(
                    SourceAssertionWithdrawalOutcome.AUDIT_CONFLICT,
                    command.target_source_assertion_ref,
                )
            binding = self._binding(command, "withdrawn")
            created = uow.committed_idempotency.create_if_absent(binding)
            if isinstance(created, PortError):
                uow.rollback()
                return created
            if created.value is IdempotencyCreateDisposition.CONFLICTING_EXISTING:
                uow.rollback()
                return _result(
                    SourceAssertionWithdrawalOutcome.IDEMPOTENCY_CONFLICT,
                    command.target_source_assertion_ref,
                )
            return self._finish_commit(
                uow, command.target_source_assertion_ref, SourceAssertionWithdrawalOutcome.APPLIED
            )

    def _commit_metadata_only(
        self,
        uow: _WithdrawalUow,
        command: WithdrawSourceAssertionCommand,
        outcome: SourceAssertionWithdrawalOutcome,
    ) -> PortResult[SourceAssertionWithdrawalResult]:
        recorded_at = self._clock.now()
        audited = self._append_audit(uow, command, recorded_at, "already_withdrawn")
        if isinstance(audited, PortError):
            uow.rollback()
            return audited
        if audited.value is InsertDisposition.CONFLICTING_EXISTING:
            uow.rollback()
            return _result(
                SourceAssertionWithdrawalOutcome.AUDIT_CONFLICT, command.target_source_assertion_ref
            )
        created = uow.committed_idempotency.create_if_absent(
            self._binding(command, "already_withdrawn")
        )
        if isinstance(created, PortError):
            uow.rollback()
            return created
        if created.value is IdempotencyCreateDisposition.CONFLICTING_EXISTING:
            uow.rollback()
            return _result(
                SourceAssertionWithdrawalOutcome.IDEMPOTENCY_CONFLICT,
                command.target_source_assertion_ref,
            )
        return self._finish_commit(uow, command.target_source_assertion_ref, outcome)

    def _append_audit(
        self,
        uow: _WithdrawalUow,
        command: WithdrawSourceAssertionCommand,
        recorded_at: datetime,
        kind: str,
    ) -> PortResult[InsertDisposition]:
        details = OpaqueEncodedPayload(
            "daen.step11.audit.v1",
            json.dumps(
                {"kind": kind, "target": command.target_source_assertion_ref.token},
                separators=(",", ":"),
                sort_keys=True,
            ).encode(),
        )
        return uow.mutation_audit.append_if_absent(
            MutationAuditRecord(
                command.key,
                command.intent_fingerprint,
                WITHDRAW_OPERATION,
                recorded_at,
                command.mutation_provenance,
                details,
            )
        )

    def _binding(
        self, command: WithdrawSourceAssertionCommand, kind: str
    ) -> CommittedMutationBinding:
        return CommittedMutationBinding(
            command.key,
            command.intent_fingerprint,
            WITHDRAW_OPERATION,
            CommittedMutationResult(
                (command.target_source_assertion_ref,),
                OpaqueReplayMetadata((("result_kind", kind),)),
            ),
            BindingRetention.PUBLIC_REPLAY_HORIZON,
        )

    def _finish_commit(
        self,
        uow: _WithdrawalUow,
        target: SourceAssertionRef,
        outcome: SourceAssertionWithdrawalOutcome,
    ) -> PortResult[SourceAssertionWithdrawalResult]:
        committed = uow.commit()
        if isinstance(committed, CommitAccepted):
            return _result(outcome, target)
        if isinstance(committed, CommitNotCommitted):
            return _result(SourceAssertionWithdrawalOutcome.NOT_COMMITTED, target)
        return _result(SourceAssertionWithdrawalOutcome.COMMIT_OUTCOME_UNKNOWN, target)

    def _read_binding_in_uow(
        self, command: WithdrawSourceAssertionCommand, uow: _WithdrawalUow
    ) -> PortResult[SourceAssertionWithdrawalResult | None]:
        read = uow.committed_idempotency.read(command.key)
        if isinstance(read, PortError):
            return read
        if not isinstance(read.value, CommittedBindingFound):
            return PortSuccess(None)
        binding = read.value.binding
        if (
            binding.intent_fingerprint != command.intent_fingerprint
            or binding.operation_key != WITHDRAW_OPERATION
        ):
            return _result(
                SourceAssertionWithdrawalOutcome.IDEMPOTENCY_CONFLICT,
                command.target_source_assertion_ref,
            )
        outcome = _replay_result(binding, command.target_source_assertion_ref)
        return (
            _result(
                SourceAssertionWithdrawalOutcome.REPLAY,
                command.target_source_assertion_ref,
                outcome,
            )
            if outcome
            else _result(
                SourceAssertionWithdrawalOutcome.IDEMPOTENCY_CONFLICT,
                command.target_source_assertion_ref,
            )
        )
