"""Import and exposure tests for core Pydantic schemas."""

from app.schemas.audit_event import AuditEventCreate, AuditEventRead
from app.schemas.organization import (
    OrganizationBase,
    OrganizationCreate,
    OrganizationRead,
)
from app.schemas.project import ProjectBase, ProjectCreate, ProjectRead
from app.schemas.project_member import ProjectMemberCreate, ProjectMemberRead
from app.schemas.user import UserBase, UserCreate, UserRead


def test_core_schemas_are_importable_and_user_read_is_safe() -> None:
    schema_classes = (
        UserBase,
        UserCreate,
        UserRead,
        OrganizationBase,
        OrganizationCreate,
        OrganizationRead,
        ProjectBase,
        ProjectCreate,
        ProjectRead,
        ProjectMemberCreate,
        ProjectMemberRead,
        AuditEventCreate,
        AuditEventRead,
    )

    assert all(hasattr(schema_class, "model_fields") for schema_class in schema_classes)
    assert "hashed_password" not in UserRead.model_fields
    assert "password" not in UserRead.model_fields
    assert "hashed_password" not in UserCreate.model_fields
    assert "password" not in UserCreate.model_fields
