"""Route and helper coverage for Day 14 launch-safety additions."""

from app.core.config import Settings
from app.main import app
from app.services.admin_billing_service import mask_provider_id


def test_day14_launch_safety_routes_are_registered() -> None:
    expected_paths = {
        "/api/v1/admin/billing/overview",
        "/api/v1/admin/billing/subscriptions",
        "/api/v1/admin/billing/payment-events",
        "/api/v1/admin/billing/usage",
        "/api/v1/launch/readiness",
    }

    assert expected_paths <= set(app.openapi()["paths"])


def test_admin_email_settings_are_normalized() -> None:
    settings = Settings(ADMIN_EMAILS="Admin@Example.com, second@example.com")

    assert settings.admin_email_set == {"admin@example.com", "second@example.com"}


def test_provider_ids_are_masked_for_admin_billing() -> None:
    assert mask_provider_id("sub_1234567890abcdef") == "sub_12...cdef"
    assert mask_provider_id(None) is None
