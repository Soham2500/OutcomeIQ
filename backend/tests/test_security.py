"""Unit tests for password and JWT security helpers."""

from app.core import security


def test_password_hash_and_verify() -> None:
    password = "unit-test-password"
    hashed_password = security.get_password_hash(password)

    assert hashed_password != password
    assert security.verify_password(password, hashed_password)
    assert not security.verify_password("wrong-password", hashed_password)


def test_access_token_create_and_decode(monkeypatch) -> None:
    monkeypatch.setattr(
        security.settings,
        "JWT_SECRET_KEY",
        "unit-test-secret-that-is-not-used-outside-tests",
    )

    token = security.create_access_token(subject="test-user-id")
    payload = security.decode_access_token(token)

    assert payload["sub"] == "test-user-id"
    assert "exp" in payload
