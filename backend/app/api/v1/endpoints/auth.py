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
    MessageResponse,
    RegisterOtpRequest,
    RegisterRequest,
    TokenResponse,
    VerifyRegistrationOtpRequest,
)
from app.services.auth_service import (
    DuplicateActiveUserError,
    OTPAttemptLimitError,
    OTPRateLimitError,
    OTPVerificationError,
    authenticate_user,
    create_user_access_token,
    request_registration_otp,
    verify_registration_otp,
)
from app.models.enums import AuditAction
from app.services.audit_service import record_audit_event


router = APIRouter()


def _request_registration_otp_or_raise(
    request: RegisterRequest,
    db: Session,
) -> MessageResponse:
    try:
        request_registration_otp(
            db,
            email=str(request.email),
            password=request.password,
            full_name=request.full_name,
        )
    except DuplicateActiveUserError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        ) from exc
    except OTPRateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Please wait before requesting another OTP.",
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not send OTP email. SMTP is not configured correctly.",
        ) from exc

    return MessageResponse(message="OTP sent")


@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_202_ACCEPTED,
    deprecated=True,
)
def register(
    request: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
) -> MessageResponse:
    return _request_registration_otp_or_raise(request, db)


@router.post("/register/request-otp", response_model=MessageResponse)
def request_register_otp(
    request: RegisterOtpRequest,
    db: Annotated[Session, Depends(get_db)],
) -> MessageResponse:
    return _request_registration_otp_or_raise(request, db)


@router.post(
    "/register/verify-otp",
    response_model=CurrentUserRead,
    status_code=status.HTTP_201_CREATED,
)
def verify_register_otp(
    request: VerifyRegistrationOtpRequest,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    try:
        user = verify_registration_otp(
            db,
            email=str(request.email),
            otp=request.otp,
        )
    except DuplicateActiveUserError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        ) from exc
    except OTPAttemptLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many wrong OTP attempts. Please request a new OTP.",
        ) from exc
    except OTPVerificationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    record_audit_event(
        db,
        action=AuditAction.CREATE.value,
        message="User registered via email OTP",
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
