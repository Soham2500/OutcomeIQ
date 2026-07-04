"""Import and status tests for authentication/authorization dependencies."""

import uuid

import pytest
from fastapi import HTTPException

from app.api import dependencies
from app.api.dependencies import (
    get_current_active_user,
    get_current_user,
    require_project_member,
    require_project_owner_or_admin,
)
from app.models.enums import ProjectMemberRole, UserStatus
from app.models.project_member import ProjectMember
from app.models.user import User


def test_api_dependency_functions_are_importable() -> None:
    assert callable(get_current_user)
    assert callable(get_current_active_user)
    assert callable(require_project_member)
    assert callable(require_project_owner_or_admin)


def test_inactive_user_is_rejected_with_forbidden() -> None:
    inactive_user = User(
        id=uuid.uuid4(),
        email="inactive@example.com",
        status=UserStatus.INACTIVE.value,
    )

    with pytest.raises(HTTPException) as exc_info:
        get_current_active_user(inactive_user)

    assert exc_info.value.status_code == 403


def test_project_membership_is_required(monkeypatch) -> None:
    project_id = uuid.uuid4()
    current_user = User(id=uuid.uuid4(), email="member@example.com")
    monkeypatch.setattr(dependencies, "get_project_by_id", lambda *_: object())
    monkeypatch.setattr(dependencies, "get_project_member", lambda *_: None)

    with pytest.raises(HTTPException) as exc_info:
        require_project_member(project_id, None, current_user)

    assert exc_info.value.status_code == 403


def test_owner_or_admin_role_is_required() -> None:
    membership = ProjectMember(
        project_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        role=ProjectMemberRole.MEMBER.value,
    )

    with pytest.raises(HTTPException) as exc_info:
        require_project_owner_or_admin(membership)

    assert exc_info.value.status_code == 403

    membership.role = ProjectMemberRole.OWNER.value
    assert require_project_owner_or_admin(membership) is membership
