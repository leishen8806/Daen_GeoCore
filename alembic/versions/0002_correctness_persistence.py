"""add committed idempotency and mutation audit correctness persistence"""

import sqlalchemy as sa
from alembic import op

revision = "0002_correctness_persistence"
down_revision = "0001_authoritative_persistence"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "mutation_committed_binding",
        sa.Column("client_identity", sa.Text(), nullable=False),
        sa.Column("request_identity", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("operation_key", sa.Text(), nullable=False),
        sa.Column("retention_class", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint(
            "client_identity", "request_identity", name="pk_mutation_committed_binding"
        ),
    )
    op.create_table(
        "mutation_committed_result_reference",
        sa.Column("client_identity", sa.Text(), nullable=False),
        sa.Column("request_identity", sa.Text(), nullable=False),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("reference_kind", sa.Text(), nullable=False),
        sa.Column("reference_token", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_identity", "request_identity"],
            [
                "mutation_committed_binding.client_identity",
                "mutation_committed_binding.request_identity",
            ],
        ),
        sa.PrimaryKeyConstraint(
            "client_identity", "request_identity", "ordinal", name="pk_mutation_result_reference"
        ),
    )
    op.create_table(
        "mutation_committed_replay_metadata",
        sa.Column("client_identity", sa.Text(), nullable=False),
        sa.Column("request_identity", sa.Text(), nullable=False),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("metadata_key", sa.Text(), nullable=False),
        sa.Column("metadata_value", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["client_identity", "request_identity"],
            [
                "mutation_committed_binding.client_identity",
                "mutation_committed_binding.request_identity",
            ],
        ),
        sa.PrimaryKeyConstraint(
            "client_identity", "request_identity", "ordinal", name="pk_mutation_replay_metadata"
        ),
    )
    op.create_table(
        "mutation_audit",
        sa.Column("client_identity", sa.Text(), nullable=False),
        sa.Column("request_identity", sa.Text(), nullable=False),
        sa.Column("intent_fingerprint", sa.Text(), nullable=False),
        sa.Column("operation_key", sa.Text(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("mutation_provenance_encoding", sa.Text(), nullable=False),
        sa.Column("mutation_provenance_payload", sa.LargeBinary(), nullable=False),
        sa.Column("audit_details_encoding", sa.Text(), nullable=False),
        sa.Column("audit_details_payload", sa.LargeBinary(), nullable=False),
        sa.PrimaryKeyConstraint("client_identity", "request_identity", name="pk_mutation_audit"),
    )


def downgrade() -> None:
    op.drop_table("mutation_audit")
    op.drop_table("mutation_committed_replay_metadata")
    op.drop_table("mutation_committed_result_reference")
    op.drop_table("mutation_committed_binding")
