"""Idempotent local development seed orchestration."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent
from app.models.enums import AuditAction, ProjectMemberRole
from app.repositories.audit_repository import create_audit_event
from app.repositories.organization_repository import (
    create_organization,
    get_organization_by_slug,
)
from app.repositories.project_member_repository import (
    add_project_member,
    list_project_members,
)
from app.repositories.project_repository import create_project, get_project_by_slug
from app.repositories.user_repository import create_user, get_user_by_email


DEMO_EMAIL = "demo@outcomeiq.local"
DEMO_ORGANIZATION_SLUG = "demo-org"
DEMO_PROJECT_SLUG = "demo-ai-support"
DEMO_AUDIT_MESSAGE = "Development seed data created"


def seed_development_data(db: Session) -> dict[str, str]:
    """Create the safe demo identity/project records only when absent."""

    result: dict[str, str] = {}

    user = get_user_by_email(db, DEMO_EMAIL)
    if user is None:
        user = create_user(
            db,
            email=DEMO_EMAIL,
            full_name="Demo User",
            hashed_password=None,
        )
        result["user"] = "created"
    else:
        result["user"] = "existing"

    organization = get_organization_by_slug(db, DEMO_ORGANIZATION_SLUG)
    if organization is None:
        organization = create_organization(
            db,
            name="Demo Organization",
            slug=DEMO_ORGANIZATION_SLUG,
        )
        result["organization"] = "created"
    else:
        result["organization"] = "existing"

    project = get_project_by_slug(
        db,
        organization_id=organization.id,
        slug=DEMO_PROJECT_SLUG,
    )
    if project is None:
        project = create_project(
            db,
            organization_id=organization.id,
            name="Demo AI Support Project",
            slug=DEMO_PROJECT_SLUG,
            description="Demo project for OutcomeIQ customer support workflow",
        )
        result["project"] = "created"
    else:
        result["project"] = "existing"

    project_members = list_project_members(db, project.id)
    project_member = next(
        (member for member in project_members if member.user_id == user.id),
        None,
    )
    if project_member is None:
        add_project_member(
            db,
            project_id=project.id,
            user_id=user.id,
            role=ProjectMemberRole.OWNER.value,
        )
        result["project_member"] = "created"
    else:
        result["project_member"] = "existing"

    audit_event = db.scalar(
        select(AuditEvent).where(
            AuditEvent.action == AuditAction.SYSTEM.value,
            AuditEvent.message == DEMO_AUDIT_MESSAGE,
            AuditEvent.actor_user_id == user.id,
            AuditEvent.organization_id == organization.id,
            AuditEvent.project_id == project.id,
        )
    )
    if audit_event is None:
        create_audit_event(
            db,
            action=AuditAction.SYSTEM.value,
            message=DEMO_AUDIT_MESSAGE,
            actor_user_id=user.id,
            organization_id=organization.id,
            project_id=project.id,
            entity_type="development_seed",
            entity_id=str(project.id),
            metadata_json={"source": "local_development_seed"},
        )
        result["audit_event"] = "created"
    else:
        result["audit_event"] = "existing"

    return result
