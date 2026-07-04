"""Pydantic schemas for redaction-safe audit events."""

from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict

from app.models.enums import AuditAction


class AuditEventCreate(BaseModel):
    action: AuditAction
    message: str | None = None
    actor_user_id: uuid.UUID | None = None
    organization_id: uuid.UUID | None = None
    project_id: uuid.UUID | None = None
    entity_type: str | None = None
    entity_id: str | None = None
    metadata_json: dict[str, object] | None = None


class AuditEventRead(AuditEventCreate):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
