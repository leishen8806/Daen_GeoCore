"""Create the Step-5 authoritative persistence structures.

Revision ID: 0001_authoritative_persistence
Revises:
"""

import sqlalchemy as sa
from alembic import op

revision = "0001_authoritative_persistence"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "identity_place",
        sa.Column("place_ref", sa.Text(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("place_ref", name="pk_identity_place"),
    )
    op.create_table(
        "identity_place_history",
        sa.Column("history_fact_ref", sa.Text(), nullable=False),
        sa.Column("place_ref", sa.Text(), nullable=False),
        sa.Column("fact_type", sa.Text(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("history_metadata_encoding", sa.Text()),
        sa.Column("history_metadata_payload", sa.LargeBinary()),
        sa.CheckConstraint(
            "(history_metadata_encoding IS NULL AND history_metadata_payload IS NULL) "
            "OR (history_metadata_encoding IS NOT NULL AND history_metadata_payload IS NOT NULL)",
            name="ck_identity_place_history_metadata_pair",
        ),
        sa.ForeignKeyConstraint(["place_ref"], ["identity_place.place_ref"]),
        sa.PrimaryKeyConstraint("history_fact_ref", name="pk_identity_place_history"),
    )
    op.create_index(
        "ix_identity_place_history_place_recorded_at",
        "identity_place_history",
        ["place_ref", "recorded_at"],
    )
    op.create_table(
        "identity_place_head",
        sa.Column("place_ref", sa.Text(), nullable=False),
        sa.Column("latest_history_fact_ref", sa.Text()),
        sa.Column("state_witness", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["latest_history_fact_ref"], ["identity_place_history.history_fact_ref"]
        ),
        sa.ForeignKeyConstraint(["place_ref"], ["identity_place.place_ref"]),
        sa.PrimaryKeyConstraint("place_ref", name="pk_identity_place_head"),
    )
    op.create_table(
        "assertions_source_assertion",
        sa.Column("source_assertion_ref", sa.Text(), nullable=False),
        sa.Column("place_ref", sa.Text(), nullable=False),
        sa.Column("fact_purpose", sa.Text(), nullable=False),
        sa.Column("value_type_id", sa.Text(), nullable=False),
        sa.Column("value_encoding", sa.Text(), nullable=False),
        sa.Column("value_payload", sa.LargeBinary(), nullable=False),
        sa.Column("scope_is_explicit", sa.Boolean(), nullable=False),
        sa.Column("scope_type_id", sa.Text()),
        sa.Column("scope_encoding", sa.Text()),
        sa.Column("scope_payload", sa.LargeBinary()),
        sa.Column("scope_equality_key", sa.LargeBinary()),
        sa.Column("provenance_encoding", sa.Text(), nullable=False),
        sa.Column("provenance_payload", sa.LargeBinary(), nullable=False),
        sa.Column("quality_is_known", sa.Boolean(), nullable=False),
        sa.Column("quality_encoding", sa.Text()),
        sa.Column("quality_payload", sa.LargeBinary()),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "(scope_is_explicit = false AND scope_type_id IS NULL AND scope_encoding IS NULL "
            "AND scope_payload IS NULL AND scope_equality_key IS NULL) "
            "OR (scope_is_explicit = true AND scope_type_id IS NOT NULL "
            "AND scope_encoding IS NOT NULL AND scope_payload IS NOT NULL)",
            name="ck_assertions_source_assertion_scope_envelope",
        ),
        sa.CheckConstraint(
            "(quality_is_known = false AND quality_encoding IS NULL AND quality_payload IS NULL) "
            "OR (quality_is_known = true AND quality_encoding IS NOT NULL "
            "AND quality_payload IS NOT NULL)",
            name="ck_assertions_source_assertion_quality_envelope",
        ),
        sa.PrimaryKeyConstraint("source_assertion_ref", name="pk_assertions_source_assertion"),
    )
    op.create_index(
        "ix_assertions_source_assertion_place", "assertions_source_assertion", ["place_ref"]
    )
    op.create_index(
        "ix_assertions_source_assertion_place_fact",
        "assertions_source_assertion",
        ["place_ref", "fact_purpose"],
    )
    op.create_table(
        "assertions_history",
        sa.Column("history_fact_ref", sa.Text(), nullable=False),
        sa.Column("source_assertion_ref", sa.Text(), nullable=False),
        sa.Column("fact_type", sa.Text(), nullable=False),
        sa.Column("related_source_assertion_ref", sa.Text()),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("history_metadata_encoding", sa.Text()),
        sa.Column("history_metadata_payload", sa.LargeBinary()),
        sa.CheckConstraint(
            "(history_metadata_encoding IS NULL AND history_metadata_payload IS NULL) "
            "OR (history_metadata_encoding IS NOT NULL AND history_metadata_payload IS NOT NULL)",
            name="ck_assertions_history_metadata_pair",
        ),
        sa.ForeignKeyConstraint(
            ["related_source_assertion_ref"], ["assertions_source_assertion.source_assertion_ref"]
        ),
        sa.ForeignKeyConstraint(
            ["source_assertion_ref"], ["assertions_source_assertion.source_assertion_ref"]
        ),
        sa.PrimaryKeyConstraint("history_fact_ref", name="pk_assertions_history"),
    )
    op.create_index(
        "ix_assertions_history_assertion_recorded_at",
        "assertions_history",
        ["source_assertion_ref", "recorded_at"],
    )
    op.create_table(
        "assertions_standing_head",
        sa.Column("source_assertion_ref", sa.Text(), nullable=False),
        sa.Column("latest_history_fact_ref", sa.Text()),
        sa.Column("state_witness", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["latest_history_fact_ref"], ["assertions_history.history_fact_ref"]
        ),
        sa.ForeignKeyConstraint(
            ["source_assertion_ref"], ["assertions_source_assertion.source_assertion_ref"]
        ),
        sa.PrimaryKeyConstraint("source_assertion_ref", name="pk_assertions_standing_head"),
    )
    op.create_table(
        "representation_selection_record",
        sa.Column("selection_record_ref", sa.Text(), nullable=False),
        sa.Column("place_ref", sa.Text(), nullable=False),
        sa.Column("fact_purpose", sa.Text(), nullable=False),
        sa.Column("value_type_id", sa.Text(), nullable=False),
        sa.Column("value_encoding", sa.Text(), nullable=False),
        sa.Column("value_payload", sa.LargeBinary(), nullable=False),
        sa.Column("scope_is_explicit", sa.Boolean(), nullable=False),
        sa.Column("scope_type_id", sa.Text()),
        sa.Column("scope_encoding", sa.Text()),
        sa.Column("scope_payload", sa.LargeBinary()),
        sa.Column("scope_equality_key", sa.LargeBinary()),
        sa.Column("selection_attribution_encoding", sa.Text(), nullable=False),
        sa.Column("selection_attribution_payload", sa.LargeBinary(), nullable=False),
        sa.Column("provenance_encoding", sa.Text(), nullable=False),
        sa.Column("provenance_payload", sa.LargeBinary(), nullable=False),
        sa.Column("quality_is_known", sa.Boolean(), nullable=False),
        sa.Column("quality_encoding", sa.Text()),
        sa.Column("quality_payload", sa.LargeBinary()),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "(scope_is_explicit = false AND scope_type_id IS NULL AND scope_encoding IS NULL "
            "AND scope_payload IS NULL AND scope_equality_key IS NULL) "
            "OR (scope_is_explicit = true AND scope_type_id IS NOT NULL "
            "AND scope_encoding IS NOT NULL AND scope_payload IS NOT NULL)",
            name="ck_representation_selection_record_scope_envelope",
        ),
        sa.CheckConstraint(
            "(quality_is_known = false AND quality_encoding IS NULL AND quality_payload IS NULL) "
            "OR (quality_is_known = true AND quality_encoding IS NOT NULL "
            "AND quality_payload IS NOT NULL)",
            name="ck_representation_selection_record_quality_envelope",
        ),
        sa.PrimaryKeyConstraint("selection_record_ref", name="pk_representation_selection_record"),
    )
    op.create_index(
        "ix_representation_selection_record_place",
        "representation_selection_record",
        ["place_ref"],
    )
    op.create_table(
        "representation_selection_support",
        sa.Column("selection_record_ref", sa.Text(), nullable=False),
        sa.Column("source_assertion_ref", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["selection_record_ref"],
            ["representation_selection_record.selection_record_ref"],
        ),
        sa.UniqueConstraint(
            "selection_record_ref",
            "source_assertion_ref",
            name="uq_selection_support_record_assertion",
        ),
    )
    op.create_table(
        "representation_selection_slot_head",
        sa.Column("place_ref", sa.Text(), nullable=False),
        sa.Column("fact_purpose", sa.Text(), nullable=False),
        sa.Column("scope_type_id", sa.Text(), nullable=False),
        sa.Column("scope_equality_key", sa.LargeBinary(), nullable=False),
        sa.Column("selection_record_ref", sa.Text(), nullable=False),
        sa.Column("state_witness", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["selection_record_ref"],
            ["representation_selection_record.selection_record_ref"],
        ),
        sa.PrimaryKeyConstraint(
            "place_ref",
            "fact_purpose",
            "scope_type_id",
            "scope_equality_key",
            name="pk_representation_selection_slot_head",
        ),
    )


def downgrade() -> None:
    op.drop_table("representation_selection_slot_head")
    op.drop_table("representation_selection_support")
    op.drop_index(
        "ix_representation_selection_record_place", table_name="representation_selection_record"
    )
    op.drop_table("representation_selection_record")
    op.drop_table("assertions_standing_head")
    op.drop_index("ix_assertions_history_assertion_recorded_at", table_name="assertions_history")
    op.drop_table("assertions_history")
    op.drop_index(
        "ix_assertions_source_assertion_place_fact", table_name="assertions_source_assertion"
    )
    op.drop_index("ix_assertions_source_assertion_place", table_name="assertions_source_assertion")
    op.drop_table("assertions_source_assertion")
    op.drop_table("identity_place_head")
    op.drop_index(
        "ix_identity_place_history_place_recorded_at", table_name="identity_place_history"
    )
    op.drop_table("identity_place_history")
    op.drop_table("identity_place")
