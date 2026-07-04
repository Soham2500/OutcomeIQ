"""Pydantic request and response schemas for authentication."""

import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import UserStatus


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str | None = None
    password: str = Field(min_length=6, max_length=72)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    full_name: str | None = None
    status: UserStatus
