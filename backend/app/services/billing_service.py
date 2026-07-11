"""Provider-neutral subscription billing service for test-mode launch prep."""

from datetime import datetime, timedelta, timezone
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import PaymentProvider, SubscriptionStatus
from app.models.payment_event import PaymentEvent
from app.models.plan import Plan
from app.models.subscription import Subscription


FREE_PLAN = {
    "name": "Free",
    "slug": "free",
    "description": "Free MVP plan for simulated OutcomeIQ usage.",
    "price_inr_monthly": 0,
    "currency": "INR",
    "max_projects": 1,
    "max_workflow_runs_per_month": 50,
    "max_team_members": 1,
    "export_enabled": False,
    "analytics_enabled": True,
    "recommendations_enabled": True,
    "openai_provider_enabled": False,
    "is_active": True,
}


def list_active_plans(db: Session) -> list[Plan]:
    return list(
        db.scalars(
            select(Plan).where(Plan.is_active.is_(True)).order_by(Plan.price_inr_monthly, Plan.name)
        )
    )


def get_plan_by_slug(db: Session, slug: str) -> Plan | None:
    return db.scalar(select(Plan).where(Plan.slug == slug))


def ensure_free_plan(db: Session) -> Plan:
    plan = get_plan_by_slug(db, "free")
    if plan is not None:
        return plan
    plan = Plan(**FREE_PLAN)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_current_subscription(db: Session, user_id: uuid.UUID) -> Subscription | None:
    return db.scalar(
        select(Subscription)
        .where(Subscription.user_id == user_id)
        .order_by(Subscription.created_at.desc(), Subscription.id.desc())
    )


def ensure_default_subscription(db: Session, user_id: uuid.UUID) -> Subscription:
    subscription = get_current_subscription(db, user_id)
    if subscription is not None:
        return subscription

    plan = ensure_free_plan(db)
    now = datetime.now(timezone.utc)
    subscription = Subscription(
        user_id=user_id,
        plan_id=plan.id,
        status=SubscriptionStatus.FREE.value,
        provider=PaymentProvider.MANUAL.value,
        current_period_start=now,
        current_period_end=now + timedelta(days=30),
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


def get_current_plan_and_subscription(
    db: Session,
    user_id: uuid.UUID,
) -> tuple[Plan, Subscription]:
    subscription = ensure_default_subscription(db, user_id)
    plan = db.get(Plan, subscription.plan_id)
    if plan is None:
        plan = ensure_free_plan(db)
        subscription.plan_id = plan.id
        subscription.status = SubscriptionStatus.FREE.value
        subscription.provider = PaymentProvider.MANUAL.value
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
    return plan, subscription


def create_test_checkout_response(db: Session, plan_slug: str) -> dict[str, str]:
    plan = get_plan_by_slug(db, plan_slug)
    if plan is None or not plan.is_active:
        raise LookupError("Plan not found.")
    return {
        "provider": PaymentProvider.RAZORPAY_TEST.value,
        "plan_slug": plan.slug,
        "test_checkout_url": f"https://checkout.razorpay.test/outcomeiq/{plan.slug}",
        "message": "Test checkout prepared. No real payment gateway was called.",
    }


def activate_test_subscription(
    db: Session,
    user_id: uuid.UUID,
    plan_slug: str,
) -> Subscription:
    plan = get_plan_by_slug(db, plan_slug)
    if plan is None or not plan.is_active:
        raise LookupError("Plan not found.")

    subscription = ensure_default_subscription(db, user_id)
    now = datetime.now(timezone.utc)
    subscription.plan_id = plan.id
    subscription.status = (
        SubscriptionStatus.FREE.value
        if plan.slug == "free"
        else SubscriptionStatus.ACTIVE.value
    )
    subscription.provider = (
        PaymentProvider.MANUAL.value
        if plan.slug == "free"
        else PaymentProvider.RAZORPAY_TEST.value
    )
    subscription.provider_subscription_id = f"test_{plan.slug}_{user_id.hex[:8]}"
    subscription.current_period_start = now
    subscription.current_period_end = now + timedelta(days=30)
    subscription.cancel_at_period_end = False
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


def cancel_subscription(db: Session, user_id: uuid.UUID) -> Subscription:
    subscription = ensure_default_subscription(db, user_id)
    free_plan = ensure_free_plan(db)
    subscription.plan_id = free_plan.id
    subscription.status = SubscriptionStatus.CANCELLED.value
    subscription.provider = PaymentProvider.MANUAL.value
    subscription.cancel_at_period_end = True
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


def store_razorpay_test_event(
    db: Session,
    payload: dict[str, object],
) -> PaymentEvent:
    event = PaymentEvent(
        provider=PaymentProvider.RAZORPAY_TEST.value,
        event_type=str(payload.get("event") or "unknown"),
        provider_event_id=str(payload.get("id")) if payload.get("id") else None,
        payload_json=payload,
        processed=False,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update_subscription_status_from_test_webhook(
    db: Session,
    payload: dict[str, object],
) -> PaymentEvent:
    """Store test webhook payloads for later verification.

    Real provider signature verification and subscription mapping are intentionally
    deferred until live-payment readiness.
    """

    return store_razorpay_test_event(db, payload)
