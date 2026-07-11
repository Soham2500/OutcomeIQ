"""Create subscription billing tables.

Revision ID: 0007_billing
Revises: 0006_recommendations
Create Date: 2026-07-04
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0007_billing"
down_revision: str | None = "0006_recommendations"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create plans, subscriptions, payment events and usage counters."""

    op.create_table(
        "plans",
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("slug", sa.String(length=80), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price_inr_monthly", sa.Numeric(precision=12, scale=2), server_default="0", nullable=False),
        sa.Column("currency", sa.String(length=3), server_default="INR", nullable=False),
        sa.Column("max_projects", sa.Integer(), nullable=False),
        sa.Column("max_workflow_runs_per_month", sa.Integer(), nullable=False),
        sa.Column("max_team_members", sa.Integer(), server_default="1", nullable=False),
        sa.Column("export_enabled", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("analytics_enabled", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("recommendations_enabled", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("openai_provider_enabled", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_plans_slug", "plans", ["slug"], unique=True)

    op.create_table(
        "subscriptions",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=30), server_default="free", nullable=False),
        sa.Column("provider", sa.String(length=40), server_default="manual", nullable=False),
        sa.Column("provider_subscription_id", sa.String(length=255), nullable=True),
        sa.Column("current_period_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("current_period_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancel_at_period_end", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["plan_id"], ["plans.id"], name="fk_subscriptions_plan_id_plans", ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_subscriptions_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_subscriptions_user_id", "subscriptions", ["user_id"])
    op.create_index("ix_subscriptions_plan_id", "subscriptions", ["plan_id"])
    op.create_index("ix_subscriptions_status", "subscriptions", ["status"])

    op.create_table(
        "payment_events",
        sa.Column("provider", sa.String(length=40), server_default="razorpay_test", nullable=False),
        sa.Column("event_type", sa.String(length=160), nullable=False),
        sa.Column("provider_event_id", sa.String(length=255), nullable=True),
        sa.Column("payload_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("processed", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_payment_events_provider", "payment_events", ["provider"])
    op.create_index("ix_payment_events_provider_event_id", "payment_events", ["provider_event_id"])
    op.create_index("ix_payment_events_processed", "payment_events", ["processed"])

    op.create_table(
        "usage_counters",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("organization_id", sa.Uuid(), nullable=True),
        sa.Column("project_id", sa.Uuid(), nullable=True),
        sa.Column("period_month", sa.String(length=7), nullable=False),
        sa.Column("workflow_runs_used", sa.Integer(), server_default="0", nullable=False),
        sa.Column("projects_used", sa.Integer(), server_default="0", nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], name="fk_usage_counters_organization_id_organizations", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], name="fk_usage_counters_project_id_projects", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_usage_counters_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "period_month", name="uq_usage_counters_user_period"),
    )
    op.create_index("ix_usage_counters_user_id", "usage_counters", ["user_id"])
    op.create_index("ix_usage_counters_organization_id", "usage_counters", ["organization_id"])
    op.create_index("ix_usage_counters_project_id", "usage_counters", ["project_id"])
    op.create_index("ix_usage_counters_period_month", "usage_counters", ["period_month"])


def downgrade() -> None:
    """Drop subscription billing tables."""

    op.drop_table("usage_counters")
    op.drop_table("payment_events")
    op.drop_table("subscriptions")
    op.drop_table("plans")
