from sqlalchemy import Connection, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError

from daen_geocore.infrastructure.postgres.repositories.common import technical_error
from daen_geocore.infrastructure.postgres.schema import mutation_audit
from daen_geocore.ports.audit.store import MutationAuditRecord, MutationAuditStore
from daen_geocore.ports.idempotency.store import IdempotencyBindingKey
from daen_geocore.ports.persistence.records import InsertDisposition, OpaqueEncodedPayload
from daen_geocore.ports.result import PortError, PortResult, PortSuccess
from daen_geocore.ports.technical import IntentFingerprint, TechnicalOperationKey


class PostgresMutationAuditStore(MutationAuditStore):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def read(self, key: IdempotencyBindingKey) -> PortResult[MutationAuditRecord | None]:
        try:
            row = (
                self._connection.execute(
                    select(mutation_audit).where(
                        mutation_audit.c.client_identity == key.client_identity.value,
                        mutation_audit.c.request_identity == key.request_identity.value,
                    )
                )
                .mappings()
                .first()
            )
            if row is None:
                return PortSuccess(None)
            return PortSuccess(
                MutationAuditRecord(
                    key,
                    IntentFingerprint(row["intent_fingerprint"]),
                    TechnicalOperationKey(row["operation_key"]),
                    row["recorded_at"],
                    OpaqueEncodedPayload(
                        row["mutation_provenance_encoding"],
                        bytes(row["mutation_provenance_payload"]),
                    ),
                    OpaqueEncodedPayload(
                        row["audit_details_encoding"],
                        bytes(row["audit_details_payload"]),
                    ),
                )
            )
        except SQLAlchemyError as error:
            return technical_error(error)

    def append_if_absent(self, record: MutationAuditRecord) -> PortResult[InsertDisposition]:
        key = record.key
        try:
            statement = (
                pg_insert(mutation_audit)
                .values(
                    client_identity=key.client_identity.value,
                    request_identity=key.request_identity.value,
                    intent_fingerprint=record.intent_fingerprint.value,
                    operation_key=record.operation_key.value,
                    recorded_at=record.recorded_at,
                    mutation_provenance_encoding=record.mutation_provenance.encoding_id,
                    mutation_provenance_payload=record.mutation_provenance.payload,
                    audit_details_encoding=record.details.encoding_id,
                    audit_details_payload=record.details.payload,
                )
                .on_conflict_do_nothing(
                    index_elements=[
                        mutation_audit.c.client_identity,
                        mutation_audit.c.request_identity,
                    ]
                )
                .returning(mutation_audit.c.client_identity)
            )
            if self._connection.execute(statement).first() is not None:
                return PortSuccess(InsertDisposition.INSERTED)
            existing = self.read(key)
            if isinstance(existing, PortError):
                return existing
            return PortSuccess(
                InsertDisposition.ALREADY_PRESENT_SAME
                if existing.value == record
                else InsertDisposition.CONFLICTING_EXISTING
            )
        except SQLAlchemyError as error:
            return technical_error(error)
