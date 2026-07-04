"""Import test for development seed orchestration."""

from app.services.dev_seed_service import seed_development_data


def test_seed_service_is_importable() -> None:
    assert callable(seed_development_data)
