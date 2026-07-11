"""Protected subscription-ready billing endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.billing import (
    BillingCheckoutRequest,
    BillingCheckoutResponse,
    BillingMeRead,
    BillingWebhookResponse,
    PlanRead,
    SubscriptionRead,
    UsageSummaryRead,
)
from app.services.billing_service import (
    activate_test_subscription,
    cancel_subscription,
    create_test_checkout_response,
    get_current_plan_and_subscription,
    list_active_plans,
    update_subscription_status_from_test_webhook,
)
from app.services.razorpay_service import (
    verify_webhook_signature,
    webhook_secret_configured,
)
from app.services.usage_limit_service import get_usage_summary


router = APIRouter()


@router.get("/plans", response_model=list[PlanRead])
def list_billing_plans_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_active_user)],
) -> list[object]:
    return list_active_plans(db)


@router.get("/me", response_model=BillingMeRead)
def get_my_billing_endpoint(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, object]:
    plan, subscription = get_current_plan_and_subscription(db, current_user.id)
    usage = get_usage_summary(db, current_user.id)
    return {
        "plan": plan,
        "subscription": subscription,
        "usage": usage,
        "payment_mode": "test/sandbox",
    }


@router.post("/checkout", response_model=BillingCheckoutResponse)
def create_checkout_endpoint(
    request: BillingCheckoutRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, object]:
    try:
        return create_test_checkout_response(db, current_user, request.plan_slug)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/test/activate", response_model=SubscriptionRead)
def activate_test_plan_endpoint(
    request: BillingCheckoutRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> object:
    try:
        return activate_test_subscription(db, current_user.id, request.plan_slug)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/cancel", response_model=SubscriptionRead)
def cancel_subscription_endpoint(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> object:
    return cancel_subscription(db, current_user.id)


@router.post("/webhook/razorpay", response_model=BillingWebhookResponse)
async def razorpay_webhook_endpoint(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, object]:
    raw_body = await request.body()
    try:
        import json

        payload = json.loads(raw_body.decode("utf-8") or "{}")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Webhook payload must be valid JSON.",
        ) from exc
    if not isinstance(payload, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Webhook payload must be a JSON object.",
        )
    signature_valid = False
    if webhook_secret_configured():
        signature = request.headers.get("X-Razorpay-Signature")
        signature_valid = verify_webhook_signature(raw_body, signature)
        if not signature_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Razorpay webhook signature.",
            )
    event = update_subscription_status_from_test_webhook(
        db,
        payload,
        signature_valid=signature_valid,
    )
    return {
        "stored": True,
        "processed": event.processed,
        "message": (
            "Webhook verified and processed in test mode."
            if event.processed
            else "Webhook stored in test mode. No subscription update was applied."
        ),
    }


@router.get("/usage", response_model=UsageSummaryRead)
def get_usage_endpoint(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, object]:
    return get_usage_summary(db, current_user.id)
