"""Versioned workflow configuration model."""

import uuid

from sqlalchemy import Boolean, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class WorkflowConfiguration(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Capture a comparable, versioned workflow execution strategy."""

    __tablename__ = "workflow_configurations"
    __table_args__ = (
        UniqueConstraint(
            "workflow_id",
            "version_label",
            name="uq_workflow_configurations_workflow_version_label",
        ),
        Index("ix_workflow_configurations_workflow_id", "workflow_id"),
        Index("ix_workflow_configurations_is_active", "is_active"),
    )

    workflow_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "workflows.id",
            name="fk_workflow_configurations_workflow_id_workflows",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    version_label: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    strategy_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    config_json: Mapped[dict[str, object] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )
    created_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_workflow_configurations_created_by_user_id_users",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )
