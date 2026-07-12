"""Read-only project dashboard analytics assembled from Day 5 evidence."""

from decimal import Decimal, ROUND_HALF_UP
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.enums import WorkflowOutcomeStatus, WorkflowRunStatus
from app.models.ai_run import AiRun
from app.models.workflow import Workflow
from app.models.workflow_run import WorkflowRun
from app.models.workflow_run_cost import WorkflowRunCost
from app.repositories.workflow_run_cost_repository import (
    get_cost_by_workflow_run_id,
)
from app.repositories.workflow_run_outcome_repository import (
    get_outcome_by_workflow_run_id,
)
from app.schemas.dashboard import (
    AiCostBreakdownRead,
    CostDashboardSummaryRead,
    LatestAiRunDashboardRead,
    OutcomeDashboardSummaryRead,
    ProjectDashboardOverviewRead,
    WorkflowRunDashboardRead,
)
from app.services.outcome_service import (
    FAILED_OUTCOME_STATUSES,
    calculate_cost_per_successful_outcome,
)


MONEY_QUANTUM = Decimal("0.00000001")


def _money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def _list_project_runs(db: Session, project_id: uuid.UUID) -> list[WorkflowRun]:
    return list(db.scalars(_project_runs_statement(project_id)))


def _project_runs_statement(project_id: uuid.UUID):
    """Select runs through their workflow's canonical project ownership."""

    return (
        select(WorkflowRun)
        .join(Workflow, Workflow.id == WorkflowRun.workflow_id)
        .where(Workflow.project_id == project_id)
        .order_by(WorkflowRun.created_at, WorkflowRun.id)
    )


def _list_project_costs(
    db: Session,
    project_id: uuid.UUID,
) -> list[WorkflowRunCost]:
    return list(db.scalars(_project_costs_statement(project_id)))


def _project_costs_statement(project_id: uuid.UUID):
    """Select cost rows through run-to-workflow project ownership."""

    return (
        select(WorkflowRunCost)
        .join(
            WorkflowRun,
            WorkflowRun.id == WorkflowRunCost.workflow_run_id,
        )
        .join(Workflow, Workflow.id == WorkflowRun.workflow_id)
        .where(Workflow.project_id == project_id)
        .order_by(WorkflowRunCost.workflow_run_id)
    )


def get_project_overview(
    db: Session,
    project_id: uuid.UUID,
) -> ProjectDashboardOverviewRead:
    total_workflows = db.scalar(
        select(func.count())
        .select_from(Workflow)
        .where(Workflow.project_id == project_id)
    ) or 0
    workflow_runs = _list_project_runs(db, project_id)
    succeeded_runs = sum(
        run.status == WorkflowRunStatus.SUCCEEDED.value
        for run in workflow_runs
    )
    failed_runs = sum(
        run.status == WorkflowRunStatus.FAILED.value
        for run in workflow_runs
    )
    pending_runs = len(workflow_runs) - succeeded_runs - failed_runs
    cost_summary = get_project_cost_summary(db, project_id)
    outcome_metrics = calculate_cost_per_successful_outcome(
        db,
        project_id=project_id,
    )

    return ProjectDashboardOverviewRead(
        project_id=project_id,
        total_workflows=int(total_workflows),
        total_workflow_runs=len(workflow_runs),
        succeeded_runs=succeeded_runs,
        failed_runs=failed_runs,
        pending_runs=pending_runs,
        total_cost_usd=cost_summary.total_cost_usd,
        successful_outcomes=outcome_metrics.successful_runs,
        failed_outcomes=outcome_metrics.failed_runs,
        success_rate=outcome_metrics.success_rate,
        cost_per_successful_outcome_usd=(
            outcome_metrics.cost_per_successful_outcome_usd
        ),
        notes=outcome_metrics.notes,
    )


def list_project_workflow_runs(
    db: Session,
    project_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
) -> list[WorkflowRunDashboardRead]:
    statement = _project_run_dashboard_statement(
        project_id,
        limit=limit,
        offset=offset,
    )
    rows = db.execute(statement).all()
    results: list[WorkflowRunDashboardRead] = []
    for workflow_run, workflow_name in rows:
        cost = get_cost_by_workflow_run_id(db, workflow_run.id)
        outcome = get_outcome_by_workflow_run_id(db, workflow_run.id)
        success = None
        if outcome is not None:
            if outcome.status == WorkflowOutcomeStatus.SUCCEEDED.value:
                success = True
            elif outcome.status in FAILED_OUTCOME_STATUSES:
                success = False
        results.append(
            WorkflowRunDashboardRead(
                workflow_run_id=workflow_run.id,
                workflow_id=workflow_run.workflow_id,
                workflow_name=workflow_name,
                configuration_id=workflow_run.configuration_id,
                status=workflow_run.status,
                started_at=workflow_run.started_at,
                completed_at=workflow_run.completed_at,
                total_cost_usd=(cost.total_cost_usd if cost else None),
                outcome_status=(outcome.status if outcome else None),
                success=success,
            )
        )
    return results


def _project_run_dashboard_statement(
    project_id: uuid.UUID,
    limit: int,
    offset: int,
):
    """Select recent dashboard rows through workflow project ownership."""

    return (
        select(WorkflowRun, Workflow.name)
        .join(Workflow, Workflow.id == WorkflowRun.workflow_id)
        .where(Workflow.project_id == project_id)
        .order_by(WorkflowRun.created_at.desc(), WorkflowRun.id.desc())
        .offset(offset)
        .limit(limit)
    )


def _list_project_ai_runs(db: Session, project_id: uuid.UUID) -> list[AiRun]:
    if not hasattr(db, "scalars"):
        return []
    return list(
        db.scalars(
            select(AiRun)
            .where(AiRun.project_id == project_id)
            .order_by(AiRun.created_at.desc(), AiRun.id.desc())
        )
    )


def get_project_cost_summary(
    db: Session,
    project_id: uuid.UUID,
) -> CostDashboardSummaryRead:
    costs = _list_project_costs(db, project_id)
    ai_runs = _list_project_ai_runs(db, project_id)
    total_cost = sum(
        (Decimal(str(cost.total_cost_usd)) for cost in costs),
        Decimal("0"),
    )
    ai_cost_usd = sum(
        (Decimal(str(run.cost_usd)) for run in ai_runs),
        Decimal("0"),
    )
    ai_cost_inr = sum(
        (Decimal(str(run.cost_inr)) for run in ai_runs),
        Decimal("0"),
    )
    usd_to_inr_rate = Decimal(str(get_settings().USD_TO_INR_RATE))
    total_cost_inr = (total_cost * usd_to_inr_rate) + ai_cost_inr
    model_cost = sum(
        (Decimal(str(cost.model_cost_usd)) for cost in costs),
        Decimal("0"),
    )
    tool_cost = sum(
        (Decimal(str(cost.tool_cost_usd)) for cost in costs),
        Decimal("0"),
    )
    highest_cost = max(
        costs,
        key=lambda cost: Decimal(str(cost.total_cost_usd)),
        default=None,
    )
    average_cost = Decimal("0")
    if costs:
        average_cost = total_cost / Decimal(len(costs))
    total_tokens = sum(cost.total_tokens for cost in costs)
    ai_total_tokens = sum(run.total_tokens for run in ai_runs)

    return CostDashboardSummaryRead(
        project_id=project_id,
        total_cost_usd=_money(total_cost),
        total_cost_inr=_money(total_cost_inr),
        model_cost_usd=_money(model_cost),
        tool_cost_usd=_money(tool_cost),
        ai_cost_usd=_money(ai_cost_usd),
        ai_cost_inr=_money(ai_cost_inr),
        total_tokens=total_tokens + ai_total_tokens,
        ai_total_tokens=ai_total_tokens,
        model_call_count=sum(cost.model_call_count for cost in costs),
        tool_call_count=sum(cost.tool_call_count for cost in costs),
        ai_run_count=len(ai_runs),
        average_cost_per_run_usd=_money(average_cost),
        highest_cost_run_id=(
            highest_cost.workflow_run_id if highest_cost else None
        ),
        cost_by_provider=_ai_breakdown(ai_runs, "provider"),
        cost_by_model=_ai_breakdown(ai_runs, "model"),
        latest_ai_runs=[
            LatestAiRunDashboardRead(
                id=run.id,
                provider=run.provider,
                model=run.model,
                workflow_name=run.workflow_name,
                total_tokens=run.total_tokens,
                cost_inr=run.cost_inr,
                latency_ms=run.latency_ms,
                status=run.status,
                created_at=run.created_at,
            )
            for run in ai_runs[:5]
        ],
    )


def _ai_breakdown(ai_runs: list[AiRun], field_name: str) -> list[AiCostBreakdownRead]:
    buckets: dict[str, dict[str, Decimal | int]] = {}
    for run in ai_runs:
        key = str(getattr(run, field_name))
        bucket = buckets.setdefault(
            key,
            {
                "total_cost_inr": Decimal("0"),
                "total_cost_usd": Decimal("0"),
                "total_tokens": 0,
                "run_count": 0,
            },
        )
        bucket["total_cost_inr"] = Decimal(str(bucket["total_cost_inr"])) + Decimal(
            str(run.cost_inr)
        )
        bucket["total_cost_usd"] = Decimal(str(bucket["total_cost_usd"])) + Decimal(
            str(run.cost_usd)
        )
        bucket["total_tokens"] = int(bucket["total_tokens"]) + run.total_tokens
        bucket["run_count"] = int(bucket["run_count"]) + 1
    return [
        AiCostBreakdownRead(
            key=key,
            total_cost_inr=_money(Decimal(str(values["total_cost_inr"]))),
            total_cost_usd=_money(Decimal(str(values["total_cost_usd"]))),
            total_tokens=int(values["total_tokens"]),
            run_count=int(values["run_count"]),
        )
        for key, values in sorted(
            buckets.items(),
            key=lambda item: Decimal(str(item[1]["total_cost_inr"])),
            reverse=True,
        )
    ]


def get_project_outcome_summary(
    db: Session,
    project_id: uuid.UUID,
) -> OutcomeDashboardSummaryRead:
    metrics = calculate_cost_per_successful_outcome(
        db,
        project_id=project_id,
    )
    return OutcomeDashboardSummaryRead(
        project_id=project_id,
        total_runs=metrics.total_runs,
        successful_runs=metrics.successful_runs,
        failed_runs=metrics.failed_runs,
        pending_runs=metrics.pending_runs,
        success_rate=metrics.success_rate,
        cost_per_successful_outcome_usd=(
            metrics.cost_per_successful_outcome_usd
        ),
    )
