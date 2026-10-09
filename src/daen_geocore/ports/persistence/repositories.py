from typing import Protocol

from daen_geocore.domain.references import PlaceRef, SelectionRecordRef, SourceAssertionRef
from daen_geocore.ports.persistence.records import (
    AssertionHistoryFact,
    AssertionHistoryFactRef,
    AssertionStandingHead,
    ConditionalWriteDisposition,
    InsertDisposition,
    PlaceHead,
    PlaceHistoryFact,
    PlaceHistoryFactRef,
    PlaceIdentityRecord,
    RecordAbsent,
    RecordFound,
    SelectionRecord,
    SelectionSlotHead,
    SelectionSlotKey,
    SourceAssertionRecord,
    StateWitness,
)
from daen_geocore.ports.result import PortResult


class IdentityRepository(Protocol):
    def get_place(
        self, place_ref: PlaceRef
    ) -> PortResult[RecordFound[PlaceIdentityRecord] | RecordAbsent]: ...

    def get_place_head(
        self, place_ref: PlaceRef
    ) -> PortResult[RecordFound[PlaceHead] | RecordAbsent]: ...

    def list_place_history(
        self, place_ref: PlaceRef
    ) -> PortResult[tuple[PlaceHistoryFact, ...]]: ...

    def insert_place_if_absent(
        self, record: PlaceIdentityRecord
    ) -> PortResult[InsertDisposition]: ...

    def append_place_history_if_absent(
        self, fact: PlaceHistoryFact
    ) -> PortResult[InsertDisposition]: ...

    def insert_place_head_if_absent(self, head: PlaceHead) -> PortResult[InsertDisposition]: ...

    def compare_and_swap_place_head(
        self,
        place_ref: PlaceRef,
        expected_witness: StateWitness,
        latest_history_fact_ref: PlaceHistoryFactRef | None,
        new_witness: StateWitness,
    ) -> PortResult[ConditionalWriteDisposition]: ...


class AssertionsRepository(Protocol):
    def get_assertion(
        self, source_assertion_ref: SourceAssertionRef
    ) -> PortResult[RecordFound[SourceAssertionRecord] | RecordAbsent]: ...

    def list_assertions_for_place(
        self, place_ref: PlaceRef
    ) -> PortResult[tuple[SourceAssertionRecord, ...]]: ...

    def list_assertions_for_place_fact(
        self, place_ref: PlaceRef, fact_purpose: str
    ) -> PortResult[tuple[SourceAssertionRecord, ...]]: ...

    def list_assertion_history(
        self, source_assertion_ref: SourceAssertionRef
    ) -> PortResult[tuple[AssertionHistoryFact, ...]]: ...

    def get_standing_head(
        self, source_assertion_ref: SourceAssertionRef
    ) -> PortResult[RecordFound[AssertionStandingHead] | RecordAbsent]: ...

    def insert_assertion_if_absent(
        self, record: SourceAssertionRecord
    ) -> PortResult[InsertDisposition]: ...

    def append_assertion_history_if_absent(
        self, fact: AssertionHistoryFact
    ) -> PortResult[InsertDisposition]: ...

    def insert_standing_head_if_absent(
        self, head: AssertionStandingHead
    ) -> PortResult[InsertDisposition]: ...

    def compare_and_swap_standing_head(
        self,
        source_assertion_ref: SourceAssertionRef,
        expected_witness: StateWitness,
        latest_history_fact_ref: AssertionHistoryFactRef | None,
        new_witness: StateWitness,
    ) -> PortResult[ConditionalWriteDisposition]: ...


class RepresentationRepository(Protocol):
    def get_selection_record(
        self, selection_record_ref: SelectionRecordRef
    ) -> PortResult[RecordFound[SelectionRecord] | RecordAbsent]: ...

    def list_selection_records_for_place(
        self, place_ref: PlaceRef
    ) -> PortResult[tuple[SelectionRecord, ...]]: ...

    def list_supporting_assertion_refs(
        self, selection_record_ref: SelectionRecordRef
    ) -> PortResult[tuple[SourceAssertionRef, ...]]: ...

    def get_selection_slot_head(
        self, slot: SelectionSlotKey
    ) -> PortResult[RecordFound[SelectionSlotHead] | RecordAbsent]: ...

    def insert_selection_record_if_absent(
        self, record: SelectionRecord
    ) -> PortResult[InsertDisposition]: ...

    def insert_support_link_if_absent(
        self, selection_record_ref: SelectionRecordRef, source_assertion_ref: SourceAssertionRef
    ) -> PortResult[InsertDisposition]: ...

    def insert_selection_slot_head_if_absent(
        self, head: SelectionSlotHead
    ) -> PortResult[InsertDisposition]: ...

    def compare_and_swap_selection_slot_head(
        self,
        slot: SelectionSlotKey,
        expected_selection_record_ref: SelectionRecordRef,
        expected_witness: StateWitness,
        new_selection_record_ref: SelectionRecordRef,
        new_witness: StateWitness,
    ) -> PortResult[ConditionalWriteDisposition]: ...
