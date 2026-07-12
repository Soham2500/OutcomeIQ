"""Create AI runs table.

Revision ID: 0009_ai_runs
Revises: 0008_pending_registrations
Create Date: 2026-07-12
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0009_ai_runs"
down_revision: str | None = "0008_pending_registrations"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create table for real OpenAI/Gemini runs and cost tracking."""

    op.create_table(
        "ai_runs",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_name", sa.String(length=160), nullable=False),
        sa.Column("provider", sa.String(length=40), nullable=False),
        sa.Column("model", sa.String(length=160), nullable=False),
        sa.Column("prompt_preview", sa.String(length=500), nullable=False),
        sa.Column("response_preview", sa.String(length=1000), nullable=True),
        sa.Column("status", sa.String(length=20), server_default="succeeded", nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("latency_ms", sa.Integer(), server_default="0", nullable=False),
        sa.Column("input_tokens", sa.Integer(), server_default="0", nullable=False),
        sa.Column("output_tokens", sa.Integer(), server_default="0", nullable=False),
        sa.Column("total_tokens", sa.Integer(), server_default="0", nullable=False),
        sa.Column("cost_usd", sa.Numeric(18, 8), server_default="0", nullable=False),
        sa.Column("cost_inr", sa.Numeric(18, 8), server_default="0", nullable=False),
        sa.Column("currency", sa.String(length=3), server_default="INR", nullable=False),
        sa.Column("pricing_unknown", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name="fk_ai_runs_project_id_projects",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_ai_runs_user_id_users",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_runs_project_id", "ai_runs", ["project_id"])
    op.create_index("ix_ai_runs_user_id", "ai_runs", ["user_id"])
    op.create_index("ix_ai_runs_provider", "ai_runs", ["provider"])
    op.create_index("ix_ai_runs_model", "ai_runs", ["model"])
    op.create_index("ix_ai_runs_created_at", "ai_runs", ["created_at"])
    op.create_index("ix_ai_runs_status", "ai_runs", ["status"])


def downgrade() -> None:
    """Drop AI runs table."""

    op.drop_table("ai_runs")
