"""Read-only admin billing summaries with safe provider identifiers."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.payment_event import PaymentEvent
from app.models.plan import Plan
from app.models.subscription import Subscription
from app.models.usage_counter import UsageCounter
from app.models.user import User


def is_admin_email(email: str) -> bool:
    """Return true when the authenticated user is listed in ADMIN_EMAILS."""

    return email.strip().lower() in get_settings().admin_email_set


def mask_provider_id(value: str | None) -> str | None:
    """Mask external provider IDs before returning admin billing responses."""

    if not value:
        return None
    if len(value) <= 10:
        return f"{value[:2]}...{value[-2:]}"
    return f"{value[:6]}...{value[-4:]}"


def get_billing_overview(db: Session) -> dict[str, object]:
    """Return aggregate billing health without exposing payment payloads."""

    total_users = db.scalar(select(func.count()).select_from(User)) or 0
    total_subscriptions = db.scalar(select(func.count()).select_from(Subscription)) or 0
    total_payment_events = db.scalar(select(func.count()).select_from(PaymentEvent)) or 0
    unprocessed_events = (
        db.scalar(
            select(func.count())
            .select_from(PaymentEvent)
            .where(PaymentEvent.processed.is_(False))
        )
        or 0
    )

    status_rows = db.execute(
        select(Subscription.status, func.count())
        .group_by(Subscription.status)
        .order_by(Subscription.status)
    ).all()
    plan_rows = db.execute(
        select(Plan.slug, func.count(Subscription.id))
        .join(Subscription, Subscription.plan_id == Plan.id)
        .group_by(Plan.slug)
        .order_by(Plan.slug)
    ).all()

    return {
        "total_users": total_users,
        "total_subscriptions": total_subscriptions,
        "total_payment_events": total_payment_events,
        "unprocessed_payment_events": unprocessed_events,
        "subscription_status_counts": {
            str(status): count for status, count in status_rows
        },
        "subscription_plan_counts": {str(slug): count for slug, count in plan_rows},
        "note": "Admin billing is read-only and hides raw payment payloads.",
    }


def list_subscriptions_admin(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, object]]:
    """Return recent subscription rows with masked provider references."""

    rows = db.execute(
        select(Subscription, User.email, Plan.slug, Plan.name)
        .join(User, User.id == Subscription.user_id)
        .join(Plan, Plan.id == Subscription.plan_id)
        .order_by(Subscription.created_at.desc(), Subscription.id.desc())
        .limit(limit)
        .offset(offset)
    ).all()
    return [
        {
            "id": subscription.id,
            "user_email": email,
            "plan_slug": plan_slug,
            "plan_name": plan_name,
            "status": subscription.status,
            "provider": subscription.provider,
            "provider_subscription_id": mask_provider_id(
                subscription.provider_subscription_id
            ),
            "current_period_start": subscription.current_period_start,
            "current_period_end": subscription.current_period_end,
            "cancel_at_period_end": subscription.cancel_at_period_end,
            "created_at": subscription.created_at,
            "updated_at": subscription.updated_at,
        }
        for subscription, email, plan_slug, plan_name in rows
    ]


def list_payment_events_admin(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, object]]:
    """Return payment event metadata only; raw payload_json is intentionally hidden."""

    events = db.scalars(
        select(PaymentEvent)
        .order_by(PaymentEvent.created_at.desc(), PaymentEvent.id.desc())
        .limit(limit)
        .offset(offset)
    )
    return [
        {
            "id": event.id,
            "provider": event.provider,
            "event_type": event.event_type,
            "provider_event_id": mask_provider_id(event.provider_event_id),
            "processed": event.processed,
            "processed_at": event.processed_at,
            "created_at": event.created_at,
        }
        for event in events
    ]


def list_usage_admin(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, object]]:
    """Return usage counters with user email and no secret data."""

    rows = db.execute(
        select(UsageCounter, User.email)
        .join(User, User.id == UsageCounter.user_id)
        .order_by(UsageCounter.period_month.desc(), UsageCounter.updated_at.desc())
        .limit(limit)
        .offset(offset)
    ).all()
    return [
        {
            "id": usage.id,
            "user_email": email,
            "period_month": usage.period_month,
            "projects_used": usage.projects_used,
            "workflow_runs_used": usage.workflow_runs_used,
            "created_at": usage.created_at,
            "updated_at": usage.updated_at,
        }
        for usage, email in rows
    ]
