"""Validation and exposure tests for authentication schemas."""

import pytest
from pydantic import ValidationError

from app.schemas.auth import CurrentUserRead, LoginRequest, RegisterRequest


def test_auth_schemas_accept_valid_credentials() -> None:
    register_request = RegisterRequest(
        email="new.user@example.com",
        full_name="New User",
        password="password123",
    )
    login_request = LoginRequest(
        email="new.user@example.com",
        password="password123",
    )

    assert str(register_request.email) == "new.user@example.com"
    assert str(login_request.email) == "new.user@example.com"


def test_auth_schemas_reject_invalid_email_and_short_password() -> None:
    with pytest.raises(ValidationError):
        RegisterRequest(email="not-an-email", password="123456")

    with pytest.raises(ValidationError):
        LoginRequest(email="user@example.com", password="short")


def test_current_user_schema_never_exposes_password_hash() -> None:
    assert "hashed_password" not in CurrentUserRead.model_fields
    assert "password" not in CurrentUserRead.model_fields
