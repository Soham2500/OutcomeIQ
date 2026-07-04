"""Database access functions for project memberships."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import ProjectMemberRole
from app.models.project_member import ProjectMember


def get_project_member(
    db: Session,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
) -> ProjectMember | None:
    return db.scalar(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )
    )


def add_project_member(
    db: Session,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
    role: str = ProjectMemberRole.MEMBER.value,
) -> ProjectMember:
    project_member = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role=role,
    )
    db.add(project_member)
    db.commit()
    db.refresh(project_member)
    return project_member


def list_project_members(
    db: Session,
    project_id: uuid.UUID,
) -> list[ProjectMember]:
    statement = (
        select(ProjectMember)
        .where(ProjectMember.project_id == project_id)
        .order_by(ProjectMember.created_at, ProjectMember.id)
    )
    return list(db.scalars(statement))


def list_user_project_memberships(
    db: Session,
    user_id: uuid.UUID,
) -> list[ProjectMember]:
    statement = (
        select(ProjectMember)
        .where(ProjectMember.user_id == user_id)
        .order_by(ProjectMember.created_at, ProjectMember.id)
    )
    return list(db.scalars(statement))
