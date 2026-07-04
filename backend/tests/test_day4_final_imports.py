"""Final import check for the completed Day 4 backend surface."""

from app.api.v1.endpoints import auth, organizations, projects
from app.core import security
from app.services import auth_service


def test_day4_modules_are_importable_without_external_services() -> None:
    assert auth.router is not None
    assert organizations.router is not None
    assert projects.router is not None
    assert callable(security.get_password_hash)
    assert callable(security.create_access_token)
    assert callable(auth_service.register_user)
    assert callable(auth_service.authenticate_user)
