"""Database access functions for organizations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.organization import Organization


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
