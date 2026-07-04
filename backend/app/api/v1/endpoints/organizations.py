"""Authenticated organization CRUD endpoints with simple MVP access."""

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.enums import AuditAction
from app.models.organization import Organization
from app.models.user import User
from app.repositories.organization_repository import (
    create_organization,
    get_organization_by_id,
    get_organization_by_slug,
    list_organizations as list_organization_records,
    update_organization,
)
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationRead,
    OrganizationUpdate,
)
from app.services.audit_service import record_audit_event


router = APIRouter()


@router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
def create_organization_endpoint(
    request: OrganizationCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Organization:
    if get_organization_by_slug(db, request.slug) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization slug is already in use.",
        )

    try:
        organization = create_organization(db, request.name, request.slug)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization slug is already in use.",
        ) from exc

    record_audit_event(
        db,
        action=AuditAction.CREATE.value,
        message="Organization created",
        actor_user_id=current_user.id,
        organization_id=organization.id,
        entity_type="organization",
        entity_id=str(organization.id),
    )
    return organization


@router.get("", response_model=list[OrganizationRead])
def list_organizations_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_active_user)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Organization]:
    return list_organization_records(db, limit=limit, offset=offset)


@router.get("/{organization_id}", response_model=OrganizationRead)
def get_organization_endpoint(
    organization_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_active_user)],
) -> Organization:
    organization = get_organization_by_id(db, organization_id)
    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )
    return organization


@router.patch("/{organization_id}", response_model=OrganizationRead)
def update_organization_endpoint(
    organization_id: uuid.UUID,
    request: OrganizationUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Organization:
    organization = get_organization_by_id(db, organization_id)
    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )

    fields = request.model_dump(
        exclude_unset=True,
        exclude_none=True,
        mode="json",
    )
    if not fields:
        return organization

    organization = update_organization(db, organization, **fields)
    record_audit_event(
        db,
        action=AuditAction.UPDATE.value,
        message="Organization updated",
        actor_user_id=current_user.id,
        organization_id=organization.id,
        entity_type="organization",
        entity_id=str(organization.id),
        metadata_json={"updated_fields": sorted(fields)},
    )
    return organization
