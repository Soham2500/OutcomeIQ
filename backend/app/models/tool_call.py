"""Individual tool-call telemetry model."""

from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ToolCallStatus


class ToolCall(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Record execution telemetry for one external tool call in a run."""

    __tablename__ = "tool_calls"
    __table_args__ = (
        Index("ix_tool_calls_workflow_run_id", "workflow_run_id"),
        Index("ix_tool_calls_status", "status"),
        Index("ix_tool_calls_tool_name", "tool_name"),
    )

    workflow_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "workflow_runs.id",
            name="fk_tool_calls_workflow_run_id_workflow_runs",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    tool_name: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=ToolCallStatus.PENDING.value,
        server_default=ToolCallStatus.PENDING.value,
    )
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estimated_cost_usd: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 8),
        nullable=True,
    )
    input_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
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
