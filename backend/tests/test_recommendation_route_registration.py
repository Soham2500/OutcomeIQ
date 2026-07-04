"""Route-registration tests for protected recommendation APIs."""

from app.main import app


def test_recommendation_routes_are_registered_and_protected() -> None:
    openapi_paths = app.openapi()["paths"]
    expected_paths = {
        "/api/v1/recommendations/generate",
        "/api/v1/recommendations",
        "/api/v1/recommendations/{recommendation_id}",
    }

    assert expected_paths <= set(openapi_paths)
    operations = [
        operation
        for path in expected_paths
        for operation in openapi_paths[path].values()
    ]
    assert len(operations) == 4
    assert all(operation.get("security") for operation in operations)
