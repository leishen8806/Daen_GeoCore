from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    LargeBinary,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    Text,
    UniqueConstraint,
)

from .metadata import metadata

correctness_metadata = MetaData()


def _scope_columns() -> list[Column[Any]]:
    return [
        Column("scope_is_explicit", Boolean, nullable=False),
        Column("scope_type_id", Text),
        Column("scope_encoding", Text),
        Column("scope_payload", LargeBinary),
        Column("scope_equality_key", LargeBinary),
    ]


def _quality_columns() -> list[Column[Any]]:
    return [
        Column("quality_is_known", Boolean, nullable=False),
        Column("quality_encoding", Text),
        Column("quality_payload", LargeBinary),
    ]


def _scope_check(name: str) -> CheckConstraint:
    return CheckConstraint(
        "(scope_is_explicit = false AND scope_type_id IS NULL AND scope_encoding IS NULL "
        "AND scope_payload IS NULL AND scope_equality_key IS NULL) "
        "OR (scope_is_explicit = true AND scope_type_id IS NOT NULL "
        "AND scope_encoding IS NOT NULL AND scope_payload IS NOT NULL)",
        name=name,
    )


def _quality_check(name: str) -> CheckConstraint:
    return CheckConstraint(
        "(quality_is_known = false AND quality_encoding IS NULL AND quality_payload IS NULL) "
        "OR (quality_is_known = true AND quality_encoding IS NOT NULL "
        "AND quality_payload IS NOT NULL)",
        name=name,
    )


identity_place = Table(
    "identity_place",
    metadata,
    Column("place_ref", Text, nullable=False),
    Column("recorded_at", DateTime(timezone=True), nullable=False),
    PrimaryKeyConstraint("place_ref", name="pk_identity_place"),
)

identity_place_history = Table(
    "identity_place_history",
    metadata,
    Column("history_fact_ref", Text, nullable=False),
    Column("place_ref", Text, nullable=False),
    Column("fact_type", Text, nullable=False),
    Column("recorded_at", DateTime(timezone=True), nullable=False),
    Column("history_metadata_encoding", Text),
    Column("history_metadata_payload", LargeBinary),
    ForeignKeyConstraint(["place_ref"], ["identity_place.place_ref"]),
    CheckConstraint(
        "(history_metadata_encoding IS NULL AND history_metadata_payload IS NULL) "
        "OR (history_metadata_encoding IS NOT NULL AND history_metadata_payload IS NOT NULL)",
        name="ck_identity_place_history_metadata_pair",
    ),
    PrimaryKeyConstraint("history_fact_ref", name="pk_identity_place_history"),
)
Index(
    "ix_identity_place_history_place_recorded_at",
    identity_place_history.c.place_ref,
    identity_place_history.c.recorded_at,
)

identity_place_head = Table(
    "identity_place_head",
    metadata,
    Column("place_ref", Text, nullable=False),
    Column("latest_history_fact_ref", Text),
    Column("state_witness", Text, nullable=False),
    ForeignKeyConstraint(["place_ref"], ["identity_place.place_ref"]),
    ForeignKeyConstraint(["latest_history_fact_ref"], ["identity_place_history.history_fact_ref"]),
    PrimaryKeyConstraint("place_ref", name="pk_identity_place_head"),
)

assertions_source_assertion = Table(
    "assertions_source_assertion",
    metadata,
    Column("source_assertion_ref", Text, nullable=False),
    Column("place_ref", Text, nullable=False),
    Column("fact_purpose", Text, nullable=False),
    Column("value_type_id", Text, nullable=False),
    Column("value_encoding", Text, nullable=False),
    Column("value_payload", LargeBinary, nullable=False),
    *_scope_columns(),
    Column("provenance_encoding", Text, nullable=False),
    Column("provenance_payload", LargeBinary, nullable=False),
    *_quality_columns(),
    Column("recorded_at", DateTime(timezone=True), nullable=False),
    _scope_check("ck_assertions_source_assertion_scope_envelope"),
    _quality_check("ck_assertions_source_assertion_quality_envelope"),
    PrimaryKeyConstraint("source_assertion_ref", name="pk_assertions_source_assertion"),
)
Index("ix_assertions_source_assertion_place", assertions_source_assertion.c.place_ref)
Index(
    "ix_assertions_source_assertion_place_fact",
    assertions_source_assertion.c.place_ref,
    assertions_source_assertion.c.fact_purpose,
)

assertions_history = Table(
    "assertions_history",
    metadata,
    Column("history_fact_ref", Text, nullable=False),
    Column("source_assertion_ref", Text, nullable=False),
    Column("fact_type", Text, nullable=False),
    Column("related_source_assertion_ref", Text),
    Column("recorded_at", DateTime(timezone=True), nullable=False),
    Column("history_metadata_encoding", Text),
    Column("history_metadata_payload", LargeBinary),
    ForeignKeyConstraint(
        ["source_assertion_ref"], ["assertions_source_assertion.source_assertion_ref"]
    ),
    ForeignKeyConstraint(
        ["related_source_assertion_ref"],
        ["assertions_source_assertion.source_assertion_ref"],
    ),
    CheckConstraint(
        "(history_metadata_encoding IS NULL AND history_metadata_payload IS NULL) "
        "OR (history_metadata_encoding IS NOT NULL AND history_metadata_payload IS NOT NULL)",
        name="ck_assertions_history_metadata_pair",
    ),
    PrimaryKeyConstraint("history_fact_ref", name="pk_assertions_history"),
)
Index(
    "ix_assertions_history_assertion_recorded_at",
    assertions_history.c.source_assertion_ref,
    assertions_history.c.recorded_at,
)

assertions_standing_head = Table(
    "assertions_standing_head",
    metadata,
    Column("source_assertion_ref", Text, nullable=False),
    Column("latest_history_fact_ref", Text),
    Column("state_witness", Text, nullable=False),
    ForeignKeyConstraint(
        ["source_assertion_ref"],
        ["assertions_source_assertion.source_assertion_ref"],
    ),
    ForeignKeyConstraint(
        ["latest_history_fact_ref"],
        ["assertions_history.history_fact_ref"],
    ),
    PrimaryKeyConstraint("source_assertion_ref", name="pk_assertions_standing_head"),
)

representation_selection_record = Table(
    "representation_selection_record",
    metadata,
    Column("selection_record_ref", Text, nullable=False),
    Column("place_ref", Text, nullable=False),
    Column("fact_purpose", Text, nullable=False),
    Column("value_type_id", Text, nullable=False),
    Column("value_encoding", Text, nullable=False),
    Column("value_payload", LargeBinary, nullable=False),
    *_scope_columns(),
    Column("selection_attribution_encoding", Text, nullable=False),
    Column("selection_attribution_payload", LargeBinary, nullable=False),
    Column("provenance_encoding", Text, nullable=False),
    Column("provenance_payload", LargeBinary, nullable=False),
    *_quality_columns(),
    Column("recorded_at", DateTime(timezone=True), nullable=False),
    _scope_check("ck_representation_selection_record_scope_envelope"),
    _quality_check("ck_representation_selection_record_quality_envelope"),
    PrimaryKeyConstraint("selection_record_ref", name="pk_representation_selection_record"),
)
Index("ix_representation_selection_record_place", representation_selection_record.c.place_ref)

representation_selection_support = Table(
    "representation_selection_support",
    metadata,
    Column("selection_record_ref", Text, nullable=False),
    Column("source_assertion_ref", Text, nullable=False),
    ForeignKeyConstraint(
        ["selection_record_ref"],
        ["representation_selection_record.selection_record_ref"],
    ),
    UniqueConstraint(
        "selection_record_ref",
        "source_assertion_ref",
        name="uq_selection_support_record_assertion",
    ),
)

representation_selection_slot_head = Table(
    "representation_selection_slot_head",
    metadata,
    Column("place_ref", Text, nullable=False),
    Column("fact_purpose", Text, nullable=False),
    Column("scope_type_id", Text, nullable=False),
    Column("scope_equality_key", LargeBinary, nullable=False),
    Column("selection_record_ref", Text, nullable=False),
    Column("state_witness", Text, nullable=False),
    ForeignKeyConstraint(
        ["selection_record_ref"],
        ["representation_selection_record.selection_record_ref"],
    ),
    PrimaryKeyConstraint(
        "place_ref",
        "fact_purpose",
        "scope_type_id",
        "scope_equality_key",
        name="pk_representation_selection_slot_head",
    ),
)


mutation_committed_binding = Table(
    "mutation_committed_binding",
    correctness_metadata,
    Column("client_identity", Text, nullable=False),
    Column("request_identity", Text, nullable=False),
    Column("intent_fingerprint", Text, nullable=False),
    Column("operation_key", Text, nullable=False),
    Column("retention_class", Text, nullable=False),
    PrimaryKeyConstraint(
        "client_identity", "request_identity", name="pk_mutation_committed_binding"
    ),
)

mutation_committed_result_reference = Table(
    "mutation_committed_result_reference",
    correctness_metadata,
    Column("client_identity", Text, nullable=False),
    Column("request_identity", Text, nullable=False),
    Column("ordinal", Integer, nullable=False),
    Column("reference_kind", Text, nullable=False),
    Column("reference_token", Text, nullable=False),
    ForeignKeyConstraint(
        ["client_identity", "request_identity"],
        [
            "mutation_committed_binding.client_identity",
            "mutation_committed_binding.request_identity",
        ],
    ),
    PrimaryKeyConstraint(
        "client_identity", "request_identity", "ordinal", name="pk_mutation_result_reference"
    ),
)

mutation_committed_replay_metadata = Table(
    "mutation_committed_replay_metadata",
    correctness_metadata,
    Column("client_identity", Text, nullable=False),
    Column("request_identity", Text, nullable=False),
    Column("ordinal", Integer, nullable=False),
    Column("metadata_key", Text, nullable=False),
    Column("metadata_value", Text, nullable=False),
    ForeignKeyConstraint(
        ["client_identity", "request_identity"],
        [
            "mutation_committed_binding.client_identity",
            "mutation_committed_binding.request_identity",
        ],
    ),
    PrimaryKeyConstraint(
        "client_identity", "request_identity", "ordinal", name="pk_mutation_replay_metadata"
    ),
)

mutation_audit = Table(
    "mutation_audit",
    correctness_metadata,
    Column("client_identity", Text, nullable=False),
    Column("request_identity", Text, nullable=False),
    Column("intent_fingerprint", Text, nullable=False),
    Column("operation_key", Text, nullable=False),
    Column("recorded_at", DateTime(timezone=True), nullable=False),
    Column("mutation_provenance_encoding", Text, nullable=False),
    Column("mutation_provenance_payload", LargeBinary, nullable=False),
    Column("audit_details_encoding", Text, nullable=False),
    Column("audit_details_payload", LargeBinary, nullable=False),
    PrimaryKeyConstraint("client_identity", "request_identity", name="pk_mutation_audit"),
)

ALL_CORRECTNESS_TABLES = (
    mutation_committed_binding,
    mutation_committed_result_reference,
    mutation_committed_replay_metadata,
    mutation_audit,
)

ALL_TABLES = (
    identity_place,
    identity_place_history,
    identity_place_head,
    assertions_source_assertion,
    assertions_history,
    assertions_standing_head,
    representation_selection_record,
    representation_selection_support,
    representation_selection_slot_head,
)
