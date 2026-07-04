"""Metadata-registration tests for cost calculation models."""

from app.db.base import Base
from app.models.model_pricing_rate import ModelPricingRate
from app.models.workflow_run_cost import WorkflowRunCost


def test_cost_models_are_registered_with_base() -> None:
    expected_models = {
        ModelPricingRate: "model_pricing_rates",
        WorkflowRunCost: "workflow_run_costs",
    }

    assert {
        model.__tablename__ for model in expected_models
    } <= set(Base.metadata.tables)
    for model, table_name in expected_models.items():
        assert model.__table__ is Base.metadata.tables[table_name]
