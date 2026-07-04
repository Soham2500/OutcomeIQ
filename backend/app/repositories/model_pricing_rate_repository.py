"""Database access functions for model pricing rates."""

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.model_pricing_rate import ModelPricingRate


def create_pricing_rate(
    db: Session,
    provider: str,
    model_name: str,
    input_token_price_per_1k: Decimal,
    output_token_price_per_1k: Decimal,
    currency: str = "USD",
    effective_from: datetime | None = None,
    effective_to: datetime | None = None,
    is_active: bool = True,
    metadata_json: dict[str, object] | None = None,
) -> ModelPricingRate:
    pricing_rate = ModelPricingRate(
        provider=provider,
        model_name=model_name,
        currency=currency,
        input_token_price_per_1k=input_token_price_per_1k,
        output_token_price_per_1k=output_token_price_per_1k,
        effective_from=effective_from,
        effective_to=effective_to,
        is_active=is_active,
        metadata_json=metadata_json,
    )
    db.add(pricing_rate)
    db.commit()
    db.refresh(pricing_rate)
    return pricing_rate


def get_active_rate(
    db: Session,
    provider: str,
    model_name: str,
    currency: str = "USD",
) -> ModelPricingRate | None:
    now = datetime.now(timezone.utc)
    statement = (
        select(ModelPricingRate)
        .where(
            ModelPricingRate.provider == provider,
            ModelPricingRate.model_name == model_name,
            ModelPricingRate.currency == currency,
            ModelPricingRate.is_active.is_(True),
            or_(
                ModelPricingRate.effective_from.is_(None),
                ModelPricingRate.effective_from <= now,
            ),
            or_(
                ModelPricingRate.effective_to.is_(None),
                ModelPricingRate.effective_to > now,
            ),
        )
        .order_by(
            ModelPricingRate.effective_from.desc().nullslast(),
            ModelPricingRate.created_at.desc(),
        )
        .limit(1)
    )
    return db.scalar(statement)


def list_pricing_rates(
    db: Session,
    provider: str | None = None,
    model_name: str | None = None,
    active_only: bool = True,
    limit: int = 50,
    offset: int = 0,
) -> list[ModelPricingRate]:
    statement = select(ModelPricingRate)
    if provider is not None:
        statement = statement.where(ModelPricingRate.provider == provider)
    if model_name is not None:
        statement = statement.where(ModelPricingRate.model_name == model_name)
    if active_only:
        statement = statement.where(ModelPricingRate.is_active.is_(True))
    statement = (
        statement.order_by(
            ModelPricingRate.provider,
            ModelPricingRate.model_name,
            ModelPricingRate.created_at.desc(),
        )
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))
