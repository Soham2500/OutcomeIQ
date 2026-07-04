"""Persisted cost summary for one workflow run."""

from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import CostCalculationStatus


class WorkflowRunCost(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Store deterministic cost-calculation output for one workflow run."""

    __tablename__ = "workflow_run_costs"
    __table_args__ = (
        UniqueConstraint(
            "workflow_run_id",
            name="uq_workflow_run_costs_workflow_run_id",
        ),
        Index("ix_workflow_run_costs_workflow_run_id", "workflow_run_id"),
        Index("ix_workflow_run_costs_total_cost_usd", "total_cost_usd"),
        Index("ix_workflow_run_costs_calculated_at", "calculated_at"),
    )

    workflow_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "workflow_runs.id",
            name="fk_workflow_run_costs_workflow_run_id_workflow_runs",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="USD",
        server_default="USD",
    )
    prompt_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    completion_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    total_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    model_call_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    tool_call_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    model_cost_usd: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
    )
    tool_cost_usd: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
    )
    total_cost_usd: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
    )
    calculation_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=CostCalculationStatus.CALCULATED.value,
        server_default=CostCalculationStatus.CALCULATED.value,
    )
    calculation_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    calculated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
