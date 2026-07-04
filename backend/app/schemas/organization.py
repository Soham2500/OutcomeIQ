"""Pydantic schemas for organizations."""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import OrganizationStatus


class OrganizationBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=160)
    slug: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationRead(OrganizationBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: OrganizationStatus
    created_at: datetime
    updated_at: datetime


class OrganizationUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=160)
    status: OrganizationStatus | None = None
