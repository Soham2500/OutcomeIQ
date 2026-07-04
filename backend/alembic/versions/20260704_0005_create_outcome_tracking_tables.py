"""Create outcome tracking tables.

Revision ID: 0005_outcome_tracking
Revises: 0004_cost_calculation
Create Date: 2026-07-04
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0005_outcome_tracking"
down_revision: str | None = "0004_cost_calculation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def timestamp_columns() -> tuple[sa.Column, sa.Column]:
    """Return shared mutable-record timestamp columns."""

    return (
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )


def upgrade() -> None:
    """Create the two approved outcome tracking tables."""

    op.create_table(
        "outcome_contracts",
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_id", sa.Uuid(), nullable=True),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "success_criteria_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column(
            "success_window_hours",
            sa.Integer(),
            server_default=sa.text("48"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default=sa.text("'active'"),
            nullable=False,
        ),
        sa.Column("created_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name="fk_outcome_contracts_project_id_projects",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["workflow_id"],
            ["workflows.id"],
            name="fk_outcome_contracts_workflow_id_workflows",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["created_by_user_id"],
            ["users.id"],
            name="fk_outcome_contracts_created_by_user_id_users",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "project_id",
            "name",
            name="uq_outcome_contracts_project_name",
        ),
    )
    op.create_index(
        "ix_outcome_contracts_project_id",
        "outcome_contracts",
        ["project_id"],
    )
    op.create_index(
        "ix_outcome_contracts_workflow_id",
        "outcome_contracts",
        ["workflow_id"],
    )
    op.create_index(
        "ix_outcome_contracts_status",
        "outcome_contracts",
        ["status"],
    )

    op.create_table(
        "workflow_run_outcomes",
        sa.Column("workflow_run_id", sa.Uuid(), nullable=False),
        sa.Column("outcome_contract_id", sa.Uuid(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default=sa.text("'pending'"),
            nullable=False,
        ),
        sa.Column(
            "verification_source",
            sa.String(length=20),
            server_default=sa.text("'manual'"),
            nullable=False,
        ),
        sa.Column(
            "outcome_score",
            sa.Numeric(precision=10, scale=4),
            nullable=True,
        ),
        sa.Column(
            "business_value_usd",
            sa.Numeric(precision=18, scale=8),
            nullable=True,
        ),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "metadata_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(
            ["workflow_run_id"],
            ["workflow_runs.id"],
            name="fk_workflow_run_outcomes_workflow_run_id_workflow_runs",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["outcome_contract_id"],
            ["outcome_contracts.id"],
            name="fk_run_outcomes_contract_id_outcome_contracts",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "workflow_run_id",
            name="uq_workflow_run_outcomes_workflow_run_id",
        ),
    )
    op.create_index(
        "ix_workflow_run_outcomes_workflow_run_id",
        "workflow_run_outcomes",
        ["workflow_run_id"],
    )
    op.create_index(
        "ix_workflow_run_outcomes_outcome_contract_id",
        "workflow_run_outcomes",
        ["outcome_contract_id"],
    )
    op.create_index(
        "ix_workflow_run_outcomes_status",
        "workflow_run_outcomes",
        ["status"],
    )
    op.create_index(
        "ix_workflow_run_outcomes_verified_at",
        "workflow_run_outcomes",
        ["verified_at"],
    )


def downgrade() -> None:
    """Drop outcome tracking tables in reverse dependency order."""

    op.drop_table("workflow_run_outcomes")
    op.drop_table("outcome_contracts")
