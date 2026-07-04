"""OpenAPI route registration tests for the Day 4 API surface."""

from inspect import signature

from app.api.v1.endpoints.auth import register
from app.main import app
from app.schemas.auth import RegisterRequest


def test_day4_routes_are_registered() -> None:
    expected_paths = {
        "/api/v1/auth/register",
        "/api/v1/auth/login",
        "/api/v1/auth/me",
        "/api/v1/organizations",
        "/api/v1/organizations/{organization_id}",
        "/api/v1/projects",
        "/api/v1/projects/{project_id}",
        "/api/v1/projects/{project_id}/members",
    }

    assert expected_paths <= set(app.openapi()["paths"])
    assert signature(register).parameters["request"].annotation is RegisterRequest
