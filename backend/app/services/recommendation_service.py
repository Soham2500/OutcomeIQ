"""Deterministic, non-autonomous recommendation rules."""

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import (
    RecommendationSeverity,
    RecommendationStatus,
    RecommendationType,
    WorkflowOutcomeStatus,
)
from app.models.recommendation import Recommendation
from app.models.workflow import Workflow
from app.models.workflow_run import WorkflowRun
from app.repositories.project_repository import get_project_by_id
from app.repositories.recommendation_repository import (
    create_recommendation,
    delete_open_recommendations_for_project,
    get_recommendation_by_id,
    list_recommendations,
    update_recommendation,
)
from app.repositories.workflow_repository import get_workflow_by_id
from app.repositories.workflow_run_cost_repository import (
    get_cost_by_workflow_run_id,
)
from app.repositories.workflow_run_outcome_repository import (
    get_outcome_by_workflow_run_id,
)
from app.schemas.recommendation import RecommendationGenerateResponse
from app.services.outcome_service import FAILED_OUTCOME_STATUSES


MONEY_QUANTUM = Decimal("0.00000001")
RATE_QUANTUM = Decimal("0.00000001")


def _list_runs(
    db: Session,
    project_id: uuid.UUID,
    workflow_id: uuid.UUID | None,
) -> list[WorkflowRun]:
    statement = (
        select(WorkflowRun)
        .join(Workflow, Workflow.id == WorkflowRun.workflow_id)
        .where(Workflow.project_id == project_id)
    )
    if workflow_id is not None:
        statement = statement.where(WorkflowRun.workflow_id == workflow_id)
    return list(db.scalars(statement.order_by(WorkflowRun.id)))


def _build_recommendation_specs(
    *,
    total_runs: int,
    missing_costs: int,
    missing_outcomes: int,
    total_outcomes: int,
    successful_outcomes: int,
    failed_outcomes: int,
    total_cost_usd: Decimal,
    cost_per_successful_outcome_usd: Decimal | None,
) -> list[dict[str, object]]:
    """Return deterministic recommendation definitions from aggregate facts."""

    specs: list[dict[str, object]] = []
    if total_runs == 0:
        specs.append(
            {
                "recommendation_type": RecommendationType.DATA_QUALITY.value,
                "severity": RecommendationSeverity.LOW.value,
                "title": "No workflow runs available for recommendation",
                "description": "Recommendation evidence requires workflow runs.",
                "current_metric_json": {"total_runs": 0},
                "suggested_action_json": {
                    "action": "run_simulated_workflows",
                },
                "confidence_score": Decimal("1.0000"),
            }
        )
        return specs

    if missing_costs > 0:
        specs.append(
            {
                "recommendation_type": RecommendationType.MISSING_COSTS.value,
                "severity": RecommendationSeverity.MEDIUM.value,
                "title": "Some workflow runs are missing cost calculations",
                "description": "Unit economics are incomplete until run costs exist.",
                "current_metric_json": {
                    "total_runs": total_runs,
                    "missing_cost_runs": missing_costs,
                },
                "suggested_action_json": {
                    "action": "calculate_missing_run_costs",
                },
                "confidence_score": Decimal("0.9500"),
            }
        )

    if missing_outcomes > 0:
        specs.append(
            {
                "recommendation_type": RecommendationType.MISSING_OUTCOMES.value,
                "severity": RecommendationSeverity.MEDIUM.value,
                "title": "Some workflow runs are missing outcome verification",
                "description": "Business success cannot be measured for these runs.",
                "current_metric_json": {
                    "total_runs": total_runs,
                    "missing_outcome_runs": missing_outcomes,
                },
                "suggested_action_json": {
                    "action": "record_run_outcomes",
                    "statuses": ["succeeded", "failed"],
                },
                "confidence_score": Decimal("0.9500"),
            }
        )

    failure_rate = Decimal("0")
    if total_outcomes > 0:
        failure_rate = (
            Decimal(failed_outcomes) / Decimal(total_outcomes)
        ).quantize(RATE_QUANTUM, rounding=ROUND_HALF_UP)
    if total_runs >= 3 and failure_rate >= Decimal("0.4"):
        specs.append(
            {
                "recommendation_type": RecommendationType.HIGH_FAILURE_RATE.value,
                "severity": RecommendationSeverity.HIGH.value,
                "title": "Workflow has high failure rate",
                "description": "Final unsuccessful outcomes exceed the MVP threshold.",
                "current_metric_json": {
                    "failed_outcomes": failed_outcomes,
                    "total_outcomes": total_outcomes,
                    "failure_rate": str(failure_rate),
                },
                "suggested_action_json": {
                    "action": "review_workflow_failures",
                    "areas": [
                        "workflow_configuration",
                        "prompt_strategy",
                        "tool_reliability",
                    ],
                },
                "confidence_score": Decimal("0.8500"),
            }
        )

    if (
        total_cost_usd > Decimal("0")
        and successful_outcomes == 0
        and total_runs >= 2
    ):
        specs.append(
            {
                "recommendation_type": (
                    RecommendationType.HIGH_COST_LOW_SUCCESS.value
                ),
                "severity": RecommendationSeverity.HIGH.value,
                "title": "Cost is increasing without successful outcomes",
                "description": "Recorded spend has produced no verified success.",
                "current_metric_json": {
                    "total_runs": total_runs,
                    "successful_outcomes": 0,
                    "total_cost_usd": str(total_cost_usd),
                },
                "suggested_action_json": {
                    "action": "investigate_cost_without_success",
                    "review": ["model_calls", "tool_calls", "failure_reasons"],
                },
                "confidence_score": Decimal("0.8500"),
            }
        )

    if (
        successful_outcomes > 0
        and cost_per_successful_outcome_usd is not None
    ):
        specs.append(
            {
                "recommendation_type": (
                    RecommendationType.COST_PER_SUCCESS_OPPORTUNITY.value
                ),
                "severity": RecommendationSeverity.LOW.value,
                "title": "Track cost per successful outcome for optimization",
                "description": "Use outcome-aware unit economics before scaling.",
                "current_metric_json": {
                    "successful_outcomes": successful_outcomes,
                    "cost_per_successful_outcome_usd": str(
                        cost_per_successful_outcome_usd
                    ),
                },
                "suggested_action_json": {
                    "action": "compare_before_scaling",
                    "compare_by": ["workflow", "configuration"],
                },
                "confidence_score": Decimal("0.7500"),
            }
        )

    return specs


def generate_project_recommendations(
    db: Session,
    project_id: uuid.UUID,
    workflow_id: uuid.UUID | None = None,
) -> RecommendationGenerateResponse:
    if get_project_by_id(db, project_id) is None:
        raise LookupError("Project not found.")
    if workflow_id is not None:
        workflow = get_workflow_by_id(db, workflow_id)
        if workflow is None:
            raise LookupError("Workflow not found.")
        if workflow.project_id != project_id:
            raise ValueError("Workflow does not belong to the selected project.")

    runs = _list_runs(db, project_id, workflow_id)
    missing_costs = 0
    missing_outcomes = 0
    total_cost = Decimal("0")
    outcomes = []
    for run in runs:
        cost = get_cost_by_workflow_run_id(db, run.id)
        if cost is None:
            missing_costs += 1
        else:
            total_cost += Decimal(str(cost.total_cost_usd))
        outcome = get_outcome_by_workflow_run_id(db, run.id)
        if outcome is None:
            missing_outcomes += 1
        else:
            outcomes.append(outcome)

    successful_outcomes = sum(
        outcome.status == WorkflowOutcomeStatus.SUCCEEDED.value
        for outcome in outcomes
    )
    failed_outcomes = sum(
        outcome.status in FAILED_OUTCOME_STATUSES
        for outcome in outcomes
    )
    total_cost = total_cost.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)
    cost_per_success = None
    if successful_outcomes > 0:
        cost_per_success = (
            total_cost / Decimal(successful_outcomes)
        ).quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)

    specs = _build_recommendation_specs(
        total_runs=len(runs),
        missing_costs=missing_costs,
        missing_outcomes=missing_outcomes,
        total_outcomes=len(outcomes),
        successful_outcomes=successful_outcomes,
        failed_outcomes=failed_outcomes,
        total_cost_usd=total_cost,
        cost_per_successful_outcome_usd=cost_per_success,
    )

    delete_open_recommendations_for_project(db, project_id, workflow_id)
    recommendations = [
        create_recommendation(
            db,
            project_id=project_id,
            workflow_id=workflow_id,
            **spec,
        )
        for spec in specs
    ]
    return RecommendationGenerateResponse(
        project_id=project_id,
        workflow_id=workflow_id,
        generated_count=len(recommendations),
        recommendations=recommendations,
    )


def list_project_recommendations(
    db: Session,
    project_id: uuid.UUID,
    workflow_id: uuid.UUID | None = None,
    status: str | None = None,
    recommendation_type: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Recommendation]:
    return list_recommendations(
        db,
        project_id=project_id,
        workflow_id=workflow_id,
        status=status,
        recommendation_type=recommendation_type,
        limit=limit,
        offset=offset,
    )


def update_recommendation_status(
    db: Session,
    recommendation_id: uuid.UUID,
    status: RecommendationStatus | str,
    accepted_at: datetime | None = None,
    dismissed_at: datetime | None = None,
) -> Recommendation:
    recommendation = get_recommendation_by_id(db, recommendation_id)
    if recommendation is None:
        raise LookupError("Recommendation not found.")

    status_value = (
        status.value if isinstance(status, RecommendationStatus) else status
    )
    fields: dict[str, object] = {"status": status_value}
    now = datetime.now(timezone.utc)
    if status_value == RecommendationStatus.ACCEPTED.value:
        fields["accepted_at"] = accepted_at or recommendation.accepted_at or now
    elif accepted_at is not None:
        fields["accepted_at"] = accepted_at
    if status_value == RecommendationStatus.DISMISSED.value:
        fields["dismissed_at"] = dismissed_at or recommendation.dismissed_at or now
    elif dismissed_at is not None:
        fields["dismissed_at"] = dismissed_at
    return update_recommendation(db, recommendation, **fields)
