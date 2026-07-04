"""Import and route-registration tests for organization/project APIs."""

from app.api.v1.endpoints import organizations, projects
from app.main import app
from app.repositories import (
    audit_repository,
    organization_repository,
    project_member_repository,
    project_repository,
)


def test_organization_project_modules_and_routes_are_registered() -> None:
    repository_functions = (
        organization_repository.create_organization,
        organization_repository.get_organization_by_id,
        organization_repository.get_organization_by_slug,
        organization_repository.list_organizations,
        organization_repository.update_organization,
        project_repository.create_project,
        project_repository.get_project_by_id,
        project_repository.get_project_by_slug,
        project_repository.list_projects,
        project_repository.update_project,
        project_member_repository.add_project_member,
        project_member_repository.get_project_member,
        project_member_repository.list_project_members,
        project_member_repository.list_user_project_memberships,
        audit_repository.create_audit_event,
    )
    assert all(callable(function) for function in repository_functions)

    organization_paths = {route.path for route in organizations.router.routes}
    project_paths = {route.path for route in projects.router.routes}
    assert organization_paths == {"", "/{organization_id}"}
    assert project_paths == {"", "/{project_id}", "/{project_id}/members"}

    openapi_paths = set(app.openapi()["paths"])
    assert {
        "/api/v1/organizations",
        "/api/v1/organizations/{organization_id}",
        "/api/v1/projects",
        "/api/v1/projects/{project_id}",
        "/api/v1/projects/{project_id}/members",
    } <= openapi_paths
