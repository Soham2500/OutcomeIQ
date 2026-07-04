"""Validation tests for dashboard analytics schemas."""

from decimal import Decimal
import uuid

from app.schemas.dashboard import (
    CostDashboardSummaryRead,
    OutcomeDashboardSummaryRead,
    ProjectDashboardOverviewRead,
    WorkflowRunDashboardRead,
)


def test_dashboard_schemas_accept_summary_data() -> None:
    project_id = uuid.uuid4()
    run_id = uuid.uuid4()
    workflow_id = uuid.uuid4()
    overview = ProjectDashboardOverviewRead(
        project_id=project_id,
        total_workflows=1,
        total_workflow_runs=2,
        succeeded_runs=2,
        failed_runs=0,
        pending_runs=0,
        total_cost_usd=Decimal("0.01000000"),
        successful_outcomes=1,
        failed_outcomes=1,
        success_rate=Decimal("0.50000000"),
        cost_per_successful_outcome_usd=Decimal("0.01000000"),
    )
    run = WorkflowRunDashboardRead(
        workflow_run_id=run_id,
        workflow_id=workflow_id,
        status="succeeded",
        outcome_status="succeeded",
        success=True,
    )
    cost = CostDashboardSummaryRead(
        project_id=project_id,
        total_cost_usd=Decimal("0.01000000"),
        model_cost_usd=Decimal("0.00800000"),
        tool_cost_usd=Decimal("0.00200000"),
        total_tokens=100,
        model_call_count=2,
        tool_call_count=1,
        average_cost_per_run_usd=Decimal("0.00500000"),
        highest_cost_run_id=run_id,
    )
    outcome = OutcomeDashboardSummaryRead(
        project_id=project_id,
        total_runs=2,
        successful_runs=1,
        failed_runs=1,
        pending_runs=0,
        success_rate=Decimal("0.50000000"),
        cost_per_successful_outcome_usd=Decimal("0.01000000"),
    )

    assert overview.total_workflow_runs == 2
    assert run.success is True
    assert cost.highest_cost_run_id == run_id
    assert outcome.success_rate == Decimal("0.50000000")
