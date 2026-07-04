"""Pydantic schemas for redacted model-call telemetry."""

from datetime import datetime
from decimal import Decimal
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ModelCallStatus


class ModelCallCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    sequence_number: int = Field(ge=0)
    provider: str = Field(min_length=1, max_length=80)
    model_name: str = Field(min_length=1, max_length=160)
    call_type: str | None = Field(default=None, max_length=80)
    status: ModelCallStatus = ModelCallStatus.SUCCEEDED
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)
    latency_ms: int | None = Field(default=None, ge=0)
    estimated_cost_usd: Decimal | None = Field(default=None, ge=0)
    is_retry: bool = False
    is_fallback: bool = False
    request_summary: str | None = None
    response_summary: str | None = None
    error_message: str | None = None
    metadata_json: dict[str, object] | None = None


class ModelCallRead(ModelCallCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workflow_run_id: uuid.UUID
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
