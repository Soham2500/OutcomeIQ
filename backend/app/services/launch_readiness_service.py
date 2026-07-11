"""Launch readiness checks that expose booleans, never secrets."""

from app.core.config import get_settings
from app.services.razorpay_service import is_configured as razorpay_is_configured


def get_launch_readiness() -> dict[str, object]:
    """Return a safe checklist for pre-launch review."""

    settings = get_settings()
    app_env = settings.ENVIRONMENT.strip().lower()
    return {
        "app_env": app_env,
        "debug_disabled": not settings.DEBUG,
        "cors_configured": len(settings.cors_origins) > 0,
        "database_configured": settings.database_configured,
        "payments_live_enabled": settings.PAYMENTS_LIVE_ENABLED,
        "razorpay_test_configured": (
            razorpay_is_configured("starter") or razorpay_is_configured("pro")
        ),
        "policy_pages_expected": True,
        "support_email_configured": bool(settings.SUPPORT_EMAIL),
        "admin_emails_configured": bool(settings.admin_email_set),
        "openai_live_enabled": False,
        "note": "This endpoint returns launch-safety booleans only and does not expose secrets.",
    }
