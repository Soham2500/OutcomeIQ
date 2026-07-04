"""Import and isolated endpoint-flow tests for authentication."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api import dependencies
from app.api.v1.endpoints import auth
from app.core import security
from app.db.session import get_db
from app.main import app
from app.models.user import User
from app.services import auth_service


def test_auth_modules_and_routes_are_importable() -> None:
    assert callable(dependencies.get_current_user)
    assert callable(auth_service.register_user)
    assert callable(auth_service.authenticate_user)
    assert callable(auth_service.create_user_access_token)

    route_paths = {route.path for route in auth.router.routes}
    assert route_paths == {"/register", "/login", "/me"}


def test_register_login_and_current_user_flow(monkeypatch) -> None:
    """Exercise auth against isolated SQLite, never the local PostgreSQL DB."""

    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    User.__table__.create(engine)
    test_session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    def override_get_db():
        database_session = test_session_factory()
        try:
            yield database_session
        finally:
            database_session.close()

    monkeypatch.setattr(
        security.settings,
        "JWT_SECRET_KEY",
        "isolated-auth-flow-test-secret",
    )
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            registration = client.post(
                "/api/v1/auth/register",
                json={
                    "email": "auth.test@example.com",
                    "full_name": "Auth Test",
                    "password": "password123",
                },
            )
            assert registration.status_code == 201
            assert "hashed_password" not in registration.json()

            duplicate = client.post(
                "/api/v1/auth/register",
                json={
                    "email": "auth.test@example.com",
                    "password": "password123",
                },
            )
            assert duplicate.status_code == 400

            invalid_login = client.post(
                "/api/v1/auth/login",
                json={
                    "email": "auth.test@example.com",
                    "password": "wrong-password",
                },
            )
            assert invalid_login.status_code == 401

            login = client.post(
                "/api/v1/auth/login",
                json={
                    "email": "auth.test@example.com",
                    "password": "password123",
                },
            )
            assert login.status_code == 200
            token = login.json()["access_token"]

            assert client.get("/api/v1/auth/me").status_code == 401
            current_user = client.get(
                "/api/v1/auth/me",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert current_user.status_code == 200
            assert current_user.json()["email"] == "auth.test@example.com"
            assert "hashed_password" not in current_user.json()
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
