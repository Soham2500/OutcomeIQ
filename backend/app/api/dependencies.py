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
from app.models.enums import ProjectMemberRole
from app.models.project_member import ProjectMember
from app.models.user import User
from app.repositories.project_member_repository import get_project_member
from app.repositories.project_repository import get_project_by_id
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
    if user is None:
        raise credentials_error
    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Reject authenticated users whose account is not active."""

    if current_user.status != UserStatus.ACTIVE.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Active user access is required.",
        )
    return current_user


def require_project_member(
    project_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> ProjectMember:
    """Require any project role for the requested project."""

    if get_project_by_id(db, project_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    membership = get_project_member(db, project_id, current_user.id)
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project membership is required.",
        )
    return membership


def require_project_owner_or_admin(
    membership: Annotated[ProjectMember, Depends(require_project_member)],
) -> ProjectMember:
    """Require the owner or admin role for a project-changing operation."""

    allowed_roles = {
        ProjectMemberRole.OWNER.value,
        ProjectMemberRole.ADMIN.value,
    }
    if membership.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project owner or admin access is required.",
        )
    return membership
