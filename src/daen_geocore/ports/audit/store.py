from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

from daen_geocore.ports.idempotency.store import IdempotencyBindingKey
from daen_geocore.ports.persistence.records import InsertDisposition, OpaqueEncodedPayload
from daen_geocore.ports.result import PortResult
from daen_geocore.ports.technical import IntentFingerprint, TechnicalOperationKey


@dataclass(frozen=True, slots=True)
class MutationAuditRecord:
    key: IdempotencyBindingKey
    intent_fingerprint: IntentFingerprint
    operation_key: TechnicalOperationKey
    recorded_at: datetime
    mutation_provenance: OpaqueEncodedPayload
    details: OpaqueEncodedPayload

    def __post_init__(self) -> None:
        if self.recorded_at.tzinfo is None or self.recorded_at.utcoffset() != UTC.utcoffset(
            self.recorded_at
        ):
            raise ValueError("recorded_at must be UTC-aware")


class MutationAuditStore(Protocol):
    def append_if_absent(self, record: MutationAuditRecord) -> PortResult[InsertDisposition]: ...
    def read(self, key: IdempotencyBindingKey) -> PortResult[MutationAuditRecord | None]: ...
