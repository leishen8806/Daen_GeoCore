from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from daen_geocore.ports.evidence.store import StableReference
from daen_geocore.ports.result import PortResult
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueClientIdentity,
    OpaqueReplayMetadata,
    OpaqueRequestIdentity,
    TechnicalOperationKey,
)


@dataclass(frozen=True, slots=True)
class IdempotencyBindingKey:
    client_identity: OpaqueClientIdentity
    request_identity: OpaqueRequestIdentity


@dataclass(frozen=True, slots=True)
class CommittedMutationResult:
    references: tuple[StableReference, ...]
    replay_metadata: OpaqueReplayMetadata = OpaqueReplayMetadata()


class BindingRetention(StrEnum):
    PUBLIC_REPLAY_HORIZON = "public_replay_horizon"
    PLACE_IDENTITY_LIFETIME = "place_identity_lifetime"


@dataclass(frozen=True, slots=True)
class CommittedMutationBinding:
    key: IdempotencyBindingKey
    intent_fingerprint: IntentFingerprint
    operation_key: TechnicalOperationKey
    result: CommittedMutationResult
    retention: BindingRetention = BindingRetention.PUBLIC_REPLAY_HORIZON


class IdempotencyCreateDisposition(StrEnum):
    CREATED = "created"
    ALREADY_PRESENT_SAME = "already_present_same"
    CONFLICTING_EXISTING = "conflicting_existing"


@dataclass(frozen=True, slots=True)
class CommittedBindingFound:
    binding: CommittedMutationBinding


@dataclass(frozen=True, slots=True)
class CommittedBindingAbsent:
    pass


class CommittedIdempotencyStore(Protocol):
    def read(
        self, key: IdempotencyBindingKey
    ) -> PortResult[CommittedBindingFound | CommittedBindingAbsent]: ...
    def create_if_absent(
        self, binding: CommittedMutationBinding
    ) -> PortResult[IdempotencyCreateDisposition]: ...
