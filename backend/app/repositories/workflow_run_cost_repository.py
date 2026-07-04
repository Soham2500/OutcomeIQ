"""Database access functions for persisted workflow run costs."""

from datetime import datetime, timezone
from decimal import Decimal
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workflow_run_cost import WorkflowRunCost


def get_cost_by_workflow_run_id(
    db: Session,
    workflow_run_id: uuid.UUID,
) -> WorkflowRunCost | None:
    return db.scalar(
        select(WorkflowRunCost).where(
            WorkflowRunCost.workflow_run_id == workflow_run_id
        )
    )


def upsert_workflow_run_cost(
    db: Session,
    workflow_run_id: uuid.UUID,
    prompt_tokens: int,
    completion_tokens: int,
    total_tokens: int,
    model_call_count: int,
    tool_call_count: int,
    model_cost_usd: Decimal,
    tool_cost_usd: Decimal,
    total_cost_usd: Decimal,
    currency: str = "USD",
    calculation_status: str = "calculated",
    calculation_notes: str | None = None,
) -> WorkflowRunCost:
    cost = get_cost_by_workflow_run_id(db, workflow_run_id)
    if cost is None:
        cost = WorkflowRunCost(workflow_run_id=workflow_run_id)

    cost.prompt_tokens = prompt_tokens
    cost.completion_tokens = completion_tokens
    cost.total_tokens = total_tokens
    cost.model_call_count = model_call_count
    cost.tool_call_count = tool_call_count
    cost.model_cost_usd = model_cost_usd
    cost.tool_cost_usd = tool_cost_usd
    cost.total_cost_usd = total_cost_usd
    cost.currency = currency
    cost.calculation_status = calculation_status
    cost.calculation_notes = calculation_notes
    cost.calculated_at = datetime.now(timezone.utc)

    db.add(cost)
    db.commit()
    db.refresh(cost)
    return cost


def list_workflow_run_costs(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[WorkflowRunCost]:
    statement = (
        select(WorkflowRunCost)
        .order_by(WorkflowRunCost.calculated_at.desc(), WorkflowRunCost.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))
