"""Pydantic schemas for user data that is safe to expose."""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict

from app.models.enums import UserStatus


class UserBase(BaseModel):
    email: str
    full_name: str | None = None


class UserCreate(UserBase):
    """Input for future user creation; passwords are intentionally excluded."""


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: UserStatus
    created_at: datetime
    updated_at: datetime
