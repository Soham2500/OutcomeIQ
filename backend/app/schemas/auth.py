"""Pydantic request and response schemas for authentication."""

import uuid
import re
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, WrapValidator

from app.models.enums import UserStatus


OUTCOMEIQ_LOCAL_EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@outcomeiq\.local$",
    flags=re.IGNORECASE,
)


def validate_auth_email(
    value: Any,
    handler: Any,
) -> str:
    """Allow the reserved local-dev domain; validate all other mail normally."""

    if isinstance(value, str) and OUTCOMEIQ_LOCAL_EMAIL_PATTERN.fullmatch(value):
        return value.lower()
    return handler(value)


AuthEmail = Annotated[EmailStr, WrapValidator(validate_auth_email)]


class RegisterRequest(BaseModel):
    email: AuthEmail
    full_name: str | None = None
    password: str = Field(min_length=6, max_length=72)


class LoginRequest(BaseModel):
    email: AuthEmail
    password: str = Field(min_length=6, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: AuthEmail
    full_name: str | None = None
    status: UserStatus
