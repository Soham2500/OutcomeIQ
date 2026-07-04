"""Persisted rule-based recommendation suggestion."""

from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import RecommendationSeverity, RecommendationStatus


class Recommendation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Store evidence-backed advice without applying any workflow change."""

    __tablename__ = "recommendations"
    __table_args__ = (
        Index("ix_recommendations_project_id", "project_id"),
        Index("ix_recommendations_workflow_id", "workflow_id"),
        Index("ix_recommendations_recommendation_type", "recommendation_type"),
        Index("ix_recommendations_severity", "severity"),
        Index("ix_recommendations_status", "status"),
        Index("ix_recommendations_generated_at", "generated_at"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "projects.id",
            name="fk_recommendations_project_id_projects",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    workflow_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "workflows.id",
            name="fk_recommendations_workflow_id_workflows",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )
    recommendation_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=RecommendationSeverity.MEDIUM.value,
        server_default=RecommendationSeverity.MEDIUM.value,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=RecommendationStatus.OPEN.value,
        server_default=RecommendationStatus.OPEN.value,
    )
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    current_metric_json: Mapped[dict[str, object] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    suggested_action_json: Mapped[dict[str, object] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    potential_savings_usd: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 8),
        nullable=True,
    )
    confidence_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 4),
        nullable=True,
    )
    generated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    dismissed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
