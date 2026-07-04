"""Protected Outcome Contract, run-outcome and unit-economics endpoints."""

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.enums import OutcomeContractStatus
from app.models.outcome_contract import OutcomeContract
from app.models.project_member import ProjectMember
from app.models.user import User
from app.models.workflow_configuration import WorkflowConfiguration
from app.models.workflow_run_outcome import WorkflowRunOutcome
from app.repositories.outcome_contract_repository import (
    get_outcome_contract_by_id,
    list_outcome_contracts_for_user,
    update_outcome_contract,
)
from app.repositories.project_member_repository import (
    get_project_member,
    list_user_project_memberships,
)
from app.repositories.project_repository import get_project_by_id
from app.repositories.workflow_configuration_repository import (
    get_configuration_by_id,
)
from app.repositories.workflow_repository import get_workflow_by_id
from app.repositories.workflow_run_repository import get_workflow_run_by_id
from app.schemas.outcome_contract import (
    OutcomeContractCreate,
    OutcomeContractRead,
    OutcomeContractUpdate,
)
from app.schemas.outcome_metrics import CostPerSuccessfulOutcomeRead
from app.schemas.workflow_run_outcome import (
    WorkflowRunOutcomeCreate,
    WorkflowRunOutcomeRead,
)
from app.services.outcome_service import (
    calculate_cost_per_successful_outcome,
    create_contract,
    get_workflow_run_outcome,
    record_workflow_run_outcome,
)


router = APIRouter()


def _require_project_access(
    db: Session,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
) -> ProjectMember:
    if get_project_by_id(db, project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found.")
    membership = get_project_member(db, project_id, user_id)
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project membership is required.",
        )
    return membership


def _get_visible_contract(
    db: Session,
    contract_id: uuid.UUID,
    user_id: uuid.UUID,
) -> OutcomeContract:
    contract = get_outcome_contract_by_id(db, contract_id)
    if contract is None:
        raise HTTPException(status_code=404, detail="Outcome Contract not found.")
    _require_project_access(db, contract.project_id, user_id)
    return contract


def _require_run_access(
    db: Session,
    workflow_run_id: uuid.UUID,
    user_id: uuid.UUID,
) -> None:
    workflow_run = get_workflow_run_by_id(db, workflow_run_id)
    if workflow_run is None:
        raise HTTPException(status_code=404, detail="Workflow run not found.")
    _require_project_access(db, workflow_run.project_id, user_id)


@router.post(
    "/contracts",
    response_model=OutcomeContractRead,
    status_code=status.HTTP_201_CREATED,
)
def create_outcome_contract_endpoint(
    request: OutcomeContractCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> OutcomeContract:
    _require_project_access(db, request.project_id, current_user.id)
    try:
        return create_contract(db, current_user.id, request)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (IntegrityError, ValueError) as exc:
        db.rollback()
        detail = (
            str(exc)
            if isinstance(exc, ValueError)
            else "Outcome Contract could not be created."
        )
        raise HTTPException(status_code=400, detail=detail) from exc


@router.get("/contracts", response_model=list[OutcomeContractRead])
def list_outcome_contracts_endpoint(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    project_id: uuid.UUID | None = None,
    workflow_id: uuid.UUID | None = None,
    contract_status: Annotated[
        OutcomeContractStatus | None,
        Query(alias="status"),
    ] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[OutcomeContract]:
    if project_id is not None:
        _require_project_access(db, project_id, current_user.id)
    return list_outcome_contracts_for_user(
        db,
        user_id=current_user.id,
        project_id=project_id,
        workflow_id=workflow_id,
        status=contract_status.value if contract_status is not None else None,
        limit=limit,
        offset=offset,
    )


@router.get("/contracts/{contract_id}", response_model=OutcomeContractRead)
def get_outcome_contract_endpoint(
    contract_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> OutcomeContract:
    return _get_visible_contract(db, contract_id, current_user.id)


@router.patch("/contracts/{contract_id}", response_model=OutcomeContractRead)
def update_outcome_contract_endpoint(
    contract_id: uuid.UUID,
    request: OutcomeContractUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> OutcomeContract:
    contract = _get_visible_contract(db, contract_id, current_user.id)
    fields = request.model_dump(exclude_unset=True, mode="json")
    fields = {
        name: value
        for name, value in fields.items()
        if not (
            name in {"name", "success_window_hours", "status"}
            and value is None
        )
    }
    if not fields:
        return contract
    try:
        return update_outcome_contract(db, contract, **fields)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Outcome Contract name is already in use for this project.",
        ) from exc


@router.post(
    "/workflow-runs/{workflow_run_id}",
    response_model=WorkflowRunOutcomeRead,
)
def record_workflow_run_outcome_endpoint(
    workflow_run_id: uuid.UUID,
    request: WorkflowRunOutcomeCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> WorkflowRunOutcome:
    _require_run_access(db, workflow_run_id, current_user.id)
    try:
        return record_workflow_run_outcome(db, workflow_run_id, request)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (IntegrityError, ValueError) as exc:
        db.rollback()
        detail = (
            str(exc)
            if isinstance(exc, ValueError)
            else "Workflow run outcome could not be recorded."
        )
        raise HTTPException(status_code=400, detail=detail) from exc


@router.get(
    "/workflow-runs/{workflow_run_id}",
    response_model=WorkflowRunOutcomeRead,
)
def get_workflow_run_outcome_endpoint(
    workflow_run_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> WorkflowRunOutcome:
    _require_run_access(db, workflow_run_id, current_user.id)
    outcome = get_workflow_run_outcome(db, workflow_run_id)
    if outcome is None:
        raise HTTPException(status_code=404, detail="Workflow outcome not found.")
    return outcome


@router.get(
    "/metrics/cost-per-success",
    response_model=CostPerSuccessfulOutcomeRead,
)
def get_cost_per_successful_outcome_endpoint(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    project_id: uuid.UUID | None = None,
    workflow_id: uuid.UUID | None = None,
    configuration_id: uuid.UUID | None = None,
) -> CostPerSuccessfulOutcomeRead:
    memberships = list_user_project_memberships(db, current_user.id)
    allowed_project_ids = {membership.project_id for membership in memberships}

    if project_id is not None:
        _require_project_access(db, project_id, current_user.id)
    if workflow_id is not None:
        workflow = get_workflow_by_id(db, workflow_id)
        if workflow is None:
            raise HTTPException(status_code=404, detail="Workflow not found.")
        _require_project_access(db, workflow.project_id, current_user.id)
        if project_id is not None and workflow.project_id != project_id:
            raise HTTPException(
                status_code=400,
                detail="Workflow does not belong to the selected project.",
            )
    if configuration_id is not None:
        configuration: WorkflowConfiguration | None = get_configuration_by_id(
            db,
            configuration_id,
        )
        if configuration is None:
            raise HTTPException(
                status_code=404,
                detail="Workflow configuration not found.",
            )
        configuration_workflow = get_workflow_by_id(db, configuration.workflow_id)
        if configuration_workflow is None:
            raise HTTPException(status_code=404, detail="Workflow not found.")
        _require_project_access(
            db,
            configuration_workflow.project_id,
            current_user.id,
        )
        if workflow_id is not None and configuration.workflow_id != workflow_id:
            raise HTTPException(
                status_code=400,
                detail="Configuration does not belong to the selected workflow.",
            )
        if (
            project_id is not None
            and configuration_workflow.project_id != project_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Configuration does not belong to the selected project.",
            )

    return calculate_cost_per_successful_outcome(
        db,
        project_id=project_id,
        workflow_id=workflow_id,
        configuration_id=configuration_id,
        allowed_project_ids=allowed_project_ids,
    )
