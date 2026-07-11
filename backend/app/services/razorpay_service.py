"""Safe Razorpay checkout and webhook helpers.

This module never decides subscription entitlement. It only prepares Razorpay
checkout payloads and verifies webhook signatures. Backend billing services
update subscription state after verified webhook events or controlled local test
activation.
"""

from __future__ import annotations

import hashlib
import hmac
import importlib.util
from typing import Any

from app.core.config import get_settings
from app.models.user import User


PLAN_AMOUNTS_IN_PAISE = {
    "starter": 49900,
    "pro": 149900,
}


def _plan_id_for_slug(plan_slug: str) -> str | None:
    settings = get_settings()
    if plan_slug == "starter":
        return settings.RAZORPAY_STARTER_PLAN_ID
    if plan_slug == "pro":
        return settings.RAZORPAY_PRO_PLAN_ID
    return None


def _sdk_available() -> bool:
    return importlib.util.find_spec("razorpay") is not None


def _current_mode() -> str:
    return get_settings().RAZORPAY_MODE.strip().lower()


def is_live_payment_allowed() -> bool:
    """Return true only when live mode and the explicit live flag are enabled."""

    settings = get_settings()
    return (
        settings.RAZORPAY_MODE.strip().lower() == "live"
        and settings.PAYMENTS_LIVE_ENABLED
    )


def _provider_for_mode() -> str:
    return "razorpay_live" if _current_mode() == "live" else "razorpay_test"


def is_configured(plan_slug: str | None = None) -> bool:
    """Return true only when checkout is enabled and required env vars exist."""

    settings = get_settings()
    mode = settings.RAZORPAY_MODE.strip().lower()
    if mode not in {"test", "live"}:
        return False
    if mode == "live" and not settings.PAYMENTS_LIVE_ENABLED:
        return False
    if not settings.RAZORPAY_CHECKOUT_ENABLED:
        return False
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return False
    if plan_slug is not None and not _plan_id_for_slug(plan_slug):
        return False
    return _sdk_available()


def create_subscription_checkout(
    user: User,
    plan_slug: str,
) -> dict[str, Any]:
    """Create a Razorpay subscription and return a safe checkout payload."""

    if plan_slug not in {"starter", "pro"}:
        raise ValueError("Razorpay checkout is available only for paid plans.")
    settings = get_settings()
    mode = settings.RAZORPAY_MODE.strip().lower()
    if mode == "live" and not settings.PAYMENTS_LIVE_ENABLED:
        raise RuntimeError(
            "Live payments are disabled. Use test mode until launch approval is complete."
        )
    if not is_configured(plan_slug):
        raise RuntimeError(
            "Razorpay is not configured. Use local test activation or set backend environment variables."
        )

    # Import lazily so local development and tests do not require configured keys.
    import razorpay  # type: ignore[import-untyped]  # noqa: PLC0415

    plan_id = _plan_id_for_slug(plan_slug)
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET),
    )
    subscription = client.subscription.create(
        {
            "plan_id": plan_id,
            "total_count": 12,
            "customer_notify": 1,
            "notes": {
                "source": "outcomeiq_test_mode",
                "plan_slug": plan_slug,
                "user_id": str(user.id),
            },
        }
    )
    subscription_id = str(subscription.get("id", ""))
    amount = PLAN_AMOUNTS_IN_PAISE[plan_slug]
    title = f"OutcomeIQ {plan_slug.title()} Plan"
    return {
        "provider": _provider_for_mode(),
        "mode": mode,
        "checkout_type": "razorpay_subscription",
        "key_id": settings.RAZORPAY_KEY_ID,
        "subscription_id": subscription_id,
        "order_id": None,
        "plan_slug": plan_slug,
        "amount": amount,
        "currency": "INR",
        "name": title,
        "description": (
            "OutcomeIQ Razorpay subscription checkout. Subscription activates "
            "after backend webhook confirmation."
        ),
        "prefill_email": user.email,
        "prefill_name": user.full_name,
        "prefill": {
            "email": user.email,
            "name": user.full_name,
        },
        "message": "Razorpay checkout created. Complete payment and wait for secure webhook confirmation.",
    }


def create_test_subscription_checkout(
    user: User,
    plan_slug: str,
) -> dict[str, Any]:
    """Backward-compatible alias for older Day 13 imports."""

    return create_subscription_checkout(user, plan_slug)


def webhook_secret_configured() -> bool:
    return bool(get_settings().RAZORPAY_WEBHOOK_SECRET)


def verify_webhook_signature(raw_body: bytes, signature: str | None) -> bool:
    """Verify Razorpay webhook signature using HMAC SHA256."""

    secret = get_settings().RAZORPAY_WEBHOOK_SECRET
    if not secret or not signature:
        return False
    digest = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


def parse_webhook_event(payload: dict[str, Any]) -> dict[str, str | None]:
    """Extract safe identifiers from a Razorpay webhook payload."""

    event_type = str(payload.get("event") or "unknown")
    payload_root = payload.get("payload")
    payload_data = payload_root if isinstance(payload_root, dict) else {}

    subscription_entity = {}
    payment_entity = {}
    if isinstance(payload_data.get("subscription"), dict):
        subscription_wrapper = payload_data["subscription"]
        if isinstance(subscription_wrapper.get("entity"), dict):
            subscription_entity = subscription_wrapper["entity"]
    if isinstance(payload_data.get("payment"), dict):
        payment_wrapper = payload_data["payment"]
        if isinstance(payment_wrapper.get("entity"), dict):
            payment_entity = payment_wrapper["entity"]

    subscription_id = (
        subscription_entity.get("id")
        or payment_entity.get("subscription_id")
        or payload.get("subscription_id")
    )
    payment_id = payment_entity.get("id") or payload.get("payment_id")
    subscription_status = subscription_entity.get("status")
    customer_email = payment_entity.get("email") or payload.get("email")

    return {
        "event_type": event_type,
        "subscription_id": str(subscription_id) if subscription_id else None,
        "payment_id": str(payment_id) if payment_id else None,
        "subscription_status": (
            str(subscription_status) if subscription_status else None
        ),
        "customer_email": str(customer_email) if customer_email else None,
    }


def parse_subscription_event(payload: dict[str, Any]) -> dict[str, str | None]:
    """Backward-compatible alias for older Day 13 imports."""

    return parse_webhook_event(payload)
