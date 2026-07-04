"""Shared FastAPI dependencies for authenticated requests."""

from typing import Annotated
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.enums import UserStatus
from app.models.user import User
from app.repositories.user_repository import get_user_by_id


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise credentials_error

    try:
        payload = decode_access_token(credentials.credentials)
        subject = payload.get("sub")
        if not isinstance(subject, str):
            raise credentials_error
        user_id = uuid.UUID(subject)
    except (JWTError, RuntimeError, TypeError, ValueError) as exc:
        raise credentials_error from exc

    user = get_user_by_id(db, user_id)
    if user is None or user.status != UserStatus.ACTIVE.value:
        raise credentials_error
    return user
