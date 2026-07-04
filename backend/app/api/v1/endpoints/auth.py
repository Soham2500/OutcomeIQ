"""Authentication endpoints for registration, login and current user."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    CurrentUserRead,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.services.auth_service import (
    authenticate_user,
    create_user_access_token,
    register_user,
)
from app.models.enums import AuditAction
from app.services.audit_service import record_audit_event


router = APIRouter()


@router.post(
    "/register",
    response_model=CurrentUserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    try:
        user = register_user(
            db,
            email=str(request.email),
            password=request.password,
            full_name=request.full_name,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        ) from exc

    record_audit_event(
        db,
        action=AuditAction.CREATE.value,
        message="User registered",
        actor_user_id=user.id,
        entity_type="user",
        entity_id=str(user.id),
    )
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    user = authenticate_user(db, str(request.email), request.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(access_token=create_user_access_token(user))


@router.get("/me", response_model=CurrentUserRead)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user
