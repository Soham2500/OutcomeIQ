"""Route-registration tests for protected outcome APIs."""

from app.main import app


def test_outcome_routes_are_registered_and_protected() -> None:
    openapi_paths = app.openapi()["paths"]
    expected_paths = {
        "/api/v1/outcomes/contracts",
        "/api/v1/outcomes/contracts/{contract_id}",
        "/api/v1/outcomes/workflow-runs/{workflow_run_id}",
        "/api/v1/outcomes/metrics/cost-per-success",
    }

    assert expected_paths <= set(openapi_paths)
    operations = [
        operation
        for path in expected_paths
        for operation in openapi_paths[path].values()
    ]
    assert operations
    assert all(operation.get("security") for operation in operations)
