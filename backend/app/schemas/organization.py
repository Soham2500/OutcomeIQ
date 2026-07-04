"""Pydantic schemas for organizations."""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict

from app.models.enums import OrganizationStatus


class OrganizationBase(BaseModel):
    name: str
    slug: str


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationRead(OrganizationBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: OrganizationStatus
    created_at: datetime
    updated_at: datetime
