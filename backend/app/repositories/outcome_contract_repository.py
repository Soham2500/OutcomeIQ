"""Database access functions for Outcome Contracts."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.outcome_contract import OutcomeContract
from app.models.project_member import ProjectMember


UPDATABLE_FIELDS = {
    "name",
    "description",
    "success_criteria_json",
    "success_window_hours",
    "status",
}


def create_outcome_contract(
    db: Session,
    project_id: uuid.UUID,
    name: str,
    workflow_id: uuid.UUID | None = None,
    description: str | None = None,
    success_criteria_json: dict[str, object] | None = None,
    success_window_hours: int = 48,
    created_by_user_id: uuid.UUID | None = None,
) -> OutcomeContract:
    contract = OutcomeContract(
        project_id=project_id,
        workflow_id=workflow_id,
        name=name,
        description=description,
        success_criteria_json=success_criteria_json,
        success_window_hours=success_window_hours,
        created_by_user_id=created_by_user_id,
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


def get_outcome_contract_by_id(
    db: Session,
    outcome_contract_id: uuid.UUID,
) -> OutcomeContract | None:
    return db.get(OutcomeContract, outcome_contract_id)


def get_outcome_contract_by_name(
    db: Session,
    project_id: uuid.UUID,
    name: str,
) -> OutcomeContract | None:
    return db.scalar(
        select(OutcomeContract).where(
            OutcomeContract.project_id == project_id,
            OutcomeContract.name == name,
        )
    )


def list_outcome_contracts(
    db: Session,
    project_id: uuid.UUID | None = None,
    workflow_id: uuid.UUID | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[OutcomeContract]:
    statement = select(OutcomeContract)
    if project_id is not None:
        statement = statement.where(OutcomeContract.project_id == project_id)
    if workflow_id is not None:
        statement = statement.where(OutcomeContract.workflow_id == workflow_id)
    if status is not None:
        statement = statement.where(OutcomeContract.status == status)
    statement = (
        statement.order_by(OutcomeContract.created_at, OutcomeContract.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def list_outcome_contracts_for_user(
    db: Session,
    user_id: uuid.UUID,
    project_id: uuid.UUID | None = None,
    workflow_id: uuid.UUID | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[OutcomeContract]:
    """List only contracts from projects visible to a user."""

    statement = (
        select(OutcomeContract)
        .join(
            ProjectMember,
            ProjectMember.project_id == OutcomeContract.project_id,
        )
        .where(ProjectMember.user_id == user_id)
    )
    if project_id is not None:
        statement = statement.where(OutcomeContract.project_id == project_id)
    if workflow_id is not None:
        statement = statement.where(OutcomeContract.workflow_id == workflow_id)
    if status is not None:
        statement = statement.where(OutcomeContract.status == status)
    statement = (
        statement.order_by(OutcomeContract.created_at, OutcomeContract.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def update_outcome_contract(
    db: Session,
    outcome_contract: OutcomeContract,
    **fields: object,
) -> OutcomeContract:
    if set(fields) - UPDATABLE_FIELDS:
        raise ValueError("Unsupported Outcome Contract update field.")
    for field_name, value in fields.items():
        setattr(outcome_contract, field_name, value)
    db.add(outcome_contract)
    db.commit()
    db.refresh(outcome_contract)
    return outcome_contract
