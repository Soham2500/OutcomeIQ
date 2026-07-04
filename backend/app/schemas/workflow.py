"""Pydantic schemas for registered AI workflows."""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import WorkflowStatus


class WorkflowBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=180)
    slug: str = Field(
        min_length=1,
        max_length=120,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )
    description: str | None = None


class WorkflowCreate(WorkflowBase):
    project_id: uuid.UUID


class WorkflowRead(WorkflowBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    status: WorkflowStatus
    created_by_user_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class WorkflowUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=180)
    description: str | None = None
    status: WorkflowStatus | None = None
