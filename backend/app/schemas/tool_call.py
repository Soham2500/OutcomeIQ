"""Pydantic schemas for redacted tool-call telemetry."""

from datetime import datetime
from decimal import Decimal
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ToolCallStatus


class ToolCallCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    sequence_number: int = Field(ge=0)
    tool_name: str = Field(min_length=1, max_length=120)
    status: ToolCallStatus = ToolCallStatus.SUCCEEDED
    latency_ms: int | None = Field(default=None, ge=0)
    estimated_cost_usd: Decimal | None = Field(default=None, ge=0)
    input_summary: str | None = None
    output_summary: str | None = None
    error_message: str | None = None
    metadata_json: dict[str, object] | None = None


class ToolCallRead(ToolCallCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workflow_run_id: uuid.UUID
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
