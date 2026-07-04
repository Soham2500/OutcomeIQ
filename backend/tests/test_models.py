"""Import and metadata-registration tests for approved database models."""

from app.db.base import Base
from app.models.audit_event import AuditEvent
from app.models.organization import Organization
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.system import SystemMetadata
from app.models.user import User


def test_approved_models_are_registered_with_base() -> None:
    """Alembic metadata should contain only the approved model batch."""

    expected_models = {
        SystemMetadata: "system_metadata",
        User: "users",
        Organization: "organizations",
        Project: "projects",
        ProjectMember: "project_members",
        AuditEvent: "audit_events",
    }

    assert {
        model.__tablename__ for model in expected_models
    } == set(Base.metadata.tables)
    for model, table_name in expected_models.items():
        assert model.__table__ is Base.metadata.tables[table_name]
