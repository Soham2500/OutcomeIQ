"""Registered AI workflow model."""

import uuid

from sqlalchemy import ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import WorkflowStatus


class Workflow(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Identify an AI workflow whose execution economics will be measured."""

    __tablename__ = "workflows"
    __table_args__ = (
        UniqueConstraint("project_id", "slug", name="uq_workflows_project_slug"),
        Index("ix_workflows_project_id", "project_id"),
        Index("ix_workflows_status", "status"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "projects.id",
            name="fk_workflows_project_id_projects",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=WorkflowStatus.ACTIVE.value,
        server_default=WorkflowStatus.ACTIVE.value,
    )
    created_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_workflows_created_by_user_id_users",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )
