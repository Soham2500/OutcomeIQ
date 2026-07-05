"""Tests for the initial service-discovery and health endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.db import health as database_health
from app.main import app


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_root(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "service": "OutcomeIQ API",
        "version": "0.1.0",
        "docs": "/docs",
    }


def test_health(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "OutcomeIQ API",
        "version": "0.1.0",
    }


def test_ready(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    # Readiness tests must never require a real PostgreSQL instance.
    monkeypatch.setattr(database_health.settings, "DATABASE_URL", None)
    response = client.get("/api/v1/ready")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    assert payload["database"] in {"not_configured", "connected", "error"}
    assert payload["database"] == "not_configured"
    assert payload["redis"] == "not_configured"


def test_local_frontend_origins_pass_cors_preflight(client: TestClient) -> None:
    local_origins = (
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    )

    for origin in local_origins:
        response = client.options(
            "/api/v1/auth/login",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == origin
        assert response.headers["access-control-allow-credentials"] == "true"
