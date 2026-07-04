"""Pydantic schemas for workflow runs and assembled traces."""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import WorkflowRunStatus, WorkflowRunTrigger
from app.schemas.model_call import ModelCallRead
from app.schemas.tool_call import ToolCallRead


class WorkflowRunCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    project_id: uuid.UUID
    workflow_id: uuid.UUID
    configuration_id: uuid.UUID | None = None
    trigger_type: WorkflowRunTrigger = WorkflowRunTrigger.MANUAL
    external_reference: str | None = Field(default=None, max_length=255)
    input_summary: str | None = None
    metadata_json: dict[str, object] | None = None


class WorkflowRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    workflow_id: uuid.UUID
    configuration_id: uuid.UUID | None
    triggered_by_user_id: uuid.UUID | None
    trigger_type: WorkflowRunTrigger
    external_reference: str | None
    status: WorkflowRunStatus
    input_summary: str | None
    output_summary: str | None
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    latency_ms: int | None
    metadata_json: dict[str, object] | None
    created_at: datetime
    updated_at: datetime


class WorkflowRunUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    external_reference: str | None = Field(default=None, max_length=255)
    status: WorkflowRunStatus | None = None
    input_summary: str | None = None
    output_summary: str | None = None
    error_message: str | None = None
    latency_ms: int | None = Field(default=None, ge=0)
    metadata_json: dict[str, object] | None = None


class WorkflowRunCompleteRequest(BaseModel):
    output_summary: str | None = None
    latency_ms: int | None = Field(default=None, ge=0)
    metadata_json: dict[str, object] | None = None


class WorkflowRunFailRequest(BaseModel):
    error_message: str | None = None
    latency_ms: int | None = Field(default=None, ge=0)


class WorkflowRunTraceRead(BaseModel):
    workflow_run: WorkflowRunRead
    model_calls: list[ModelCallRead]
    tool_calls: list[ToolCallRead]
