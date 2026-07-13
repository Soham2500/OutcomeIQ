"""Add raw usage metadata to AI runs.

Revision ID: 0010_ai_runs_raw_usage
Revises: 0009_ai_runs
Create Date: 2026-07-13
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0010_ai_runs_raw_usage"
down_revision: str | None = "0009_ai_runs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Store safe provider token-usage metadata for audit/debugging."""

    op.add_column(
        "ai_runs",
        sa.Column(
            "raw_usage_json",
            sa.JSON(),
            server_default="{}",
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Remove safe provider token-usage metadata."""

    op.drop_column("ai_runs", "raw_usage_json")
