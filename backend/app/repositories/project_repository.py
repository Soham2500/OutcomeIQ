"""Database access functions for projects."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


UPDATABLE_FIELDS = {"name", "description", "status"}


def get_project_by_id(db: Session, project_id: uuid.UUID) -> Project | None:
    return db.get(Project, project_id)


def get_project_by_slug(
    db: Session,
    organization_id: uuid.UUID,
    slug: str,
) -> Project | None:
    return db.scalar(
        select(Project).where(
            Project.organization_id == organization_id,
            Project.slug == slug,
        )
    )


def create_project(
    db: Session,
    organization_id: uuid.UUID,
    name: str,
    slug: str,
    description: str | None = None,
) -> Project:
    project = Project(
        organization_id=organization_id,
        name=name,
        slug=slug,
        description=description,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def list_projects(
    db: Session,
    organization_id: uuid.UUID | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Project]:
    statement = select(Project)
    if organization_id is not None:
        statement = statement.where(Project.organization_id == organization_id)
    statement = (
        statement.order_by(Project.created_at, Project.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def update_project(
    db: Session,
    project: Project,
    **fields: object,
) -> Project:
    unknown_fields = set(fields) - UPDATABLE_FIELDS
    if unknown_fields:
        raise ValueError("Unsupported project update field.")

    for field_name, value in fields.items():
        setattr(project, field_name, value)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
