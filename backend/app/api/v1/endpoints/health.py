"""Liveness and readiness endpoints."""

from fastapi import APIRouter

from app.core.config import get_settings
from app.db.health import check_database_connection


router = APIRouter(tags=["system"])
settings = get_settings()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Confirm that the API process is running."""

    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.get("/ready")
def readiness_check() -> dict[str, str]:
    """Report dependency readiness without opening external connections."""

    database_health = check_database_connection()

    return {
        "status": "ready",
        "database": database_health["status"],
        "redis": "not_configured",
    }
