"""Import and isolated endpoint-flow tests for authentication."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api import dependencies
from app.api.v1.endpoints import auth
from app.core import security
from app.db.session import get_db
from app.models.pending_registration import PendingRegistration
from app.main import app
from app.models.user import User
from app.services import auth_service


def test_auth_modules_and_routes_are_importable() -> None:
    assert callable(dependencies.get_current_user)
    assert callable(auth_service.register_user)
    assert callable(auth_service.request_registration_otp)
    assert callable(auth_service.verify_registration_otp)
    assert callable(auth_service.authenticate_user)
    assert callable(auth_service.create_user_access_token)

    route_paths = {route.path for route in auth.router.routes}
    assert route_paths == {
        "/register",
        "/register/request-otp",
        "/register/verify-otp",
        "/login",
        "/me",
    }


def test_register_login_and_current_user_flow(monkeypatch) -> None:
    """Exercise auth against isolated SQLite, never the local PostgreSQL DB."""

    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    User.__table__.create(engine)
    PendingRegistration.__table__.create(engine)
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
    monkeypatch.setattr(auth, "record_audit_event", lambda *args, **kwargs: None)
    app.dependency_overrides[get_db] = override_get_db

    try:
        with test_session_factory() as database_session:
            auth_service.register_user(
                database_session,
                email="auth.test@example.com",
                full_name="Auth Test",
                password="password123",
            )

        with TestClient(app) as client:
            duplicate = client.post(
                "/api/v1/auth/register",
                json={
                    "email": "auth.test@example.com",
                    "password": "password123",
                },
            )
            assert duplicate.status_code == 409

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


def test_request_and_verify_registration_otp_flow(monkeypatch) -> None:
    """Exercise email OTP registration without sending a real SMTP message."""

    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    User.__table__.create(engine)
    PendingRegistration.__table__.create(engine)
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

    sent_messages: list[tuple[str, str]] = []
    monkeypatch.setattr(
        security.settings,
        "JWT_SECRET_KEY",
        "isolated-otp-flow-test-secret",
    )
    monkeypatch.setattr(auth, "record_audit_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(auth_service, "generate_numeric_otp", lambda: "123456")
    monkeypatch.setattr(
        auth_service,
        "send_registration_otp_email",
        lambda email, otp: sent_messages.append((email, otp)),
    )
    monkeypatch.setattr(auth_service.get_settings(), "OTP_RESEND_COOLDOWN_SECONDS", 0)
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            legacy_request = client.post(
                "/api/v1/auth/register",
                json={
                    "email": "legacy.otp@example.com",
                    "full_name": "Legacy OTP",
                    "password": "password123",
                },
            )
            assert legacy_request.status_code == 202
            assert legacy_request.json() == {"message": "OTP sent"}
            assert sent_messages == [("legacy.otp@example.com", "123456")]

            legacy_login = client.post(
                "/api/v1/auth/login",
                json={
                    "email": "legacy.otp@example.com",
                    "password": "password123",
                },
            )
            assert legacy_login.status_code == 401
            with test_session_factory() as database_session:
                assert (
                    database_session.query(User)
                    .filter_by(email="legacy.otp@example.com")
                    .one_or_none()
                    is None
                )
                legacy_pending = (
                    database_session.query(PendingRegistration)
                    .filter_by(email="legacy.otp@example.com")
                    .one()
                )
                assert legacy_pending.hashed_otp != "123456"

            request_otp = client.post(
                "/api/v1/auth/register/request-otp",
                json={
                    "email": "otp.test@example.com",
                    "full_name": "OTP Test",
                    "password": "password123",
                },
            )
            assert request_otp.status_code == 200
            assert request_otp.json() == {"message": "OTP sent"}
            assert sent_messages[-1] == ("otp.test@example.com", "123456")

            with test_session_factory() as database_session:
                pending = (
                    database_session.query(PendingRegistration)
                    .filter_by(email="otp.test@example.com")
                    .one()
                )
                assert pending.hashed_otp != "123456"
                assert auth_service.verify_password("123456", pending.hashed_otp)

            wrong_otp = client.post(
                "/api/v1/auth/register/verify-otp",
                json={"email": "otp.test@example.com", "otp": "000000"},
            )
            assert wrong_otp.status_code == 400

            verify_otp = client.post(
                "/api/v1/auth/register/verify-otp",
                json={"email": "otp.test@example.com", "otp": "123456"},
            )
            assert verify_otp.status_code == 201
            assert verify_otp.json()["email"] == "otp.test@example.com"
            assert "hashed_password" not in verify_otp.json()

            duplicate_request = client.post(
                "/api/v1/auth/register/request-otp",
                json={
                    "email": "otp.test@example.com",
                    "full_name": "OTP Test",
                    "password": "password123",
                },
            )
            assert duplicate_request.status_code == 409
            assert duplicate_request.json()["detail"] == (
                "Email is already registered. Please login instead."
            )
            assert sent_messages.count(("otp.test@example.com", "123456")) == 1

            duplicate_verify = client.post(
                "/api/v1/auth/register/verify-otp",
                json={"email": "otp.test@example.com", "otp": "123456"},
            )
            assert duplicate_verify.status_code == 409
            assert duplicate_verify.json()["detail"] == (
                "Email is already registered. Please login."
            )
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
