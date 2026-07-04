"""Top-level router for OutcomeIQ API version 1."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    costs,
    health,
    organizations,
    projects,
    workflow_runs,
    workflows,
)


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
api_router.include_router(
    workflows.router,
    prefix="/workflows",
    tags=["workflows"],
)
api_router.include_router(
    workflow_runs.router,
    prefix="/workflow-runs",
    tags=["workflow-runs"],
)
api_router.include_router(
    costs.router,
    prefix="/costs",
    tags=["costs"],
)
