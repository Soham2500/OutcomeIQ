"""Stored payment webhook/event payloads for test-mode billing."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Index, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import PaymentProvider


class PaymentEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Store incoming payment events without exposing secrets."""

    __tablename__ = "payment_events"
    __table_args__ = (
        Index("ix_payment_events_provider", "provider"),
        Index("ix_payment_events_provider_event_id", "provider_event_id"),
        Index("ix_payment_events_processed", "processed"),
    )

    provider: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default=PaymentProvider.RAZORPAY_TEST.value,
        server_default=PaymentProvider.RAZORPAY_TEST.value,
    )
    event_type: Mapped[str] = mapped_column(String(160), nullable=False)
    provider_event_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    payload_json: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    processed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
