"""Subscription plan model for test-mode SaaS billing."""

from decimal import Decimal

from sqlalchemy import Boolean, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Plan(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Represent an available subscription plan."""

    __tablename__ = "plans"
    __table_args__ = (Index("ix_plans_slug", "slug", unique=True),)

    name: Mapped[str] = mapped_column(String(80), nullable=False)
    slug: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price_inr_monthly: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0",
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR", server_default="INR")
    max_projects: Mapped[int] = mapped_column(Integer, nullable=False)
    max_workflow_runs_per_month: Mapped[int] = mapped_column(Integer, nullable=False)
    max_team_members: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")
    export_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    analytics_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    recommendations_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    openai_provider_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
