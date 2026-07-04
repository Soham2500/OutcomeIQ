"""Top-level router for OutcomeIQ API version 1."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, organizations, projects


api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"],
)
api_router.include_router(
    organizations.router,
    prefix="/organizations",
    tags=["organizations"],
)
api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["projects"],
)
