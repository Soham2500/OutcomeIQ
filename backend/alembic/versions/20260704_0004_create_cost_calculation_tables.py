"""Create cost calculation tables.

Revision ID: 0004_cost_calculation
Revises: 0003_workflow_logging
Create Date: 2026-07-04
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0004_cost_calculation"
down_revision: str | None = "0003_workflow_logging"
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
    """Create the two approved cost calculation tables."""

    op.create_table(
        "model_pricing_rates",
        sa.Column("provider", sa.String(length=80), nullable=False),
        sa.Column("model_name", sa.String(length=160), nullable=False),
        sa.Column(
            "currency",
            sa.String(length=3),
            server_default=sa.text("'USD'"),
            nullable=False,
        ),
        sa.Column(
            "input_token_price_per_1k",
            sa.Numeric(precision=18, scale=8),
            nullable=False,
        ),
        sa.Column(
            "output_token_price_per_1k",
            sa.Numeric(precision=18, scale=8),
            nullable=False,
        ),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "metadata_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        *timestamp_columns(),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "provider",
            "model_name",
            "currency",
            "effective_from",
            name="uq_model_pricing_rates_identity_effective_from",
        ),
    )
    op.create_index(
        "ix_model_pricing_rates_provider",
        "model_pricing_rates",
        ["provider"],
    )
    op.create_index(
        "ix_model_pricing_rates_model_name",
        "model_pricing_rates",
        ["model_name"],
    )
    op.create_index(
        "ix_model_pricing_rates_is_active",
        "model_pricing_rates",
        ["is_active"],
    )

    op.create_table(
        "workflow_run_costs",
        sa.Column("workflow_run_id", sa.Uuid(), nullable=False),
        sa.Column(
            "currency",
            sa.String(length=3),
            server_default=sa.text("'USD'"),
            nullable=False,
        ),
        sa.Column(
            "prompt_tokens",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "completion_tokens",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "total_tokens",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "model_call_count",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "tool_call_count",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "model_cost_usd",
            sa.Numeric(precision=18, scale=8),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "tool_cost_usd",
            sa.Numeric(precision=18, scale=8),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "total_cost_usd",
            sa.Numeric(precision=18, scale=8),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "calculation_status",
            sa.String(length=20),
            server_default=sa.text("'calculated'"),
            nullable=False,
        ),
        sa.Column("calculation_notes", sa.Text(), nullable=True),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(
            ["workflow_run_id"],
            ["workflow_runs.id"],
            name="fk_workflow_run_costs_workflow_run_id_workflow_runs",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "workflow_run_id",
            name="uq_workflow_run_costs_workflow_run_id",
        ),
    )
    op.create_index(
        "ix_workflow_run_costs_workflow_run_id",
        "workflow_run_costs",
        ["workflow_run_id"],
    )
    op.create_index(
        "ix_workflow_run_costs_total_cost_usd",
        "workflow_run_costs",
        ["total_cost_usd"],
    )
    op.create_index(
        "ix_workflow_run_costs_calculated_at",
        "workflow_run_costs",
        ["calculated_at"],
    )


def downgrade() -> None:
    """Drop cost tables in reverse dependency order."""

    op.drop_table("workflow_run_costs")
    op.drop_table("model_pricing_rates")
