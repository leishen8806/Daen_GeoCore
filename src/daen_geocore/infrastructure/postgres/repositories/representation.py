from collections.abc import Mapping
from typing import Any

from sqlalchemy import Connection, and_, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError

from daen_geocore.domain.references import PlaceRef, SelectionRecordRef, SourceAssertionRef
from daen_geocore.infrastructure.postgres.schema import (
    representation_selection_record,
    representation_selection_slot_head,
    representation_selection_support,
)
from daen_geocore.ports.persistence.records import (
    ConditionalWriteDisposition,
    InsertDisposition,
    OpaqueEncodedPayload,
    PersistedExplicitScope,
    PersistedQualityKnown,
    PersistedTypedValue,
    RecordAbsent,
    RecordFound,
    SelectionRecord,
    SelectionSlotHead,
    SelectionSlotKey,
    StateWitness,
)
from daen_geocore.ports.result import PortError, PortResult, PortSuccess

from .common import quality_from_row, scope_from_row, technical_error


class PostgresRepresentationRepository:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def _record(self, row: Mapping[Any, Any]) -> SelectionRecord:
        return SelectionRecord(
            SelectionRecordRef(row["selection_record_ref"]),
            PlaceRef(row["place_ref"]),
            row["fact_purpose"],
            PersistedTypedValue(
                row["value_type_id"],
                OpaqueEncodedPayload(row["value_encoding"], bytes(row["value_payload"])),
            ),
            scope_from_row(row),
            OpaqueEncodedPayload(
                row["selection_attribution_encoding"],
                bytes(row["selection_attribution_payload"]),
            ),
            OpaqueEncodedPayload(row["provenance_encoding"], bytes(row["provenance_payload"])),
            quality_from_row(row),
            row["recorded_at"],
        )

    def get_selection_record(
        self, selection_record_ref: SelectionRecordRef
    ) -> PortResult[RecordFound[SelectionRecord] | RecordAbsent]:
        try:
            row = (
                self._connection.execute(
                    select(representation_selection_record).where(
                        representation_selection_record.c.selection_record_ref
                        == selection_record_ref.token
                    )
                )
                .mappings()
                .first()
            )
            return PortSuccess(RecordAbsent() if row is None else RecordFound(self._record(row)))
        except SQLAlchemyError as error:
            return technical_error(error)

    def list_selection_records_for_place(
        self, place_ref: PlaceRef
    ) -> PortResult[tuple[SelectionRecord, ...]]:
        try:
            rows = self._connection.execute(
                select(representation_selection_record).where(
                    representation_selection_record.c.place_ref == place_ref.token
                )
            ).mappings()
            return PortSuccess(tuple(self._record(row) for row in rows))
        except SQLAlchemyError as error:
            return technical_error(error)

    def list_supporting_assertion_refs(
        self, selection_record_ref: SelectionRecordRef
    ) -> PortResult[tuple[SourceAssertionRef, ...]]:
        try:
            rows = self._connection.execute(
                select(representation_selection_support.c.source_assertion_ref).where(
                    representation_selection_support.c.selection_record_ref
                    == selection_record_ref.token
                )
            )
            return PortSuccess(tuple(SourceAssertionRef(row[0]) for row in rows))
        except SQLAlchemyError as error:
            return technical_error(error)

    def get_selection_slot_head(
        self, slot: SelectionSlotKey
    ) -> PortResult[RecordFound[SelectionSlotHead] | RecordAbsent]:
        try:
            row = (
                self._connection.execute(
                    select(representation_selection_slot_head).where(
                        and_(
                            representation_selection_slot_head.c.place_ref == slot.place_ref.token,
                            representation_selection_slot_head.c.fact_purpose == slot.fact_purpose,
                            representation_selection_slot_head.c.scope_type_id
                            == slot.scope_type_id,
                            representation_selection_slot_head.c.scope_equality_key
                            == slot.equality_key,
                        )
                    )
                )
                .mappings()
                .first()
            )
            if row is None:
                return PortSuccess(RecordAbsent())
            return PortSuccess(
                RecordFound(
                    SelectionSlotHead(
                        SelectionSlotKey(
                            PlaceRef(row["place_ref"]),
                            row["fact_purpose"],
                            row["scope_type_id"],
                            bytes(row["scope_equality_key"]),
                        ),
                        SelectionRecordRef(row["selection_record_ref"]),
                        StateWitness(row["state_witness"]),
                    )
                )
            )
        except SQLAlchemyError as error:
            return technical_error(error)

    def insert_selection_record_if_absent(
        self, record: SelectionRecord
    ) -> PortResult[InsertDisposition]:
        scope = record.scope
        quality = record.quality
        values = {
            "selection_record_ref": record.selection_record_ref.token,
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
            "selection_attribution_encoding": record.attribution.encoding_id,
            "selection_attribution_payload": record.attribution.payload,
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
        try:
            statement = (
                pg_insert(representation_selection_record)
                .values(values)
                .on_conflict_do_nothing(
                    index_elements=[representation_selection_record.c.selection_record_ref]
                )
            )
            if self._connection.execute(statement).rowcount == 1:
                return PortSuccess(InsertDisposition.INSERTED)
            existing = self.get_selection_record(record.selection_record_ref)
            if isinstance(existing, PortError):
                return existing
            if isinstance(existing.value, RecordFound) and existing.value.record == record:
                return PortSuccess(InsertDisposition.ALREADY_PRESENT_SAME)
            return PortSuccess(InsertDisposition.CONFLICTING_EXISTING)
        except SQLAlchemyError as error:
            return technical_error(error)

    def insert_support_link_if_absent(
        self,
        selection_record_ref: SelectionRecordRef,
        source_assertion_ref: SourceAssertionRef,
    ) -> PortResult[InsertDisposition]:
        values = {
            "selection_record_ref": selection_record_ref.token,
            "source_assertion_ref": source_assertion_ref.token,
        }
        try:
            statement = (
                pg_insert(representation_selection_support)
                .values(values)
                .on_conflict_do_nothing(
                    index_elements=[
                        representation_selection_support.c.selection_record_ref,
                        representation_selection_support.c.source_assertion_ref,
                    ]
                )
            )
            if self._connection.execute(statement).rowcount == 1:
                return PortSuccess(InsertDisposition.INSERTED)
            return PortSuccess(InsertDisposition.ALREADY_PRESENT_SAME)
        except SQLAlchemyError as error:
            return technical_error(error)

    def insert_selection_slot_head_if_absent(
        self, head: SelectionSlotHead
    ) -> PortResult[InsertDisposition]:
        values = {
            "place_ref": head.slot.place_ref.token,
            "fact_purpose": head.slot.fact_purpose,
            "scope_type_id": head.slot.scope_type_id,
            "scope_equality_key": head.slot.equality_key,
            "selection_record_ref": head.selection_record_ref.token,
            "state_witness": head.state_witness.value,
        }
        try:
            statement = (
                pg_insert(representation_selection_slot_head)
                .values(values)
                .on_conflict_do_nothing(
                    index_elements=[
                        representation_selection_slot_head.c.place_ref,
                        representation_selection_slot_head.c.fact_purpose,
                        representation_selection_slot_head.c.scope_type_id,
                        representation_selection_slot_head.c.scope_equality_key,
                    ]
                )
            )
            if self._connection.execute(statement).rowcount == 1:
                return PortSuccess(InsertDisposition.INSERTED)
            existing = self.get_selection_slot_head(head.slot)
            if isinstance(existing, PortError):
                return existing
            if isinstance(existing.value, RecordFound) and existing.value.record == head:
                return PortSuccess(InsertDisposition.ALREADY_PRESENT_SAME)
            return PortSuccess(InsertDisposition.CONFLICTING_EXISTING)
        except SQLAlchemyError as error:
            return technical_error(error)

    def compare_and_swap_selection_slot_head(
        self,
        slot: SelectionSlotKey,
        expected_selection_record_ref: SelectionRecordRef,
        expected_witness: StateWitness,
        new_selection_record_ref: SelectionRecordRef,
        new_witness: StateWitness,
    ) -> PortResult[ConditionalWriteDisposition]:
        try:
            result = self._connection.execute(
                update(representation_selection_slot_head)
                .where(
                    and_(
                        representation_selection_slot_head.c.place_ref == slot.place_ref.token,
                        representation_selection_slot_head.c.fact_purpose == slot.fact_purpose,
                        representation_selection_slot_head.c.scope_type_id == slot.scope_type_id,
                        representation_selection_slot_head.c.scope_equality_key
                        == slot.equality_key,
                        representation_selection_slot_head.c.selection_record_ref
                        == expected_selection_record_ref.token,
                        representation_selection_slot_head.c.state_witness
                        == expected_witness.value,
                    )
                )
                .values(
                    selection_record_ref=new_selection_record_ref.token,
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
