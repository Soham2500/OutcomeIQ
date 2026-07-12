"""Schemas for real AI provider runs."""

from datetime import datetime
from decimal import Decimal
import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AiRunCreate(BaseModel):
    project_id: uuid.UUID
    workflow_name: str = Field(min_length=1, max_length=160)
    prompt: str = Field(min_length=1, max_length=8000)
    provider: str | None = Field(default=None, max_length=40)
    model: str | None = Field(default=None, max_length=160)

    @field_validator("prompt", "workflow_name")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Value cannot be blank.")
        return cleaned


class AiRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    workflow_name: str
    provider: str
    model: str
    response_text: str | None = None
    prompt_preview: str
    response_preview: str | None = None
    status: str
    error_message: str | None = None
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: Decimal
    cost_inr: Decimal
    currency: str
    pricing_unknown: bool
    latency_ms: int
    created_at: datetime


class AiRunListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    workflow_name: str
    provider: str
    model: str
    prompt_preview: str
    response_preview: str | None = None
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: Decimal
    cost_inr: Decimal
    currency: str
    pricing_unknown: bool
    latency_ms: int
    status: str
    error_message: str | None = None
    created_at: datetime
