"""Business success definition for a project workflow."""

import uuid

from sqlalchemy import ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import OutcomeContractStatus


class OutcomeContract(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Define the evidence and time window used to judge business success."""

    __tablename__ = "outcome_contracts"
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "name",
            name="uq_outcome_contracts_project_name",
        ),
        Index("ix_outcome_contracts_project_id", "project_id"),
        Index("ix_outcome_contracts_workflow_id", "workflow_id"),
        Index("ix_outcome_contracts_status", "status"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "projects.id",
            name="fk_outcome_contracts_project_id_projects",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    workflow_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "workflows.id",
            name="fk_outcome_contracts_workflow_id_workflows",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    success_criteria_json: Mapped[dict[str, object] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    success_window_hours: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=48,
        server_default="48",
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=OutcomeContractStatus.ACTIVE.value,
        server_default=OutcomeContractStatus.ACTIVE.value,
    )
    created_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_outcome_contracts_created_by_user_id_users",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )
