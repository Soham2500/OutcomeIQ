"""Import and costing tests for real AI run support."""

from decimal import Decimal

import pytest

from app.api.v1.endpoints import ai_runs
from app.schemas.ai_run import AiRunCreate
from app.services.ai.costing import calculate_ai_cost
from app.services.ai.service import AiRunValidationError, _normalize_provider


def test_ai_run_routes_are_importable() -> None:
    route_paths = {route.path for route in ai_runs.router.routes}
    assert route_paths == {"/runs"}


def test_ai_schema_accepts_gemini_35_flash_payload() -> None:
    request = AiRunCreate(
        project_id="00000000-0000-0000-0000-000000000001",
        workflow_name="AI Test",
        prompt="Summarize this synthetic workflow.",
        provider="gemini",
        model="gemini-3.5-flash",
    )

    assert request.model == "gemini-3.5-flash"


def test_ai_costing_includes_gemini_35_flash() -> None:
    cost = calculate_ai_cost(
        provider="gemini",
        model="gemini-3.5-flash",
        input_tokens=1_000_000,
        output_tokens=1_000_000,
        usd_to_inr_rate=Decimal("83.50"),
    )

    assert cost.pricing_unknown is False
    assert cost.cost_usd > Decimal("0")
    assert cost.cost_inr > Decimal("0")


def test_ai_costing_unknown_model_falls_back_to_zero_cost() -> None:
    cost = calculate_ai_cost(
        provider="gemini",
        model="unknown-model",
        input_tokens=10_000,
        output_tokens=10_000,
        usd_to_inr_rate=Decimal("83.50"),
    )

    assert cost.pricing_unknown is True
    assert cost.cost_usd == Decimal("0E-8")
    assert cost.cost_inr == Decimal("0E-8")


def test_provider_allowlist_rejects_unknown_provider() -> None:
    with pytest.raises(AiRunValidationError):
        _normalize_provider("not-a-provider")
