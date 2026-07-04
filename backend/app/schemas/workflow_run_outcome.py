"""Pydantic schemas for workflow-run business outcomes."""

from datetime import datetime
from decimal import Decimal
import uuid

from pydantic import BaseModel, ConfigDict

from app.models.enums import OutcomeVerificationSource, WorkflowOutcomeStatus


class WorkflowRunOutcomeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    outcome_contract_id: uuid.UUID | None = None
    status: WorkflowOutcomeStatus
    verification_source: OutcomeVerificationSource = (
        OutcomeVerificationSource.MANUAL
    )
    outcome_score: Decimal | None = None
    business_value_usd: Decimal | None = None
    verified_at: datetime | None = None
    notes: str | None = None
    metadata_json: dict[str, object] | None = None


class WorkflowRunOutcomeRead(WorkflowRunOutcomeCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workflow_run_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class WorkflowRunOutcomeUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    outcome_contract_id: uuid.UUID | None = None
    status: WorkflowOutcomeStatus | None = None
    verification_source: OutcomeVerificationSource | None = None
    outcome_score: Decimal | None = None
    business_value_usd: Decimal | None = None
    verified_at: datetime | None = None
    notes: str | None = None
    metadata_json: dict[str, object] | None = None
