from sqlalchemy import Connection, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError

from daen_geocore.infrastructure.postgres.repositories.common import technical_error
from daen_geocore.infrastructure.postgres.schema import (
    mutation_committed_binding,
    mutation_committed_replay_metadata,
    mutation_committed_result_reference,
)
from daen_geocore.ports.idempotency.store import (
    BindingRetention,
    CommittedBindingAbsent,
    CommittedBindingFound,
    CommittedIdempotencyStore,
    CommittedMutationBinding,
    CommittedMutationResult,
    IdempotencyBindingKey,
    IdempotencyCreateDisposition,
)
from daen_geocore.ports.result import PortError, PortResult, PortSuccess
from daen_geocore.ports.technical import (
    IntentFingerprint,
    OpaqueReplayMetadata,
    TechnicalOperationKey,
)

from .reference_codec import reference_from_row, reference_kind


class PostgresCommittedIdempotencyStore(CommittedIdempotencyStore):
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def read(
        self, key: IdempotencyBindingKey
    ) -> PortResult[CommittedBindingFound | CommittedBindingAbsent]:
        try:
            row = (
                self._connection.execute(
                    select(mutation_committed_binding).where(
                        mutation_committed_binding.c.client_identity == key.client_identity.value,
                        mutation_committed_binding.c.request_identity == key.request_identity.value,
                    )
                )
                .mappings()
                .first()
            )
            if row is None:
                return PortSuccess(CommittedBindingAbsent())
            references = tuple(
                reference_from_row(item["reference_kind"], item["reference_token"])
                for item in self._connection.execute(
                    select(mutation_committed_result_reference)
                    .where(
                        mutation_committed_result_reference.c.client_identity
                        == key.client_identity.value,
                        mutation_committed_result_reference.c.request_identity
                        == key.request_identity.value,
                    )
                    .order_by(mutation_committed_result_reference.c.ordinal)
                ).mappings()
            )
            metadata = tuple(
                (item["metadata_key"], item["metadata_value"])
                for item in self._connection.execute(
                    select(mutation_committed_replay_metadata)
                    .where(
                        mutation_committed_replay_metadata.c.client_identity
                        == key.client_identity.value,
                        mutation_committed_replay_metadata.c.request_identity
                        == key.request_identity.value,
                    )
                    .order_by(mutation_committed_replay_metadata.c.ordinal)
                ).mappings()
            )
            binding = CommittedMutationBinding(
                key,
                IntentFingerprint(row["intent_fingerprint"]),
                TechnicalOperationKey(row["operation_key"]),
                CommittedMutationResult(references, OpaqueReplayMetadata(metadata)),
                BindingRetention(row["retention_class"]),
            )
            return PortSuccess(CommittedBindingFound(binding))
        except (SQLAlchemyError, ValueError) as error:
            return technical_error(error)

    def create_if_absent(
        self, binding: CommittedMutationBinding
    ) -> PortResult[IdempotencyCreateDisposition]:
        key = binding.key
        try:
            statement = (
                pg_insert(mutation_committed_binding)
                .values(
                    client_identity=key.client_identity.value,
                    request_identity=key.request_identity.value,
                    intent_fingerprint=binding.intent_fingerprint.value,
                    operation_key=binding.operation_key.value,
                    retention_class=binding.retention.value,
                )
                .on_conflict_do_nothing(
                    index_elements=[
                        mutation_committed_binding.c.client_identity,
                        mutation_committed_binding.c.request_identity,
                    ]
                )
                .returning(mutation_committed_binding.c.client_identity)
            )
            if self._connection.execute(statement).first() is not None:
                for ordinal, reference in enumerate(binding.result.references):
                    kind, token = reference_kind(reference)
                    self._connection.execute(
                        mutation_committed_result_reference.insert().values(
                            client_identity=key.client_identity.value,
                            request_identity=key.request_identity.value,
                            ordinal=ordinal,
                            reference_kind=kind,
                            reference_token=token,
                        )
                    )
                for ordinal, (metadata_key, metadata_value) in enumerate(
                    binding.result.replay_metadata.entries
                ):
                    self._connection.execute(
                        mutation_committed_replay_metadata.insert().values(
                            client_identity=key.client_identity.value,
                            request_identity=key.request_identity.value,
                            ordinal=ordinal,
                            metadata_key=metadata_key,
                            metadata_value=metadata_value,
                        )
                    )
                return PortSuccess(IdempotencyCreateDisposition.CREATED)
            existing = self.read(key)
            if isinstance(existing, PortError):
                return existing
            if (
                isinstance(existing.value, CommittedBindingFound)
                and existing.value.binding == binding
            ):
                return PortSuccess(IdempotencyCreateDisposition.ALREADY_PRESENT_SAME)
            return PortSuccess(IdempotencyCreateDisposition.CONFLICTING_EXISTING)
        except (SQLAlchemyError, ValueError) as error:
            return technical_error(error)
