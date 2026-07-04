"""Import and deterministic rule tests for recommendation service."""

from decimal import Decimal

from app.services import recommendation_service


def test_recommendation_service_functions_are_importable() -> None:
    functions = (
        recommendation_service.generate_project_recommendations,
        recommendation_service.list_project_recommendations,
        recommendation_service.update_recommendation_status,
    )
    assert all(callable(function) for function in functions)


def test_recommendation_rules_emit_expected_evidence_types() -> None:
    specs = recommendation_service._build_recommendation_specs(
        total_runs=3,
        missing_costs=1,
        missing_outcomes=1,
        total_outcomes=2,
        successful_outcomes=1,
        failed_outcomes=1,
        total_cost_usd=Decimal("0.50000000"),
        cost_per_successful_outcome_usd=Decimal("0.50000000"),
    )
    types = {spec["recommendation_type"] for spec in specs}

    assert types == {
        "missing_costs",
        "missing_outcomes",
        "high_failure_rate",
        "cost_per_success_opportunity",
    }


def test_no_runs_emits_only_data_quality_recommendation() -> None:
    specs = recommendation_service._build_recommendation_specs(
        total_runs=0,
        missing_costs=0,
        missing_outcomes=0,
        total_outcomes=0,
        successful_outcomes=0,
        failed_outcomes=0,
        total_cost_usd=Decimal("0"),
        cost_per_successful_outcome_usd=None,
    )

    assert len(specs) == 1
    assert specs[0]["recommendation_type"] == "data_quality"
