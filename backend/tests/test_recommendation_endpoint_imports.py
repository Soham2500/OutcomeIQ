"""Import tests for recommendation endpoints."""

from app.api.v1.endpoints import recommendations


def test_recommendation_endpoint_functions_are_importable() -> None:
    functions = (
        recommendations.generate_recommendations_endpoint,
        recommendations.list_recommendations_endpoint,
        recommendations.get_recommendation_endpoint,
        recommendations.update_recommendation_endpoint,
    )
    assert all(callable(function) for function in functions)
