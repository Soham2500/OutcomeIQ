"""Pydantic schemas for business Outcome Contracts."""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import OutcomeContractStatus


class OutcomeContractCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    project_id: uuid.UUID
    workflow_id: uuid.UUID | None = None
    name: str = Field(min_length=1, max_length=180)
    description: str | None = None
    success_criteria_json: dict[str, object] | None = None
    success_window_hours: int = Field(default=48, ge=1)


class OutcomeContractRead(OutcomeContractCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: OutcomeContractStatus
    created_by_user_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class OutcomeContractUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=180)
    description: str | None = None
    success_criteria_json: dict[str, object] | None = None
    success_window_hours: int | None = Field(default=None, ge=1)
    status: OutcomeContractStatus | None = None
