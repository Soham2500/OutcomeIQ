"""Database access functions for registered workflows."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project_member import ProjectMember
from app.models.workflow import Workflow


UPDATABLE_FIELDS = {"name", "description", "status"}


def create_workflow(
    db: Session,
    project_id: uuid.UUID,
    name: str,
    slug: str,
    description: str | None = None,
    created_by_user_id: uuid.UUID | None = None,
) -> Workflow:
    workflow = Workflow(
        project_id=project_id,
        name=name,
        slug=slug,
        description=description,
        created_by_user_id=created_by_user_id,
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow


def get_workflow_by_id(
    db: Session,
    workflow_id: uuid.UUID,
) -> Workflow | None:
    return db.get(Workflow, workflow_id)


def get_workflow_by_slug(
    db: Session,
    project_id: uuid.UUID,
    slug: str,
) -> Workflow | None:
    return db.scalar(
        select(Workflow).where(
            Workflow.project_id == project_id,
            Workflow.slug == slug,
        )
    )


def list_workflows(
    db: Session,
    project_id: uuid.UUID | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Workflow]:
    statement = select(Workflow)
    if project_id is not None:
        statement = statement.where(Workflow.project_id == project_id)
    statement = (
        statement.order_by(Workflow.created_at, Workflow.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def list_workflows_for_user(
    db: Session,
    user_id: uuid.UUID,
    project_id: uuid.UUID | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Workflow]:
    """List only workflows belonging to projects visible to a user."""

    statement = (
        select(Workflow)
        .join(ProjectMember, ProjectMember.project_id == Workflow.project_id)
        .where(ProjectMember.user_id == user_id)
    )
    if project_id is not None:
        statement = statement.where(Workflow.project_id == project_id)
    statement = (
        statement.order_by(Workflow.created_at, Workflow.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def update_workflow(
    db: Session,
    workflow: Workflow,
    **fields: object,
) -> Workflow:
    if set(fields) - UPDATABLE_FIELDS:
        raise ValueError("Unsupported workflow update field.")
    for field_name, value in fields.items():
        setattr(workflow, field_name, value)
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow
