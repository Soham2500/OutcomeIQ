"""Pending email-OTP registrations awaiting verification."""

from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class PendingRegistration(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Store a registration attempt until its email OTP is verified."""

    __tablename__ = "pending_registrations"
    __table_args__ = (
        Index("ix_pending_registrations_email", "email", unique=True),
        Index("ix_pending_registrations_otp_expires_at", "otp_expires_at"),
    )

    email: Mapped[str] = mapped_column(String(320), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    hashed_otp: Mapped[str] = mapped_column(Text, nullable=False)
    otp_expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    otp_attempts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    last_sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
