"""Pydantic schemas for projects."""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ProjectStatus


class ProjectBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=160)
    slug: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )
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


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = None
    status: ProjectStatus | None = None
