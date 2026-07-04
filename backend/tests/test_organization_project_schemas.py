"""Validation tests for organization, project and membership schemas."""

import uuid

import pytest
from pydantic import ValidationError

from app.models.enums import OrganizationStatus, ProjectMemberRole, ProjectStatus
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.project_member import ProjectMemberCreate


def test_organization_and_project_schemas_accept_valid_data() -> None:
    organization = OrganizationCreate(name="Acme Payments", slug="acme-payments")
    project = ProjectCreate(
        organization_id=uuid.uuid4(),
        name="AI Support",
        slug="ai-support",
        description="Synthetic support project",
    )
    membership = ProjectMemberCreate(
        project_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        role=ProjectMemberRole.OWNER,
    )

    assert organization.slug == "acme-payments"
    assert project.slug == "ai-support"
    assert membership.role == ProjectMemberRole.OWNER


def test_slug_and_update_validation() -> None:
    with pytest.raises(ValidationError):
        OrganizationCreate(name="Acme", slug="Not Lowercase")

    with pytest.raises(ValidationError):
        ProjectCreate(
            organization_id=uuid.uuid4(),
            name="Support",
            slug="invalid_slug",
        )

    organization_update = OrganizationUpdate(status=OrganizationStatus.INACTIVE)
    project_update = ProjectUpdate(
        description=None,
        status=ProjectStatus.ARCHIVED,
    )
    assert organization_update.model_dump(exclude_unset=True, mode="json") == {
        "status": "inactive"
    }
    assert project_update.model_dump(exclude_unset=True, mode="json") == {
        "description": None,
        "status": "archived",
    }
