from collections.abc import Mapping
from typing import Any

from sqlalchemy import Connection, and_, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError

from daen_geocore.domain.references import PlaceRef, SourceAssertionRef
from daen_geocore.infrastructure.postgres.schema import (
    assertions_history,
    assertions_source_assertion,
    assertions_standing_head,
)
from daen_geocore.ports.persistence.records import (
    AssertionHistoryFact,
    AssertionHistoryFactRef,
    AssertionStandingHead,
    ConditionalWriteDisposition,
    InsertDisposition,
    OpaqueEncodedPayload,
    PersistedExplicitScope,
    PersistedQualityKnown,
    PersistedTypedValue,
    RecordAbsent,
    RecordFound,
    SourceAssertionRecord,
    StateWitness,
)
from daen_geocore.ports.result import PortError, PortResult, PortSuccess

from .common import metadata_from_row, quality_from_row, scope_from_row, technical_error


class PostgresAssertionsRepository:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def _record(self, row: Mapping[Any, Any]) -> SourceAssertionRecord:
        return SourceAssertionRecord(
            SourceAssertionRef(row["source_assertion_ref"]),
            PlaceRef(row["place_ref"]),
            row["fact_purpose"],
            PersistedTypedValue(
                row["value_type_id"],
                OpaqueEncodedPayload(row["value_encoding"], bytes(row["value_payload"])),
            ),
            scope_from_row(row),
            OpaqueEncodedPayload(row["provenance_encoding"], bytes(row["provenance_payload"])),
            quality_from_row(row),
            row["recorded_at"],
        )

    def get_assertion(
        self, source_assertion_ref: SourceAssertionRef
    ) -> PortResult[RecordFound[SourceAssertionRecord] | RecordAbsent]:
        try:
            row = (
                self._connection.execute(
                    select(assertions_source_assertion).where(
                        assertions_source_assertion.c.source_assertion_ref
                        == source_assertion_ref.token
                    )
                )
                .mappings()
                .first()
            )
            return PortSuccess(RecordAbsent() if row is None else RecordFound(self._record(row)))
        except SQLAlchemyError as error:
            return technical_error(error)

    def list_assertions_for_place(
        self, place_ref: PlaceRef
    ) -> PortResult[tuple[SourceAssertionRecord, ...]]:
        return self._list(assertions_source_assertion.c.place_ref == place_ref.token)

    def list_assertions_for_place_fact(
        self, place_ref: PlaceRef, fact_purpose: str
    ) -> PortResult[tuple[SourceAssertionRecord, ...]]:
        return self._list(
            and_(
                assertions_source_assertion.c.place_ref == place_ref.token,
                assertions_source_assertion.c.fact_purpose == fact_purpose,
            )
        )

    def _list(self, predicate: Any) -> PortResult[tuple[SourceAssertionRecord, ...]]:
        try:
            rows = self._connection.execute(
                select(assertions_source_assertion).where(predicate)
            ).mappings()
            return PortSuccess(tuple(self._record(row) for row in rows))
        except SQLAlchemyError as error:
            return technical_error(error)

    def list_assertion_history(
        self, source_assertion_ref: SourceAssertionRef
    ) -> PortResult[tuple[AssertionHistoryFact, ...]]:
        try:
            rows = self._connection.execute(
                select(assertions_history).where(
                    assertions_history.c.source_assertion_ref == source_assertion_ref.token
                )
            ).mappings()
            return PortSuccess(
                tuple(
                    AssertionHistoryFact(
                        AssertionHistoryFactRef(row["history_fact_ref"]),
                        SourceAssertionRef(row["source_assertion_ref"]),
                        row["fact_type"],
                        row["recorded_at"],
                        None
                        if row["related_source_assertion_ref"] is None
                        else SourceAssertionRef(row["related_source_assertion_ref"]),
                        metadata_from_row(row),
                    )
                    for row in rows
                )
            )
        except SQLAlchemyError as error:
            return technical_error(error)

    def get_standing_head(
        self, source_assertion_ref: SourceAssertionRef
    ) -> PortResult[RecordFound[AssertionStandingHead] | RecordAbsent]:
        try:
            row = (
                self._connection.execute(
                    select(assertions_standing_head).where(
                        assertions_standing_head.c.source_assertion_ref
                        == source_assertion_ref.token
                    )
                )
                .mappings()
                .first()
            )
            if row is None:
                return PortSuccess(RecordAbsent())
            latest = (
                None
                if row["latest_history_fact_ref"] is None
                else AssertionHistoryFactRef(row["latest_history_fact_ref"])
            )
            return PortSuccess(
                RecordFound(
                    AssertionStandingHead(
                        SourceAssertionRef(row["source_assertion_ref"]),
                        latest,
                        StateWitness(row["state_witness"]),
                    )
                )
            )
        except SQLAlchemyError as error:
            return technical_error(error)

    def insert_assertion_if_absent(
        self, record: SourceAssertionRecord
    ) -> PortResult[InsertDisposition]:
        values = self._record_values(record)
        try:
            statement = (
                pg_insert(assertions_source_assertion)
                .values(values)
                .on_conflict_do_nothing(
                    index_elements=[assertions_source_assertion.c.source_assertion_ref]
                )
            )
            if self._connection.execute(statement).rowcount == 1:
                return PortSuccess(InsertDisposition.INSERTED)
            existing = self.get_assertion(record.source_assertion_ref)
            if isinstance(existing, PortError):
                return existing
            if isinstance(existing.value, RecordFound) and existing.value.record == record:
                return PortSuccess(InsertDisposition.ALREADY_PRESENT_SAME)
            return PortSuccess(InsertDisposition.CONFLICTING_EXISTING)
        except SQLAlchemyError as error:
            return technical_error(error)

    def _record_values(self, record: SourceAssertionRecord) -> dict[str, object]:
        scope = record.scope
        quality = record.quality
        return {
            "source_assertion_ref": record.source_assertion_ref.token,
            "place_ref": record.place_ref.token,
            "fact_purpose": record.fact_purpose,
            "value_type_id": record.value.type_id,
            "value_encoding": record.value.encoded.encoding_id,
            "value_payload": record.value.encoded.payload,
            "scope_is_explicit": isinstance(scope, PersistedExplicitScope),
            "scope_type_id": scope.type_id if isinstance(scope, PersistedExplicitScope) else None,
            "scope_encoding": scope.encoded.encoding_id
            if isinstance(scope, PersistedExplicitScope)
            else None,
            "scope_payload": scope.encoded.payload
            if isinstance(scope, PersistedExplicitScope)
            else None,
            "scope_equality_key": scope.equality_key
            if isinstance(scope, PersistedExplicitScope)
            else None,
            "provenance_encoding": record.provenance.encoding_id,
            "provenance_payload": record.provenance.payload,
            "quality_is_known": isinstance(quality, PersistedQualityKnown),
            "quality_encoding": quality.encoded.encoding_id
            if isinstance(quality, PersistedQualityKnown)
            else None,
            "quality_payload": quality.encoded.payload
            if isinstance(quality, PersistedQualityKnown)
            else None,
            "recorded_at": record.recorded_at,
        }

    def append_assertion_history_if_absent(
        self, fact: AssertionHistoryFact
    ) -> PortResult[InsertDisposition]:
        values = {
            "history_fact_ref": fact.history_fact_ref.value,
            "source_assertion_ref": fact.source_assertion_ref.token,
            "fact_type": fact.fact_type,
            "related_source_assertion_ref": None
            if fact.related_source_assertion_ref is None
            else fact.related_source_assertion_ref.token,
            "recorded_at": fact.recorded_at,
            "history_metadata_encoding": None
            if fact.metadata is None
            else fact.metadata.encoding_id,
            "history_metadata_payload": None if fact.metadata is None else fact.metadata.payload,
        }
        try:
            statement = (
                pg_insert(assertions_history)
                .values(values)
                .on_conflict_do_nothing(index_elements=[assertions_history.c.history_fact_ref])
            )
            if self._connection.execute(statement).rowcount == 1:
                return PortSuccess(InsertDisposition.INSERTED)
            existing = (
                self._connection.execute(
                    select(assertions_history).where(
                        assertions_history.c.history_fact_ref == fact.history_fact_ref.value
                    )
                )
                .mappings()
                .first()
            )
            if existing is None:
                return PortError(
                    technical_error(RuntimeError("history row absent after conflict")).failure
                )
            same = (
                existing.source_assertion_ref == fact.source_assertion_ref.token
                and existing.fact_type == fact.fact_type
                and existing.recorded_at == fact.recorded_at
                and existing.related_source_assertion_ref
                == (
                    None
                    if fact.related_source_assertion_ref is None
                    else fact.related_source_assertion_ref.token
                )
                and metadata_from_row(existing) == fact.metadata
            )
            return PortSuccess(
                InsertDisposition.ALREADY_PRESENT_SAME
                if same
                else InsertDisposition.CONFLICTING_EXISTING
            )
        except SQLAlchemyError as error:
            return technical_error(error)

    def insert_standing_head_if_absent(
        self, head: AssertionStandingHead
    ) -> PortResult[InsertDisposition]:
        values = {
            "source_assertion_ref": head.source_assertion_ref.token,
            "latest_history_fact_ref": None
            if head.latest_history_fact_ref is None
            else head.latest_history_fact_ref.value,
            "state_witness": head.state_witness.value,
        }
        try:
            statement = (
                pg_insert(assertions_standing_head)
                .values(values)
                .on_conflict_do_nothing(
                    index_elements=[assertions_standing_head.c.source_assertion_ref]
                )
            )
            if self._connection.execute(statement).rowcount == 1:
                return PortSuccess(InsertDisposition.INSERTED)
            existing = self.get_standing_head(head.source_assertion_ref)
            if isinstance(existing, PortError):
                return existing
            if isinstance(existing.value, RecordFound) and existing.value.record == head:
                return PortSuccess(InsertDisposition.ALREADY_PRESENT_SAME)
            return PortSuccess(InsertDisposition.CONFLICTING_EXISTING)
        except SQLAlchemyError as error:
            return technical_error(error)

    def compare_and_swap_standing_head(
        self,
        source_assertion_ref: SourceAssertionRef,
        expected_witness: StateWitness,
        latest_history_fact_ref: AssertionHistoryFactRef | None,
        new_witness: StateWitness,
    ) -> PortResult[ConditionalWriteDisposition]:
        try:
            result = self._connection.execute(
                update(assertions_standing_head)
                .where(
                    and_(
                        assertions_standing_head.c.source_assertion_ref
                        == source_assertion_ref.token,
                        assertions_standing_head.c.state_witness == expected_witness.value,
                    )
                )
                .values(
                    latest_history_fact_ref=None
                    if latest_history_fact_ref is None
                    else latest_history_fact_ref.value,
                    state_witness=new_witness.value,
                )
            )
            return PortSuccess(
                ConditionalWriteDisposition.APPLIED
                if result.rowcount == 1
                else ConditionalWriteDisposition.PRECONDITION_NOT_MET
            )
        except SQLAlchemyError as error:
            return technical_error(error)
