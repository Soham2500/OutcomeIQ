"""Application service for outcome tracking and unit economics."""

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import WorkflowOutcomeStatus
from app.models.outcome_contract import OutcomeContract
from app.models.workflow_run import WorkflowRun
from app.models.workflow_run_outcome import WorkflowRunOutcome
from app.repositories.outcome_contract_repository import (
    create_outcome_contract,
    get_outcome_contract_by_id,
    get_outcome_contract_by_name,
)
from app.repositories.project_repository import get_project_by_id
from app.repositories.workflow_repository import get_workflow_by_id
from app.repositories.workflow_run_cost_repository import (
    get_cost_by_workflow_run_id,
)
from app.repositories.workflow_run_outcome_repository import (
    create_or_update_workflow_run_outcome,
    get_outcome_by_workflow_run_id,
)
from app.repositories.workflow_run_repository import get_workflow_run_by_id
from app.schemas.outcome_contract import OutcomeContractCreate
from app.schemas.outcome_metrics import CostPerSuccessfulOutcomeRead
from app.schemas.workflow_run_outcome import WorkflowRunOutcomeCreate


MONEY_QUANTUM = Decimal("0.00000001")
RATE_QUANTUM = Decimal("0.00000001")
FAILED_OUTCOME_STATUSES = {
    WorkflowOutcomeStatus.FAILED.value,
    WorkflowOutcomeStatus.ESCALATED.value,
    WorkflowOutcomeStatus.REOPENED.value,
    WorkflowOutcomeStatus.ABANDONED.value,
    WorkflowOutcomeStatus.REVERSED.value,
}


def create_contract(
    db: Session,
    user_id: uuid.UUID,
    data: OutcomeContractCreate,
) -> OutcomeContract:
    if get_project_by_id(db, data.project_id) is None:
        raise LookupError("Project not found.")
    if data.workflow_id is not None:
        workflow = get_workflow_by_id(db, data.workflow_id)
        if workflow is None:
            raise LookupError("Workflow not found.")
        if workflow.project_id != data.project_id:
            raise ValueError("Workflow does not belong to the selected project.")
    if get_outcome_contract_by_name(db, data.project_id, data.name) is not None:
        raise ValueError("Outcome Contract name is already in use for this project.")

    return create_outcome_contract(
        db,
        created_by_user_id=user_id,
        **data.model_dump(mode="python"),
    )


def record_workflow_run_outcome(
    db: Session,
    workflow_run_id: uuid.UUID,
    data: WorkflowRunOutcomeCreate,
) -> WorkflowRunOutcome:
    workflow_run = get_workflow_run_by_id(db, workflow_run_id)
    if workflow_run is None:
        raise LookupError("Workflow run not found.")

    if data.outcome_contract_id is not None:
        contract = get_outcome_contract_by_id(db, data.outcome_contract_id)
        if contract is None:
            raise LookupError("Outcome Contract not found.")
        if contract.project_id != workflow_run.project_id:
            raise ValueError(
                "Outcome Contract does not belong to the workflow run project."
            )
        if (
            contract.workflow_id is not None
            and contract.workflow_id != workflow_run.workflow_id
        ):
            raise ValueError(
                "Outcome Contract does not apply to the workflow run workflow."
            )

    verified_at = data.verified_at
    if (
        verified_at is None
        and data.status != WorkflowOutcomeStatus.PENDING
    ):
        verified_at = datetime.now(timezone.utc)

    return create_or_update_workflow_run_outcome(
        db,
        workflow_run_id=workflow_run_id,
        outcome_contract_id=data.outcome_contract_id,
        status=data.status.value,
        verification_source=data.verification_source.value,
        outcome_score=data.outcome_score,
        business_value_usd=data.business_value_usd,
        verified_at=verified_at,
        notes=data.notes,
        metadata_json=data.metadata_json,
    )


def get_workflow_run_outcome(
    db: Session,
    workflow_run_id: uuid.UUID,
) -> WorkflowRunOutcome | None:
    return get_outcome_by_workflow_run_id(db, workflow_run_id)


def calculate_cost_per_successful_outcome(
    db: Session,
    project_id: uuid.UUID | None = None,
    workflow_id: uuid.UUID | None = None,
    configuration_id: uuid.UUID | None = None,
    allowed_project_ids: set[uuid.UUID] | None = None,
) -> CostPerSuccessfulOutcomeRead:
    statement = select(WorkflowRun)
    if allowed_project_ids is not None:
        statement = statement.where(
            WorkflowRun.project_id.in_(allowed_project_ids)
        )
    if project_id is not None:
        statement = statement.where(WorkflowRun.project_id == project_id)
    if workflow_id is not None:
        statement = statement.where(WorkflowRun.workflow_id == workflow_id)
    if configuration_id is not None:
        statement = statement.where(
            WorkflowRun.configuration_id == configuration_id
        )
    workflow_runs = list(db.scalars(statement.order_by(WorkflowRun.id)))

    successful_runs = 0
    failed_runs = 0
    pending_runs = 0
    missing_cost_summaries = 0
    total_cost = Decimal("0")

    for workflow_run in workflow_runs:
        cost = get_cost_by_workflow_run_id(db, workflow_run.id)
        if cost is None:
            missing_cost_summaries += 1
        else:
            total_cost += Decimal(str(cost.total_cost_usd))

        outcome = get_outcome_by_workflow_run_id(db, workflow_run.id)
        if outcome is None or outcome.status == WorkflowOutcomeStatus.PENDING.value:
            pending_runs += 1
        elif outcome.status == WorkflowOutcomeStatus.SUCCEEDED.value:
            successful_runs += 1
        elif outcome.status in FAILED_OUTCOME_STATUSES:
            failed_runs += 1

    total_runs = len(workflow_runs)
    total_cost = total_cost.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)
    cost_per_success = None
    if successful_runs > 0:
        cost_per_success = (total_cost / Decimal(successful_runs)).quantize(
            MONEY_QUANTUM,
            rounding=ROUND_HALF_UP,
        )
    success_rate = Decimal("0")
    if total_runs > 0:
        success_rate = (
            Decimal(successful_runs) / Decimal(total_runs)
        ).quantize(RATE_QUANTUM, rounding=ROUND_HALF_UP)

    notes: list[str] = []
    if total_runs == 0:
        notes.append("No workflow runs matched the selected filters.")
    if missing_cost_summaries:
        notes.append(
            f"{missing_cost_summaries} workflow run(s) have no cost summary."
        )

    return CostPerSuccessfulOutcomeRead(
        project_id=project_id,
        workflow_id=workflow_id,
        configuration_id=configuration_id,
        total_runs=total_runs,
        successful_runs=successful_runs,
        failed_runs=failed_runs,
        pending_runs=pending_runs,
        total_cost_usd=total_cost,
        cost_per_successful_outcome_usd=cost_per_success,
        success_rate=success_rate,
        notes=" ".join(notes) if notes else None,
    )
