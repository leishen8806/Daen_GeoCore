from sqlalchemy import Connection, and_, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError

from daen_geocore.domain.references import PlaceRef
from daen_geocore.infrastructure.postgres.schema import (
    identity_place,
    identity_place_head,
    identity_place_history,
)
from daen_geocore.ports.persistence.records import (
    ConditionalWriteDisposition,
    InsertDisposition,
    PlaceHead,
    PlaceHistoryFact,
    PlaceHistoryFactRef,
    PlaceIdentityRecord,
    RecordAbsent,
    RecordFound,
    StateWitness,
)
from daen_geocore.ports.result import PortError, PortResult, PortSuccess

from .common import metadata_from_row, technical_error


class PostgresIdentityRepository:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    def get_place(
        self, place_ref: PlaceRef
    ) -> PortResult[RecordFound[PlaceIdentityRecord] | RecordAbsent]:
        try:
            row = (
                self._connection.execute(
                    select(identity_place).where(identity_place.c.place_ref == place_ref.token)
                )
                .mappings()
                .first()
            )
            if row is None:
                return PortSuccess(RecordAbsent())
            return PortSuccess(
                RecordFound(PlaceIdentityRecord(PlaceRef(row["place_ref"]), row["recorded_at"]))
            )
        except SQLAlchemyError as error:
            return technical_error(error)

    def get_place_head(
        self, place_ref: PlaceRef
    ) -> PortResult[RecordFound[PlaceHead] | RecordAbsent]:
        try:
            row = (
                self._connection.execute(
                    select(identity_place_head).where(
                        identity_place_head.c.place_ref == place_ref.token
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
                else PlaceHistoryFactRef(row["latest_history_fact_ref"])
            )
            return PortSuccess(
                RecordFound(
                    PlaceHead(
                        PlaceRef(row["place_ref"]), latest, StateWitness(row["state_witness"])
                    )
                )
            )
        except SQLAlchemyError as error:
            return technical_error(error)

    def list_place_history(self, place_ref: PlaceRef) -> PortResult[tuple[PlaceHistoryFact, ...]]:
        try:
            rows = self._connection.execute(
                select(identity_place_history).where(
                    identity_place_history.c.place_ref == place_ref.token
                )
            ).mappings()
            facts = tuple(
                PlaceHistoryFact(
                    PlaceHistoryFactRef(row["history_fact_ref"]),
                    PlaceRef(row["place_ref"]),
                    row["fact_type"],
                    row["recorded_at"],
                    metadata_from_row(row),
                )
                for row in rows
            )
            return PortSuccess(facts)
        except SQLAlchemyError as error:
            return technical_error(error)

    def insert_place_if_absent(self, record: PlaceIdentityRecord) -> PortResult[InsertDisposition]:
        try:
            statement = (
                pg_insert(identity_place)
                .values(place_ref=record.place_ref.token, recorded_at=record.recorded_at)
                .on_conflict_do_nothing(index_elements=[identity_place.c.place_ref])
                .returning(identity_place.c.place_ref)
            )
            if self._connection.execute(statement).first() is not None:
                return PortSuccess(InsertDisposition.INSERTED)
            existing = self.get_place(record.place_ref)
            if isinstance(existing, PortError):
                return existing
            if isinstance(existing.value, RecordFound) and existing.value.record == record:
                return PortSuccess(InsertDisposition.ALREADY_PRESENT_SAME)
            return PortSuccess(InsertDisposition.CONFLICTING_EXISTING)
        except SQLAlchemyError as error:
            return technical_error(error)

    def append_place_history_if_absent(
        self, fact: PlaceHistoryFact
    ) -> PortResult[InsertDisposition]:
        values = {
            "history_fact_ref": fact.history_fact_ref.value,
            "place_ref": fact.place_ref.token,
            "fact_type": fact.fact_type,
            "recorded_at": fact.recorded_at,
            "history_metadata_encoding": None
            if fact.metadata is None
            else fact.metadata.encoding_id,
            "history_metadata_payload": None if fact.metadata is None else fact.metadata.payload,
        }
        try:
            statement = (
                pg_insert(identity_place_history)
                .values(values)
                .on_conflict_do_nothing(index_elements=[identity_place_history.c.history_fact_ref])
                .returning(identity_place_history.c.history_fact_ref)
            )
            if self._connection.execute(statement).first() is not None:
                return PortSuccess(InsertDisposition.INSERTED)
            existing = (
                self._connection.execute(
                    select(identity_place_history).where(
                        identity_place_history.c.history_fact_ref == fact.history_fact_ref.value
                    )
                )
                .mappings()
                .first()
            )
            if existing is None:
                return PortError(
                    technical_error(RuntimeError("insert race left no history row")).failure
                )
            same = (
                existing.place_ref == fact.place_ref.token
                and existing.fact_type == fact.fact_type
                and existing.recorded_at == fact.recorded_at
                and metadata_from_row(existing) == fact.metadata
            )
            return PortSuccess(
                InsertDisposition.ALREADY_PRESENT_SAME
                if same
                else InsertDisposition.CONFLICTING_EXISTING
            )
        except SQLAlchemyError as error:
            return technical_error(error)

    def insert_place_head_if_absent(self, head: PlaceHead) -> PortResult[InsertDisposition]:
        values = {
            "place_ref": head.place_ref.token,
            "latest_history_fact_ref": None
            if head.latest_history_fact_ref is None
            else head.latest_history_fact_ref.value,
            "state_witness": head.state_witness.value,
        }
        try:
            statement = (
                pg_insert(identity_place_head)
                .values(values)
                .on_conflict_do_nothing(index_elements=[identity_place_head.c.place_ref])
                .returning(identity_place_head.c.place_ref)
            )
            if self._connection.execute(statement).first() is not None:
                return PortSuccess(InsertDisposition.INSERTED)
            existing = self.get_place_head(head.place_ref)
            if isinstance(existing, PortError):
                return existing
            if isinstance(existing.value, RecordFound) and existing.value.record == head:
                return PortSuccess(InsertDisposition.ALREADY_PRESENT_SAME)
            return PortSuccess(InsertDisposition.CONFLICTING_EXISTING)
        except SQLAlchemyError as error:
            return technical_error(error)

    def compare_and_swap_place_head(
        self,
        place_ref: PlaceRef,
        expected_witness: StateWitness,
        latest_history_fact_ref: PlaceHistoryFactRef | None,
        new_witness: StateWitness,
    ) -> PortResult[ConditionalWriteDisposition]:
        try:
            result = self._connection.execute(
                update(identity_place_head)
                .where(
                    and_(
                        identity_place_head.c.place_ref == place_ref.token,
                        identity_place_head.c.state_witness == expected_witness.value,
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
