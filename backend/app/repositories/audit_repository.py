"""Database access functions for audit events."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent


def create_audit_event(
    db: Session,
    action: str,
    message: str | None = None,
    actor_user_id: uuid.UUID | None = None,
    organization_id: uuid.UUID | None = None,
    project_id: uuid.UUID | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    metadata_json: dict[str, object] | None = None,
) -> AuditEvent:
    audit_event = AuditEvent(
        action=action,
        message=message,
        actor_user_id=actor_user_id,
        organization_id=organization_id,
        project_id=project_id,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata_json=metadata_json,
    )
    db.add(audit_event)
    db.commit()
    db.refresh(audit_event)
    return audit_event


def list_audit_events(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[AuditEvent]:
    statement = (
        select(AuditEvent)
        .order_by(AuditEvent.created_at.desc(), AuditEvent.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))
