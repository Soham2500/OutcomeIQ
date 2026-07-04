"""Authentication use cases built on the existing user repository."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.enums import UserStatus
from app.models.user import User
from app.repositories.user_repository import create_user, get_user_by_email


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
