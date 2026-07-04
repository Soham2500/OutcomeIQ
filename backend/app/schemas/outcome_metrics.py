"""Read schemas for outcome-aware unit economics."""

from decimal import Decimal
import uuid

from pydantic import BaseModel, ConfigDict, Field


class CostPerSuccessfulOutcomeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: uuid.UUID | None = None
    workflow_id: uuid.UUID | None = None
    configuration_id: uuid.UUID | None = None
    total_runs: int = Field(ge=0)
    successful_runs: int = Field(ge=0)
    failed_runs: int = Field(ge=0)
    pending_runs: int = Field(ge=0)
    total_cost_usd: Decimal
    cost_per_successful_outcome_usd: Decimal | None
    success_rate: Decimal
    notes: str | None = None
