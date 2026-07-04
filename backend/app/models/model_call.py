"""Individual model-call telemetry model."""

from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ModelCallStatus


class ModelCall(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Record usage, cost estimate and execution state for one model call."""

    __tablename__ = "model_calls"
    __table_args__ = (
        Index("ix_model_calls_workflow_run_id", "workflow_run_id"),
        Index("ix_model_calls_status", "status"),
        Index("ix_model_calls_provider", "provider"),
        Index("ix_model_calls_model_name", "model_name"),
        Index("ix_model_calls_is_retry", "is_retry"),
        Index("ix_model_calls_is_fallback", "is_fallback"),
    )

    workflow_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "workflow_runs.id",
            name="fk_model_calls_workflow_run_id_workflow_runs",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    provider: Mapped[str] = mapped_column(String(80), nullable=False)
    model_name: Mapped[str] = mapped_column(String(160), nullable=False)
    call_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=ModelCallStatus.PENDING.value,
        server_default=ModelCallStatus.PENDING.value,
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
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estimated_cost_usd: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 8),
        nullable=True,
    )
    is_retry: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    is_fallback: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    request_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    response_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict[str, object] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
