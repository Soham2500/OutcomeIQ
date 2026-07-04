"""Route-registration tests for protected cost APIs."""

from app.main import app


def test_cost_routes_are_registered_and_protected() -> None:
    openapi_paths = app.openapi()["paths"]
    expected_paths = {
        "/api/v1/costs/workflow-runs/{workflow_run_id}/calculate",
        "/api/v1/costs/workflow-runs/{workflow_run_id}",
        "/api/v1/costs/pricing-rates",
    }

    assert expected_paths <= set(openapi_paths)
    operations = [
        operation
        for path in expected_paths
        for operation in openapi_paths[path].values()
    ]
    assert operations
    assert all(operation.get("security") for operation in operations)
