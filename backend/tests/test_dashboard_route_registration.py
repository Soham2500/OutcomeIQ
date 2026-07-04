"""Route-registration tests for protected dashboard APIs."""

from app.main import app


def test_dashboard_routes_are_registered_and_protected() -> None:
    openapi_paths = app.openapi()["paths"]
    expected_paths = {
        "/api/v1/dashboard/projects/{project_id}/overview",
        "/api/v1/dashboard/projects/{project_id}/workflow-runs",
        "/api/v1/dashboard/projects/{project_id}/cost-summary",
        "/api/v1/dashboard/projects/{project_id}/outcome-summary",
    }

    assert expected_paths <= set(openapi_paths)
    operations = [openapi_paths[path]["get"] for path in expected_paths]
    assert all(operation.get("security") for operation in operations)
    assert "get" in openapi_paths[
        "/api/v1/dashboard/projects/{project_id}/workflow-runs"
    ]
