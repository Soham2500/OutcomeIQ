"""Import tests for the core repository functions."""

from app.repositories.audit_repository import (
    create_audit_event,
    list_audit_events,
)
from app.repositories.organization_repository import (
    create_organization,
    get_organization_by_slug,
    list_organizations,
)
from app.repositories.project_member_repository import (
    add_project_member,
    list_project_members,
)
from app.repositories.project_repository import (
    create_project,
    get_project_by_slug,
    list_projects,
)
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
    list_users,
)


def test_repository_functions_are_importable() -> None:
    repository_functions = (
        get_user_by_email,
        create_user,
        list_users,
        get_organization_by_slug,
        create_organization,
        list_organizations,
        get_project_by_slug,
        create_project,
        list_projects,
        add_project_member,
        list_project_members,
        create_audit_event,
        list_audit_events,
    )

    assert all(callable(function) for function in repository_functions)
