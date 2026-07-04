"""Password hashing and JWT helpers for the authentication foundation."""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Safely compare a plain password with a stored password hash."""

    try:
        return password_context.verify(plain_password, hashed_password)
    except (TypeError, ValueError):
        return False


def get_password_hash(password: str) -> str:
    """Create a bcrypt hash; the plain password is never logged or stored."""

    return password_context.hash(password)


def _jwt_secret() -> str:
    """Return the configured secret without ever including it in an error."""

    if not settings.JWT_SECRET_KEY:
        raise RuntimeError("JWT secret is not configured.")
    return settings.JWT_SECRET_KEY


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed access token for one user identifier."""

    now = datetime.now(timezone.utc)
    expires_at = now + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": subject,
        "iat": now,
        "exp": expires_at,
    }
    return jwt.encode(
        payload,
        _jwt_secret(),
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a signed access token."""

    return jwt.decode(
        token,
        _jwt_secret(),
        algorithms=[settings.JWT_ALGORITHM],
    )
