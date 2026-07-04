"""Validation tests for cost calculation schemas."""

from decimal import Decimal

from app.schemas.model_pricing_rate import (
    ModelPricingRateCreate,
    ModelPricingRateRead,
    ModelPricingRateUpdate,
)
from app.schemas.workflow_run_cost import (
    WorkflowRunCostCalculateResponse,
    WorkflowRunCostRead,
)


def test_cost_schemas_accept_decimal_demo_rates() -> None:
    rate = ModelPricingRateCreate(
        provider="simulated",
        model_name="support-classifier-small",
        input_token_price_per_1k=Decimal("0.0001"),
        output_token_price_per_1k=Decimal("0.0002"),
    )
    update = ModelPricingRateUpdate(is_active=False)

    assert rate.currency == "USD"
    assert rate.input_token_price_per_1k == Decimal("0.0001")
    assert update.is_active is False
    assert ModelPricingRateRead.model_config["from_attributes"] is True
    assert WorkflowRunCostRead.model_config["from_attributes"] is True
    assert WorkflowRunCostCalculateResponse.model_config["from_attributes"] is True
