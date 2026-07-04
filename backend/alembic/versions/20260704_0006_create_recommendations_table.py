"""Create recommendations table.

Revision ID: 0006_recommendations
Revises: 0005_outcome_tracking
Create Date: 2026-07-04
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0006_recommendations"
down_revision: str | None = "0005_outcome_tracking"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the rule-based recommendation suggestion table."""

    op.create_table(
        "recommendations",
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_id", sa.Uuid(), nullable=True),
        sa.Column("recommendation_type", sa.String(length=50), nullable=False),
        sa.Column(
            "severity",
            sa.String(length=20),
            server_default=sa.text("'medium'"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default=sa.text("'open'"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "current_metric_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column(
            "suggested_action_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column(
            "potential_savings_usd",
            sa.Numeric(precision=18, scale=8),
            nullable=True,
        ),
        sa.Column(
            "confidence_score",
            sa.Numeric(precision=5, scale=4),
            nullable=True,
        ),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("dismissed_at", sa.DateTime(timezone=True), nullable=True),
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
            name="fk_recommendations_project_id_projects",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["workflow_id"],
            ["workflows.id"],
            name="fk_recommendations_workflow_id_workflows",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_recommendations_project_id",
        "recommendations",
        ["project_id"],
    )
    op.create_index(
        "ix_recommendations_workflow_id",
        "recommendations",
        ["workflow_id"],
    )
    op.create_index(
        "ix_recommendations_recommendation_type",
        "recommendations",
        ["recommendation_type"],
    )
    op.create_index(
        "ix_recommendations_severity",
        "recommendations",
        ["severity"],
    )
    op.create_index(
        "ix_recommendations_status",
        "recommendations",
        ["status"],
    )
    op.create_index(
        "ix_recommendations_generated_at",
        "recommendations",
        ["generated_at"],
    )


def downgrade() -> None:
    """Drop the recommendation suggestion table."""

    op.drop_table("recommendations")
