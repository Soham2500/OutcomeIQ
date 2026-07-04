"""Pydantic schemas for configured model pricing rates."""

from datetime import datetime
from decimal import Decimal
import uuid

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ModelPricingRateCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    provider: str = Field(min_length=1, max_length=80)
    model_name: str = Field(min_length=1, max_length=160)
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    input_token_price_per_1k: Decimal = Field(ge=0)
    output_token_price_per_1k: Decimal = Field(ge=0)
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    is_active: bool = True
    metadata_json: dict[str, object] | None = None

    @model_validator(mode="after")
    def validate_effective_window(self) -> "ModelPricingRateCreate":
        if (
            self.effective_from is not None
            and self.effective_to is not None
            and self.effective_to <= self.effective_from
        ):
            raise ValueError("effective_to must be later than effective_from")
        return self


class ModelPricingRateRead(ModelPricingRateCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ModelPricingRateUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    input_token_price_per_1k: Decimal | None = Field(default=None, ge=0)
    output_token_price_per_1k: Decimal | None = Field(default=None, ge=0)
    effective_from: datetime | None = None
    effective_to: datetime | None = None
    is_active: bool | None = None
    metadata_json: dict[str, object] | None = None
