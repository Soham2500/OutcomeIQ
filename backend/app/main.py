"""FastAPI application entry point for OutcomeIQ."""

from contextlib import asynccontextmanager
import logging
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.constants import API_VERSION, SERVICE_NAME
from app.core.logging import configure_logging


settings = get_settings()
configure_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Log application lifecycle events without initializing external services."""

    logger.info(
        "OutcomeIQ API starting",
        extra={
            "event": "application_startup",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        },
    )
    yield
    logger.info(
        "OutcomeIQ API stopping",
        extra={"event": "application_shutdown", "service": settings.APP_NAME},
    )


app = FastAPI(
    title=SERVICE_NAME,
    description="Outcome-aware AI FinOps Platform API",
    version=API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["root"])
async def read_root() -> dict[str, str]:
    """Return a small service-discovery response."""

    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }
