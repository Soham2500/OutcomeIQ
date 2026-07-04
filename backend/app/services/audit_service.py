"""Safe application-level audit recording helper."""

import uuid

from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent
from app.repositories.audit_repository import create_audit_event


SENSITIVE_KEY_FRAGMENTS = (
    "password",
    "token",
    "secret",
    "credential",
    "authorization",
)


def record_audit_event(
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
    """Persist an audit event after removing sensitive top-level metadata keys."""

    safe_metadata = None
    if metadata_json is not None:
        safe_metadata = {
            key: value
            for key, value in metadata_json.items()
            if not any(
                fragment in key.lower()
                for fragment in SENSITIVE_KEY_FRAGMENTS
            )
        }

    return create_audit_event(
        db,
        action=action,
        message=message,
        actor_user_id=actor_user_id,
        organization_id=organization_id,
        project_id=project_id,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata_json=safe_metadata,
    )
