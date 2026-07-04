"""Pydantic schemas for persisted workflow run costs."""

from datetime import datetime
from decimal import Decimal
import uuid

from pydantic import BaseModel, ConfigDict

from app.models.enums import CostCalculationStatus


class WorkflowRunCostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workflow_run_id: uuid.UUID
    currency: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    model_call_count: int
    tool_call_count: int
    model_cost_usd: Decimal
    tool_cost_usd: Decimal
    total_cost_usd: Decimal
    calculation_status: CostCalculationStatus
    calculation_notes: str | None
    calculated_at: datetime | None
    created_at: datetime
    updated_at: datetime


class WorkflowRunCostCalculateResponse(WorkflowRunCostRead):
    """Response returned after a cost summary is calculated or recalculated."""
