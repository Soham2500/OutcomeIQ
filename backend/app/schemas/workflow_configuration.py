"""Pydantic schemas for versioned workflow configurations."""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class WorkflowConfigurationCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=160)
    version_label: str = Field(min_length=1, max_length=100)
    description: str | None = None
    strategy_name: str | None = Field(default=None, max_length=100)
    config_json: dict[str, object] | None = None


class WorkflowConfigurationRead(WorkflowConfigurationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    workflow_id: uuid.UUID
    is_active: bool
    created_by_user_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class WorkflowConfigurationUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = None
    strategy_name: str | None = Field(default=None, max_length=100)
    config_json: dict[str, object] | None = None
    is_active: bool | None = None
