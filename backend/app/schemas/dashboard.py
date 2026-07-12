"""Read schemas for project dashboard analytics."""

from datetime import datetime
from decimal import Decimal
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import WorkflowOutcomeStatus, WorkflowRunStatus


class ProjectDashboardOverviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: uuid.UUID
    total_workflows: int = Field(ge=0)
    total_workflow_runs: int = Field(ge=0)
    succeeded_runs: int = Field(ge=0)
    failed_runs: int = Field(ge=0)
    pending_runs: int = Field(ge=0)
    total_cost_usd: Decimal
    successful_outcomes: int = Field(ge=0)
    failed_outcomes: int = Field(ge=0)
    success_rate: Decimal
    cost_per_successful_outcome_usd: Decimal | None
    notes: str | None = None


class WorkflowRunDashboardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workflow_run_id: uuid.UUID
    workflow_id: uuid.UUID
    workflow_name: str | None = None
    configuration_id: uuid.UUID | None = None
    status: WorkflowRunStatus
    started_at: datetime | None = None
    completed_at: datetime | None = None
    total_cost_usd: Decimal | None = None
    outcome_status: WorkflowOutcomeStatus | None = None
    success: bool | None = None


class CostDashboardSummaryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: uuid.UUID
    total_cost_usd: Decimal
    total_cost_inr: Decimal = Decimal("0")
    model_cost_usd: Decimal
    tool_cost_usd: Decimal
    ai_cost_usd: Decimal = Decimal("0")
    ai_cost_inr: Decimal = Decimal("0")
    total_tokens: int = Field(ge=0)
    ai_total_tokens: int = Field(default=0, ge=0)
    model_call_count: int = Field(ge=0)
    tool_call_count: int = Field(ge=0)
    ai_run_count: int = Field(default=0, ge=0)
    average_cost_per_run_usd: Decimal
    highest_cost_run_id: uuid.UUID | None = None
    cost_by_provider: list["AiCostBreakdownRead"] = Field(default_factory=list)
    cost_by_model: list["AiCostBreakdownRead"] = Field(default_factory=list)
    latest_ai_runs: list["LatestAiRunDashboardRead"] = Field(default_factory=list)


class AiCostBreakdownRead(BaseModel):
    key: str
    total_cost_inr: Decimal
    total_cost_usd: Decimal
    total_tokens: int = Field(ge=0)
    run_count: int = Field(ge=0)


class LatestAiRunDashboardRead(BaseModel):
    id: uuid.UUID
    provider: str
    model: str
    workflow_name: str
    total_tokens: int = Field(ge=0)
    cost_inr: Decimal
    latency_ms: int = Field(ge=0)
    status: str
    created_at: datetime


class OutcomeDashboardSummaryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: uuid.UUID
    total_runs: int = Field(ge=0)
    successful_runs: int = Field(ge=0)
    failed_runs: int = Field(ge=0)
    pending_runs: int = Field(ge=0)
    success_rate: Decimal
    cost_per_successful_outcome_usd: Decimal | None
