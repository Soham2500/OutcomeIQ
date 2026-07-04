"""Pydantic schemas for projects."""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict

from app.models.enums import ProjectStatus


class ProjectBase(BaseModel):
    name: str
    slug: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    organization_id: uuid.UUID


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    organization_id: uuid.UUID
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
