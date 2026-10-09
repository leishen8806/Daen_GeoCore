from dataclasses import dataclass
from enum import StrEnum

from daen_geocore.ports.idempotency.store import (
    CommittedBindingAbsent,
    CommittedIdempotencyStore,
    CommittedMutationBinding,
    IdempotencyBindingKey,
)
from daen_geocore.ports.result import PortError, PortResult, PortSuccess
from daen_geocore.ports.technical import IntentFingerprint, TechnicalOperationKey


class ReplayDecision(StrEnum):
    EXECUTE = "execute"
    REPLAY = "replay"
    CONFLICT = "conflict"


@dataclass(frozen=True, slots=True)
class ReplayResult:
    decision: ReplayDecision
    binding: CommittedMutationBinding | None = None


class IdempotencyReplayDecider:
    def __init__(self, store: CommittedIdempotencyStore) -> None:
        self._store = store

    def decide(
        self,
        key: IdempotencyBindingKey,
        intent: IntentFingerprint,
        operation: TechnicalOperationKey,
    ) -> PortResult[ReplayResult]:
        result = self._store.read(key)
        if isinstance(result, PortError):
            return result
        if isinstance(result.value, CommittedBindingAbsent):
            return PortSuccess(ReplayResult(ReplayDecision.EXECUTE))
        binding = result.value.binding
        if binding.intent_fingerprint == intent and binding.operation_key == operation:
            return PortSuccess(ReplayResult(ReplayDecision.REPLAY, binding))
        return PortSuccess(ReplayResult(ReplayDecision.CONFLICT))
