"""Redaction-safe audit event model without logging behavior."""

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class AuditEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Store significant future user or system actions without secrets."""

    __tablename__ = "audit_events"

    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "users.id",
            name="fk_audit_events_actor_user_id_users",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "organizations.id",
            name="fk_audit_events_organization_id_organizations",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey(
            "projects.id",
            name="fk_audit_events_project_id_projects",
            ondelete="RESTRICT",
        ),
        nullable=True,
    )
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    entity_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict[str, object] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
