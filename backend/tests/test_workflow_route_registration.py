"""Route-registration tests for the workflow logging API."""

from app.main import app


def test_workflow_logging_routes_are_registered() -> None:
    expected_paths = {
        "/api/v1/workflows",
        "/api/v1/workflows/{workflow_id}",
        "/api/v1/workflows/{workflow_id}/configurations",
        "/api/v1/workflow-runs",
        "/api/v1/workflow-runs/{workflow_run_id}",
        "/api/v1/workflow-runs/{workflow_run_id}/model-calls",
        "/api/v1/workflow-runs/{workflow_run_id}/tool-calls",
        "/api/v1/workflow-runs/{workflow_run_id}/complete",
        "/api/v1/workflow-runs/{workflow_run_id}/fail",
        "/api/v1/workflow-runs/{workflow_run_id}/trace",
    }

    assert expected_paths <= set(app.openapi()["paths"])
