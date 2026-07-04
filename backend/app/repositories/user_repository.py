"""Database access functions for users."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.get(User, user_id)


def create_user(
    db: Session,
    email: str,
    full_name: str | None = None,
    hashed_password: str | None = None,
) -> User:
    user = User(
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session, limit: int = 50, offset: int = 0) -> list[User]:
    statement = (
        select(User)
        .order_by(User.created_at, User.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))
