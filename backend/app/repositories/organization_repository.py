"""Database access functions for organizations."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.organization import Organization


UPDATABLE_FIELDS = {"name", "status"}


def get_organization_by_id(
    db: Session,
    organization_id: uuid.UUID,
) -> Organization | None:
    return db.get(Organization, organization_id)


def get_organization_by_slug(db: Session, slug: str) -> Organization | None:
    return db.scalar(select(Organization).where(Organization.slug == slug))


def create_organization(db: Session, name: str, slug: str) -> Organization:
    organization = Organization(name=name, slug=slug)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization


def list_organizations(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[Organization]:
    statement = (
        select(Organization)
        .order_by(Organization.created_at, Organization.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def update_organization(
    db: Session,
    organization: Organization,
    **fields: object,
) -> Organization:
    unknown_fields = set(fields) - UPDATABLE_FIELDS
    if unknown_fields:
        raise ValueError("Unsupported organization update field.")

    for field_name, value in fields.items():
        setattr(organization, field_name, value)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization
