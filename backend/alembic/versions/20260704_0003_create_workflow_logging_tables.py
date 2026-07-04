"""Create workflow logging tables.

Revision ID: 0003_workflow_logging
Revises: 0002_core_identity_projects
Create Date: 2026-07-04
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0003_workflow_logging"
down_revision: str | None = "0002_core_identity_projects"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def timestamp_columns() -> tuple[sa.Column, sa.Column]:
    """Return the shared mutable-record timestamp columns."""

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
    """Create the five approved workflow logging tables."""

    op.create_table(
        "workflows",
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
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
            name="fk_workflows_project_id_projects",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["created_by_user_id"],
            ["users.id"],
            name="fk_workflows_created_by_user_id_users",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "project_id",
            "slug",
            name="uq_workflows_project_slug",
        ),
    )
    op.create_index("ix_workflows_project_id", "workflows", ["project_id"])
    op.create_index("ix_workflows_status", "workflows", ["status"])

    op.create_table(
        "workflow_configurations",
        sa.Column("workflow_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("version_label", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("strategy_name", sa.String(length=100), nullable=True),
        sa.Column("config_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column("created_by_user_id", sa.Uuid(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(
            ["workflow_id"],
            ["workflows.id"],
            name="fk_workflow_configurations_workflow_id_workflows",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["created_by_user_id"],
            ["users.id"],
            name="fk_workflow_configurations_created_by_user_id_users",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "workflow_id",
            "version_label",
            name="uq_workflow_configurations_workflow_version_label",
        ),
    )
    op.create_index(
        "ix_workflow_configurations_workflow_id",
        "workflow_configurations",
        ["workflow_id"],
    )
    op.create_index(
        "ix_workflow_configurations_is_active",
        "workflow_configurations",
        ["is_active"],
    )

    op.create_table(
        "workflow_runs",
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("workflow_id", sa.Uuid(), nullable=False),
        sa.Column("configuration_id", sa.Uuid(), nullable=True),
        sa.Column("triggered_by_user_id", sa.Uuid(), nullable=True),
        sa.Column(
            "trigger_type",
            sa.String(length=20),
            server_default=sa.text("'manual'"),
            nullable=False,
        ),
        sa.Column("external_reference", sa.String(length=255), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default=sa.text("'pending'"),
            nullable=False,
        ),
        sa.Column("input_summary", sa.Text(), nullable=True),
        sa.Column("output_summary", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name="fk_workflow_runs_project_id_projects",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["workflow_id"],
            ["workflows.id"],
            name="fk_workflow_runs_workflow_id_workflows",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["configuration_id"],
            ["workflow_configurations.id"],
            name="fk_workflow_runs_configuration_id_workflow_configurations",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["triggered_by_user_id"],
            ["users.id"],
            name="fk_workflow_runs_triggered_by_user_id_users",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_runs_project_id", "workflow_runs", ["project_id"])
    op.create_index("ix_workflow_runs_workflow_id", "workflow_runs", ["workflow_id"])
    op.create_index(
        "ix_workflow_runs_configuration_id",
        "workflow_runs",
        ["configuration_id"],
    )
    op.create_index("ix_workflow_runs_status", "workflow_runs", ["status"])
    op.create_index(
        "ix_workflow_runs_external_reference",
        "workflow_runs",
        ["external_reference"],
    )

    op.create_table(
        "model_calls",
        sa.Column("workflow_run_id", sa.Uuid(), nullable=False),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=80), nullable=False),
        sa.Column("model_name", sa.String(length=160), nullable=False),
        sa.Column("call_type", sa.String(length=80), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default=sa.text("'pending'"),
            nullable=False,
        ),
        sa.Column("prompt_tokens", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column(
            "completion_tokens",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column("total_tokens", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("estimated_cost_usd", sa.Numeric(precision=18, scale=8), nullable=True),
        sa.Column(
            "is_retry",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "is_fallback",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("request_summary", sa.Text(), nullable=True),
        sa.Column("response_summary", sa.Text(), nullable=True),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(
            ["workflow_run_id"],
            ["workflow_runs.id"],
            name="fk_model_calls_workflow_run_id_workflow_runs",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_model_calls_workflow_run_id",
        "model_calls",
        ["workflow_run_id"],
    )
    op.create_index("ix_model_calls_provider", "model_calls", ["provider"])
    op.create_index("ix_model_calls_model_name", "model_calls", ["model_name"])
    op.create_index("ix_model_calls_status", "model_calls", ["status"])
    op.create_index("ix_model_calls_is_retry", "model_calls", ["is_retry"])
    op.create_index("ix_model_calls_is_fallback", "model_calls", ["is_fallback"])

    op.create_table(
        "tool_calls",
        sa.Column("workflow_run_id", sa.Uuid(), nullable=False),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("tool_name", sa.String(length=120), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default=sa.text("'pending'"),
            nullable=False,
        ),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("estimated_cost_usd", sa.Numeric(precision=18, scale=8), nullable=True),
        sa.Column("input_summary", sa.Text(), nullable=True),
        sa.Column("output_summary", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(
            ["workflow_run_id"],
            ["workflow_runs.id"],
            name="fk_tool_calls_workflow_run_id_workflow_runs",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tool_calls_workflow_run_id",
        "tool_calls",
        ["workflow_run_id"],
    )
    op.create_index("ix_tool_calls_tool_name", "tool_calls", ["tool_name"])
    op.create_index("ix_tool_calls_status", "tool_calls", ["status"])


def downgrade() -> None:
    """Drop workflow logging tables in reverse dependency order."""

    op.drop_table("tool_calls")
    op.drop_table("model_calls")
    op.drop_table("workflow_runs")
    op.drop_table("workflow_configurations")
    op.drop_table("workflows")
