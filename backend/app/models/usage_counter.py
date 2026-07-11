"""Monthly usage counters for subscription limit checks."""

import uuid

from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class UsageCounter(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Track user usage inside a YYYY-MM period."""

    __tablename__ = "usage_counters"
    __table_args__ = (
        UniqueConstraint("user_id", "period_month", name="uq_usage_counters_user_period"),
        Index("ix_usage_counters_user_id", "user_id"),
        Index("ix_usage_counters_organization_id", "organization_id"),
        Index("ix_usage_counters_project_id", "project_id"),
        Index("ix_usage_counters_period_month", "period_month"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", name="fk_usage_counters_user_id_users", ondelete="CASCADE"),
        nullable=False,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id", name="fk_usage_counters_organization_id_organizations", ondelete="SET NULL"),
        nullable=True,
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("projects.id", name="fk_usage_counters_project_id_projects", ondelete="SET NULL"),
        nullable=True,
    )
    period_month: Mapped[str] = mapped_column(String(7), nullable=False)
    workflow_runs_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    projects_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
