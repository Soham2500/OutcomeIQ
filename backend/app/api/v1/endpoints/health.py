"""Liveness and readiness endpoints."""

from fastapi import APIRouter

from app.core.config import get_settings


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
async def readiness_check() -> dict[str, str]:
    """Report dependency readiness without opening external connections."""

    return {
        "status": "ready",
        "database": "not_configured",
        "redis": "not_configured",
    }
