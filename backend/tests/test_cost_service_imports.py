"""Import and deterministic arithmetic tests for cost calculation."""

from decimal import Decimal
from types import SimpleNamespace

from app.services import cost_calculation_service


def test_cost_service_functions_are_importable() -> None:
    assert callable(cost_calculation_service.calculate_model_call_cost)
    assert callable(cost_calculation_service.calculate_workflow_run_cost)


def test_model_call_cost_uses_configured_decimal_rate(monkeypatch) -> None:
    rate = SimpleNamespace(
        input_token_price_per_1k=Decimal("0.00100000"),
        output_token_price_per_1k=Decimal("0.00300000"),
    )
    model_call = SimpleNamespace(
        provider="simulated",
        model_name="test-model",
        prompt_tokens=1000,
        completion_tokens=500,
        estimated_cost_usd=None,
    )
    monkeypatch.setattr(
        cost_calculation_service,
        "get_active_rate",
        lambda *args, **kwargs: rate,
    )

    result = cost_calculation_service.calculate_model_call_cost(
        db=object(),
        model_call=model_call,
    )

    assert result["cost_usd"] == Decimal("0.00250000")
    assert result["status"] == "calculated"
    assert result["source"] == "pricing_rate"
