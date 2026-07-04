"""Verified or pending business outcome for one workflow run."""

from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import OutcomeVerificationSource, WorkflowOutcomeStatus


class WorkflowRunOutcome(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Store the current verified outcome evidence for one workflow run."""

    __tablename__ = "workflow_run_outcomes"
    __table_args__ = (
        UniqueConstraint(
            "workflow_run_id",
            name="uq_workflow_run_outcomes_workflow_run_id",
        ),
        Index("ix_workflow_run_outcomes_workflow_run_id", "workflow_run_id"),
        Index(
            "ix_workflow_run_outcomes_outcome_contract_id",
            "outcome_contract_id",
        ),
        Index("ix_workflow_run_outcomes_status", "status"),
        Index("ix_workflow_run_outcomes_verified_at", "verified_at"),
    )

    workflow_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "workflow_runs.id",
            name="fk_workflow_run_outcomes_workflow_run_id_workflow_runs",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    outcome_contract_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "outcome_contracts.id",
            name="fk_run_outcomes_contract_id_outcome_contracts",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=WorkflowOutcomeStatus.PENDING.value,
        server_default=WorkflowOutcomeStatus.PENDING.value,
    )
    verification_source: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=OutcomeVerificationSource.MANUAL.value,
        server_default=OutcomeVerificationSource.MANUAL.value,
    )
    outcome_score: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 4),
        nullable=True,
    )
    business_value_usd: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 8),
        nullable=True,
    )
    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict[str, object] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
