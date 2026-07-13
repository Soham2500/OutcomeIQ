"""Authentication use cases built on the existing user repository."""

from datetime import datetime, timedelta, timezone
import secrets

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.enums import UserStatus
from app.models.pending_registration import PendingRegistration
from app.models.user import User
from app.repositories.user_repository import create_user, get_user_by_email
from app.services.email_service import send_registration_otp_email


MAX_OTP_ATTEMPTS = 5


class DuplicateActiveUserError(ValueError):
    """Raised when an active account already owns an email."""


class OTPRateLimitError(ValueError):
    """Raised when a pending registration requests OTP too quickly."""


class OTPVerificationError(ValueError):
    """Raised when an OTP cannot be verified."""


class OTPAttemptLimitError(OTPVerificationError):
    """Raised when too many wrong OTP attempts have occurred."""


def normalize_email(email: str) -> str:
    """Use one stable representation for registration and login lookups."""

    return email.strip().lower()


def register_user(
    db: Session,
    email: str,
    password: str,
    full_name: str | None = None,
) -> User:
    normalized_email = normalize_email(email)
    if get_user_by_email(db, normalized_email) is not None:
        raise ValueError("An account with this email already exists.")

    try:
        return create_user(
            db,
            email=normalized_email,
            full_name=full_name,
            hashed_password=get_password_hash(password),
        )
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("An account with this email already exists.") from exc


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _as_aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def generate_numeric_otp() -> str:
    """Generate a six-digit OTP with cryptographically secure randomness."""

    return f"{secrets.randbelow(1_000_000):06d}"


def get_pending_registration(
    db: Session,
    email: str,
) -> PendingRegistration | None:
    normalized_email = normalize_email(email)
    return db.scalar(
        select(PendingRegistration).where(
            PendingRegistration.email == normalized_email
        )
    )


def request_registration_otp(
    db: Session,
    email: str,
    password: str,
    full_name: str | None = None,
) -> None:
    """Create or update a pending registration and email its OTP."""

    settings = get_settings()
    normalized_email = normalize_email(email)
    existing_user = get_user_by_email(db, normalized_email)
    if existing_user is not None and existing_user.status == UserStatus.ACTIVE.value:
        raise DuplicateActiveUserError("An active account with this email exists.")
    if existing_user is not None:
        raise DuplicateActiveUserError("An account with this email exists.")

    now = _now()
    pending = get_pending_registration(db, normalized_email)
    cooldown_seconds = max(0, settings.OTP_RESEND_COOLDOWN_SECONDS)
    if pending is not None and cooldown_seconds > 0:
        last_sent_at = _as_aware(pending.last_sent_at)
        if now < last_sent_at + timedelta(seconds=cooldown_seconds):
            raise OTPRateLimitError("Please wait before requesting another OTP.")

    otp = generate_numeric_otp()
    expires_at = now + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    if pending is None:
        pending = PendingRegistration(
            email=normalized_email,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            hashed_otp=get_password_hash(otp),
            otp_expires_at=expires_at,
            otp_attempts=0,
            last_sent_at=now,
        )
        db.add(pending)
    else:
        pending.full_name = full_name
        pending.hashed_password = get_password_hash(password)
        pending.hashed_otp = get_password_hash(otp)
        pending.otp_expires_at = expires_at
        pending.otp_attempts = 0
        pending.last_sent_at = now

    try:
        db.flush()
        send_registration_otp_email(normalized_email, otp)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateActiveUserError("An account with this email exists.") from exc
    except Exception:
        db.rollback()
        raise


def verify_registration_otp(
    db: Session,
    email: str,
    otp: str,
) -> User:
    """Verify pending registration OTP and create an active user."""

    normalized_email = normalize_email(email)
    existing_user = get_user_by_email(db, normalized_email)
    if existing_user is not None and existing_user.status == UserStatus.ACTIVE.value:
        pending = get_pending_registration(db, normalized_email)
        if pending is not None:
            db.delete(pending)
            db.commit()
        raise DuplicateActiveUserError("An active account with this email exists.")
    if existing_user is not None:
        pending = get_pending_registration(db, normalized_email)
        if pending is not None:
            db.delete(pending)
            db.commit()
        raise DuplicateActiveUserError("An account with this email exists.")

    pending = get_pending_registration(db, normalized_email)
    if pending is None:
        raise OTPVerificationError("No pending registration found.")

    now = _now()
    if now > _as_aware(pending.otp_expires_at):
        db.delete(pending)
        db.commit()
        raise OTPVerificationError("OTP has expired. Please request a new OTP.")

    if pending.otp_attempts >= MAX_OTP_ATTEMPTS:
        raise OTPAttemptLimitError("Too many wrong OTP attempts.")

    if not verify_password(otp, pending.hashed_otp):
        pending.otp_attempts += 1
        db.commit()
        if pending.otp_attempts >= MAX_OTP_ATTEMPTS:
            raise OTPAttemptLimitError("Too many wrong OTP attempts.")
        raise OTPVerificationError("Invalid OTP.")

    user = User(
        email=pending.email,
        full_name=pending.full_name,
        hashed_password=pending.hashed_password,
        status=UserStatus.ACTIVE.value,
    )
    try:
        db.add(user)
        db.delete(pending)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateActiveUserError("An account with this email exists.") from exc


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, normalize_email(email))
    if user is None or user.hashed_password is None:
        return None
    if user.status != UserStatus.ACTIVE.value:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user_access_token(user: User) -> str:
    return create_access_token(subject=str(user.id))
