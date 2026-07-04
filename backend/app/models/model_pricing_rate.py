"""Version-aware model token pricing rate."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Index, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class ModelPricingRate(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Store explicit demo or configured token rates without provider calls."""

    __tablename__ = "model_pricing_rates"
    __table_args__ = (
        UniqueConstraint(
            "provider",
            "model_name",
            "currency",
            "effective_from",
            name="uq_model_pricing_rates_identity_effective_from",
        ),
        Index("ix_model_pricing_rates_provider", "provider"),
        Index("ix_model_pricing_rates_model_name", "model_name"),
        Index("ix_model_pricing_rates_is_active", "is_active"),
    )

    provider: Mapped[str] = mapped_column(String(80), nullable=False)
    model_name: Mapped[str] = mapped_column(String(160), nullable=False)
    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="USD",
        server_default="USD",
    )
    input_token_price_per_1k: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
    )
    output_token_price_per_1k: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
    )
    effective_from: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    effective_to: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )
    metadata_json: Mapped[dict[str, object] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
