"""Protected workflow-run telemetry and trace endpoints."""

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.enums import WorkflowRunStatus
from app.models.model_call import ModelCall
from app.models.tool_call import ToolCall
from app.models.user import User
from app.models.workflow_run import WorkflowRun
from app.repositories.project_member_repository import get_project_member
from app.repositories.project_repository import get_project_by_id
from app.repositories.workflow_run_repository import (
    get_workflow_run_by_id,
    list_workflow_runs_for_user,
)
from app.schemas.model_call import ModelCallCreate, ModelCallRead
from app.schemas.tool_call import ToolCallCreate, ToolCallRead
from app.schemas.workflow_run import (
    WorkflowRunCompleteRequest,
    WorkflowRunCreate,
    WorkflowRunFailRequest,
    WorkflowRunRead,
    WorkflowRunTraceRead,
)
from app.services.workflow_logging_service import (
    complete_run,
    fail_run,
    get_workflow_run_trace,
    record_model_call,
    record_tool_call,
    start_workflow_run,
)
from app.services.usage_limit_service import (
    LIMIT_MESSAGE,
    check_workflow_run_monthly_limit,
    increment_workflow_run_usage,
)


router = APIRouter()


def _require_project_access(
    db: Session,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
) -> None:
    if get_project_by_id(db, project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found.")
    if get_project_member(db, project_id, user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project membership is required.",
        )


def _get_visible_run(
    db: Session,
    workflow_run_id: uuid.UUID,
    user_id: uuid.UUID,
) -> WorkflowRun:
    workflow_run = get_workflow_run_by_id(db, workflow_run_id)
    if workflow_run is None:
        raise HTTPException(status_code=404, detail="Workflow run not found.")
    _require_project_access(db, workflow_run.project_id, user_id)
    return workflow_run


def _raise_service_error(exc: Exception) -> None:
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, IntegrityError):
        raise HTTPException(status_code=400, detail="Telemetry could not be recorded.") from exc
    raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("", response_model=WorkflowRunRead, status_code=status.HTTP_201_CREATED)
def start_workflow_run_endpoint(
    request: WorkflowRunCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> WorkflowRun:
    _require_project_access(db, request.project_id, current_user.id)
    try:
        check_workflow_run_monthly_limit(db, current_user.id)
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=LIMIT_MESSAGE,
        ) from exc
    try:
        workflow_run = start_workflow_run(
            db,
            project_id=request.project_id,
            workflow_id=request.workflow_id,
            user_id=current_user.id,
            data=request,
        )
        increment_workflow_run_usage(db, current_user.id)
        return workflow_run
    except (IntegrityError, LookupError, ValueError) as exc:
        db.rollback()
        _raise_service_error(exc)


@router.get("", response_model=list[WorkflowRunRead])
def list_workflow_runs_endpoint(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    project_id: uuid.UUID | None = None,
    workflow_id: uuid.UUID | None = None,
    run_status: Annotated[WorkflowRunStatus | None, Query(alias="status")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[WorkflowRun]:
    if project_id is not None:
        _require_project_access(db, project_id, current_user.id)
    return list_workflow_runs_for_user(
        db,
        user_id=current_user.id,
        project_id=project_id,
        workflow_id=workflow_id,
        status=run_status.value if run_status is not None else None,
        limit=limit,
        offset=offset,
    )


@router.get("/{workflow_run_id}", response_model=WorkflowRunRead)
def get_workflow_run_endpoint(
    workflow_run_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> WorkflowRun:
    return _get_visible_run(db, workflow_run_id, current_user.id)


@router.post(
    "/{workflow_run_id}/model-calls",
    response_model=ModelCallRead,
    status_code=status.HTTP_201_CREATED,
)
def record_model_call_endpoint(
    workflow_run_id: uuid.UUID,
    request: ModelCallCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> ModelCall:
    _get_visible_run(db, workflow_run_id, current_user.id)
    try:
        return record_model_call(db, workflow_run_id, request)
    except (IntegrityError, LookupError, ValueError) as exc:
        db.rollback()
        _raise_service_error(exc)


@router.post(
    "/{workflow_run_id}/tool-calls",
    response_model=ToolCallRead,
    status_code=status.HTTP_201_CREATED,
)
def record_tool_call_endpoint(
    workflow_run_id: uuid.UUID,
    request: ToolCallCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> ToolCall:
    _get_visible_run(db, workflow_run_id, current_user.id)
    try:
        return record_tool_call(db, workflow_run_id, request)
    except (IntegrityError, LookupError, ValueError) as exc:
        db.rollback()
        _raise_service_error(exc)


@router.post("/{workflow_run_id}/complete", response_model=WorkflowRunRead)
def complete_workflow_run_endpoint(
    workflow_run_id: uuid.UUID,
    request: WorkflowRunCompleteRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> WorkflowRun:
    _get_visible_run(db, workflow_run_id, current_user.id)
    try:
        return complete_run(db, workflow_run_id, request)
    except (LookupError, ValueError) as exc:
        db.rollback()
        _raise_service_error(exc)


@router.post("/{workflow_run_id}/fail", response_model=WorkflowRunRead)
def fail_workflow_run_endpoint(
    workflow_run_id: uuid.UUID,
    request: WorkflowRunFailRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> WorkflowRun:
    _get_visible_run(db, workflow_run_id, current_user.id)
    try:
        return fail_run(db, workflow_run_id, request)
    except (LookupError, ValueError) as exc:
        db.rollback()
        _raise_service_error(exc)


@router.get("/{workflow_run_id}/trace", response_model=WorkflowRunTraceRead)
def get_workflow_run_trace_endpoint(
    workflow_run_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, object]:
    _get_visible_run(db, workflow_run_id, current_user.id)
    try:
        return get_workflow_run_trace(db, workflow_run_id)
    except LookupError as exc:
        _raise_service_error(exc)
