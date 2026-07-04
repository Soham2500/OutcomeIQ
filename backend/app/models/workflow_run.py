"""Workflow execution-run model."""

from datetime import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import WorkflowRunStatus, WorkflowRunTrigger


class WorkflowRun(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Track one complete execution attempt of a registered workflow."""

    __tablename__ = "workflow_runs"
    __table_args__ = (
        Index("ix_workflow_runs_project_id", "project_id"),
        Index("ix_workflow_runs_workflow_id", "workflow_id"),
        Index("ix_workflow_runs_configuration_id", "configuration_id"),
        Index("ix_workflow_runs_status", "status"),
        Index("ix_workflow_runs_external_reference", "external_reference"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "projects.id",
            name="fk_workflow_runs_project_id_projects",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "workflows.id",
            name="fk_workflow_runs_workflow_id_workflows",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    configuration_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "workflow_configurations.id",
            name="fk_workflow_runs_configuration_id_workflow_configurations",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )
    triggered_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_workflow_runs_triggered_by_user_id_users",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )
    trigger_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=WorkflowRunTrigger.MANUAL.value,
        server_default=WorkflowRunTrigger.MANUAL.value,
    )
    external_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=WorkflowRunStatus.PENDING.value,
        server_default=WorkflowRunStatus.PENDING.value,
    )
    input_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    metadata_json: Mapped[dict[str, object] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
