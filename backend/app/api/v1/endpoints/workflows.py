"""Protected workflow and workflow-configuration endpoints."""

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.enums import AuditAction, ProjectMemberRole
from app.models.project_member import ProjectMember
from app.models.user import User
from app.models.workflow import Workflow
from app.models.workflow_configuration import WorkflowConfiguration
from app.repositories.project_member_repository import get_project_member
from app.repositories.project_repository import get_project_by_id
from app.repositories.workflow_configuration_repository import list_configurations
from app.repositories.workflow_repository import (
    get_workflow_by_id,
    list_workflows_for_user,
    update_workflow,
)
from app.schemas.workflow import WorkflowCreate, WorkflowRead, WorkflowUpdate
from app.schemas.workflow_configuration import (
    WorkflowConfigurationCreate,
    WorkflowConfigurationRead,
)
from app.services.workflow_logging_service import (
    create_configuration_for_workflow,
    create_workflow_for_project,
)
from app.services.audit_service import record_audit_event


router = APIRouter()
PRIVILEGED_ROLES = {
    ProjectMemberRole.OWNER.value,
    ProjectMemberRole.ADMIN.value,
}


def _require_membership(
    db: Session,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
) -> ProjectMember:
    if get_project_by_id(db, project_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )
    membership = get_project_member(db, project_id, user_id)
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project membership is required.",
        )
    return membership


def _require_owner_or_admin(membership: ProjectMember) -> None:
    if membership.role not in PRIVILEGED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project owner or admin access is required.",
        )


def _get_visible_workflow(
    db: Session,
    workflow_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Workflow:
    workflow = get_workflow_by_id(db, workflow_id)
    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found.",
        )
    _require_membership(db, workflow.project_id, user_id)
    return workflow


@router.post("", response_model=WorkflowRead, status_code=status.HTTP_201_CREATED)
def create_workflow_endpoint(
    request: WorkflowCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Workflow:
    membership = _require_membership(db, request.project_id, current_user.id)
    _require_owner_or_admin(membership)
    try:
        return create_workflow_for_project(
            db,
            project_id=request.project_id,
            user_id=current_user.id,
            data=request,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (IntegrityError, ValueError) as exc:
        db.rollback()
        detail = str(exc) if isinstance(exc, ValueError) else "Workflow could not be created."
        raise HTTPException(status_code=400, detail=detail) from exc


@router.get("", response_model=list[WorkflowRead])
def list_workflows_endpoint(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    project_id: uuid.UUID | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Workflow]:
    if project_id is not None:
        _require_membership(db, project_id, current_user.id)
    return list_workflows_for_user(
        db,
        user_id=current_user.id,
        project_id=project_id,
        limit=limit,
        offset=offset,
    )


@router.get("/{workflow_id}", response_model=WorkflowRead)
def get_workflow_endpoint(
    workflow_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Workflow:
    return _get_visible_workflow(db, workflow_id, current_user.id)


@router.patch("/{workflow_id}", response_model=WorkflowRead)
def update_workflow_endpoint(
    workflow_id: uuid.UUID,
    request: WorkflowUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Workflow:
    workflow = _get_visible_workflow(db, workflow_id, current_user.id)
    membership = _require_membership(db, workflow.project_id, current_user.id)
    _require_owner_or_admin(membership)
    fields = request.model_dump(exclude_unset=True, mode="json")
    fields = {
        name: value
        for name, value in fields.items()
        if not (name in {"name", "status"} and value is None)
    }
    if not fields:
        return workflow
    workflow = update_workflow(db, workflow, **fields)
    record_audit_event(
        db,
        action=AuditAction.UPDATE.value,
        message="Workflow updated",
        actor_user_id=current_user.id,
        project_id=workflow.project_id,
        entity_type="workflow",
        entity_id=str(workflow.id),
        metadata_json={"updated_fields": sorted(fields)},
    )
    return workflow


@router.post(
    "/{workflow_id}/configurations",
    response_model=WorkflowConfigurationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_workflow_configuration_endpoint(
    workflow_id: uuid.UUID,
    request: WorkflowConfigurationCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> WorkflowConfiguration:
    workflow = _get_visible_workflow(db, workflow_id, current_user.id)
    membership = _require_membership(db, workflow.project_id, current_user.id)
    _require_owner_or_admin(membership)
    try:
        return create_configuration_for_workflow(
            db,
            workflow_id=workflow_id,
            user_id=current_user.id,
            data=request,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (IntegrityError, ValueError) as exc:
        db.rollback()
        detail = (
            str(exc)
            if isinstance(exc, ValueError)
            else "Workflow configuration could not be created."
        )
        raise HTTPException(status_code=400, detail=detail) from exc


@router.get(
    "/{workflow_id}/configurations",
    response_model=list[WorkflowConfigurationRead],
)
def list_workflow_configurations_endpoint(
    workflow_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[WorkflowConfiguration]:
    _get_visible_workflow(db, workflow_id, current_user.id)
    return list_configurations(db, workflow_id, limit=limit, offset=offset)
