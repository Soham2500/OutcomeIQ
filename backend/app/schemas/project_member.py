"""Pydantic schemas for project memberships."""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict

from app.models.enums import ProjectMemberRole


class ProjectMemberCreate(BaseModel):
    project_id: uuid.UUID
    user_id: uuid.UUID
    role: ProjectMemberRole = ProjectMemberRole.MEMBER


class ProjectMemberRead(ProjectMemberCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
