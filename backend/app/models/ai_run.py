"""Persisted real AI provider run metadata and safe previews."""

from decimal import Decimal
import uuid

from typing import Any

from sqlalchemy import Boolean, ForeignKey, Index, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class AiRun(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Track one backend-only OpenAI or Gemini run without storing secrets."""

    __tablename__ = "ai_runs"
    __table_args__ = (
        Index("ix_ai_runs_project_id", "project_id"),
        Index("ix_ai_runs_user_id", "user_id"),
        Index("ix_ai_runs_provider", "provider"),
        Index("ix_ai_runs_model", "model"),
        Index("ix_ai_runs_created_at", "created_at"),
        Index("ix_ai_runs_status", "status"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", name="fk_ai_runs_user_id_users", ondelete="RESTRICT"),
        nullable=False,
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "projects.id",
            name="fk_ai_runs_project_id_projects",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    workflow_name: Mapped[str] = mapped_column(String(160), nullable=False)
    provider: Mapped[str] = mapped_column(String(40), nullable=False)
    model: Mapped[str] = mapped_column(String(160), nullable=False)
    prompt_preview: Mapped[str] = mapped_column(String(500), nullable=False)
    response_preview: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="succeeded",
        server_default="succeeded",
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    latency_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    input_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    output_tokens: Mapped[int] = mapped_column(
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
    cost_usd: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
    )
    cost_inr: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
        default=Decimal("0"),
        server_default="0",
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="INR",
        server_default="INR",
    )
    pricing_unknown: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    raw_usage_json: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
        server_default="{}",
    )
