"""Database access functions for workflow-run outcomes."""

from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workflow_run_outcome import WorkflowRunOutcome


def get_outcome_by_workflow_run_id(
    db: Session,
    workflow_run_id: uuid.UUID,
) -> WorkflowRunOutcome | None:
    return db.scalar(
        select(WorkflowRunOutcome).where(
            WorkflowRunOutcome.workflow_run_id == workflow_run_id
        )
    )


def create_or_update_workflow_run_outcome(
    db: Session,
    workflow_run_id: uuid.UUID,
    outcome_contract_id: uuid.UUID | None = None,
    status: str = "pending",
    verification_source: str = "manual",
    outcome_score: Decimal | None = None,
    business_value_usd: Decimal | None = None,
    verified_at: datetime | None = None,
    notes: str | None = None,
    metadata_json: dict[str, object] | None = None,
) -> WorkflowRunOutcome:
    outcome = get_outcome_by_workflow_run_id(db, workflow_run_id)
    if outcome is None:
        outcome = WorkflowRunOutcome(workflow_run_id=workflow_run_id)

    outcome.outcome_contract_id = outcome_contract_id
    outcome.status = status
    outcome.verification_source = verification_source
    outcome.outcome_score = outcome_score
    outcome.business_value_usd = business_value_usd
    outcome.verified_at = verified_at
    outcome.notes = notes
    outcome.metadata_json = metadata_json

    db.add(outcome)
    db.commit()
    db.refresh(outcome)
    return outcome


def list_outcomes(
    db: Session,
    status: str | None = None,
    outcome_contract_id: uuid.UUID | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[WorkflowRunOutcome]:
    statement = select(WorkflowRunOutcome)
    if status is not None:
        statement = statement.where(WorkflowRunOutcome.status == status)
    if outcome_contract_id is not None:
        statement = statement.where(
            WorkflowRunOutcome.outcome_contract_id == outcome_contract_id
        )
    statement = (
        statement.order_by(
            WorkflowRunOutcome.created_at,
            WorkflowRunOutcome.id,
        )
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))
