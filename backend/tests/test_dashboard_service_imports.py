"""Import and deterministic arithmetic tests for dashboard analytics."""

from decimal import Decimal
from types import SimpleNamespace
import uuid

from sqlalchemy.dialects import postgresql

from app.services import dashboard_analytics_service
from app.services import outcome_service


def test_dashboard_service_functions_are_importable() -> None:
    functions = (
        dashboard_analytics_service.get_project_overview,
        dashboard_analytics_service.list_project_workflow_runs,
        dashboard_analytics_service.get_project_cost_summary,
        dashboard_analytics_service.get_project_outcome_summary,
    )
    assert all(callable(function) for function in functions)


def test_cost_summary_uses_decimal_and_finds_highest_run(monkeypatch) -> None:
    project_id = uuid.uuid4()
    lower_run_id = uuid.uuid4()
    higher_run_id = uuid.uuid4()
    costs = [
        SimpleNamespace(
            workflow_run_id=lower_run_id,
            total_cost_usd=Decimal("0.10"),
            model_cost_usd=Decimal("0.08"),
            tool_cost_usd=Decimal("0.02"),
            total_tokens=100,
            model_call_count=1,
            tool_call_count=1,
        ),
        SimpleNamespace(
            workflow_run_id=higher_run_id,
            total_cost_usd=Decimal("0.30"),
            model_cost_usd=Decimal("0.25"),
            tool_cost_usd=Decimal("0.05"),
            total_tokens=300,
            model_call_count=2,
            tool_call_count=1,
        ),
    ]
    monkeypatch.setattr(
        dashboard_analytics_service,
        "_list_project_costs",
        lambda _db, _project_id: costs,
    )

    summary = dashboard_analytics_service.get_project_cost_summary(
        object(),
        project_id,
    )

    assert summary.total_cost_usd == Decimal("0.40000000")
    assert summary.average_cost_per_run_usd == Decimal("0.20000000")
    assert summary.total_tokens == 400
    assert summary.highest_cost_run_id == higher_run_id


def test_project_run_queries_use_workflow_project_ownership() -> None:
    project_id = uuid.uuid4()
    statements = (
        dashboard_analytics_service._project_runs_statement(project_id),
        dashboard_analytics_service._project_run_dashboard_statement(
            project_id,
            limit=50,
            offset=0,
        ),
        dashboard_analytics_service._project_costs_statement(project_id),
        outcome_service._workflow_run_metrics_statement(project_id=project_id),
    )

    for statement in statements:
        sql = str(
            statement.compile(
                dialect=postgresql.dialect(),
                compile_kwargs={"literal_binds": True},
            )
        ).lower()
        assert "join workflows on workflows.id = workflow_runs.workflow_id" in sql
        assert "where workflows.project_id =" in sql
