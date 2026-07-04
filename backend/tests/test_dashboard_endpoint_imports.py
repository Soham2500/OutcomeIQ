"""Import tests for dashboard analytics endpoints."""

from app.api.v1.endpoints import dashboard


def test_dashboard_endpoint_functions_are_importable() -> None:
    functions = (
        dashboard.get_project_dashboard_overview_endpoint,
        dashboard.list_project_dashboard_runs_endpoint,
        dashboard.get_project_cost_summary_endpoint,
        dashboard.get_project_outcome_summary_endpoint,
    )
    assert all(callable(function) for function in functions)
    assert dashboard.list_project_dashboard_runs_endpoint.__name__ == (
        "list_project_dashboard_runs_endpoint"
    )
