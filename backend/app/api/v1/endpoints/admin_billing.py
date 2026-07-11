"""Admin-only read views for launch-safe billing inspection."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.services.admin_billing_service import (
    get_billing_overview,
    is_admin_email,
    list_payment_events_admin,
    list_subscriptions_admin,
    list_usage_admin,
)


router = APIRouter()


def require_admin_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """Allow admin billing access only for config-listed admin emails."""

    if not is_admin_email(current_user.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin billing access is restricted.",
        )
    return current_user


@router.get("/overview")
def get_admin_billing_overview_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _admin_user: Annotated[User, Depends(require_admin_user)],
) -> dict[str, object]:
    return get_billing_overview(db)


@router.get("/subscriptions")
def list_admin_subscriptions_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _admin_user: Annotated[User, Depends(require_admin_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[dict[str, object]]:
    return list_subscriptions_admin(db, limit=limit, offset=offset)


@router.get("/payment-events")
def list_admin_payment_events_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _admin_user: Annotated[User, Depends(require_admin_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[dict[str, object]]:
    return list_payment_events_admin(db, limit=limit, offset=offset)


@router.get("/usage")
def list_admin_usage_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _admin_user: Annotated[User, Depends(require_admin_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[dict[str, object]]:
    return list_usage_admin(db, limit=limit, offset=offset)
