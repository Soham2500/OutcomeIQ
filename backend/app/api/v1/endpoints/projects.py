"""Authenticated project CRUD endpoints with simple MVP access."""

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_active_user,
    require_project_member,
    require_project_owner_or_admin,
)
from app.db.session import get_db
from app.models.enums import AuditAction, ProjectMemberRole
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.user import User
from app.repositories.organization_repository import get_organization_by_id
from app.repositories.project_member_repository import (
    add_project_member,
    list_project_members as list_project_member_records,
)
from app.repositories.project_repository import (
    create_project,
    get_project_by_id,
    get_project_by_slug,
    list_projects_for_user,
    update_project,
)
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.schemas.project_member import ProjectMemberRead
from app.services.audit_service import record_audit_event
from app.services.usage_limit_service import (
    LIMIT_MESSAGE,
    check_project_creation_limit,
)


router = APIRouter()


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project_endpoint(
    request: ProjectCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Project:
    try:
        check_project_creation_limit(db, current_user.id)
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=LIMIT_MESSAGE,
        ) from exc

    organization = get_organization_by_id(db, request.organization_id)
    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )
    if get_project_by_slug(db, request.organization_id, request.slug) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project slug is already in use for this organization.",
        )

    try:
        project = create_project(
            db,
            organization_id=request.organization_id,
            name=request.name,
            slug=request.slug,
            description=request.description,
        )
        add_project_member(
            db,
            project_id=project.id,
            user_id=current_user.id,
            role=ProjectMemberRole.OWNER.value,
        )
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project could not be created because a unique value is in use.",
        ) from exc

    record_audit_event(
        db,
        action=AuditAction.CREATE.value,
        message="Project created",
        actor_user_id=current_user.id,
        organization_id=project.organization_id,
        project_id=project.id,
        entity_type="project",
        entity_id=str(project.id),
    )
    return project


@router.get("", response_model=list[ProjectRead])
def list_projects_endpoint(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    organization_id: uuid.UUID | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Project]:
    return list_projects_for_user(
        db,
        user_id=current_user.id,
        organization_id=organization_id,
        limit=limit,
        offset=offset,
    )


@router.get("/{project_id}", response_model=ProjectRead)
def get_project_endpoint(
    project_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    _membership: Annotated[ProjectMember, Depends(require_project_member)],
) -> Project:
    project = get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project_endpoint(
    project_id: uuid.UUID,
    request: ProjectUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    _membership: Annotated[
        ProjectMember,
        Depends(require_project_owner_or_admin),
    ],
) -> Project:
    project = get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    fields = request.model_dump(exclude_unset=True, mode="json")
    fields = {
        field_name: value
        for field_name, value in fields.items()
        if not (field_name in {"name", "status"} and value is None)
    }
    if not fields:
        return project

    project = update_project(db, project, **fields)
    record_audit_event(
        db,
        action=AuditAction.UPDATE.value,
        message="Project updated",
        actor_user_id=current_user.id,
        organization_id=project.organization_id,
        project_id=project.id,
        entity_type="project",
        entity_id=str(project.id),
        metadata_json={"updated_fields": sorted(fields)},
    )
    return project


@router.get("/{project_id}/members", response_model=list[ProjectMemberRead])
def list_project_members_endpoint(
    project_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    _membership: Annotated[ProjectMember, Depends(require_project_member)],
) -> list[ProjectMember]:
    if get_project_by_id(db, project_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )
    return list_project_member_records(db, project_id)
