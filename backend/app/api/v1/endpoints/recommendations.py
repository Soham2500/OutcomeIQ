"""Protected rule-based recommendation endpoints."""

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.enums import (
    RecommendationStatus,
    RecommendationType,
)
from app.models.recommendation import Recommendation
from app.models.user import User
from app.repositories.project_member_repository import get_project_member
from app.repositories.project_repository import get_project_by_id
from app.repositories.recommendation_repository import get_recommendation_by_id
from app.schemas.recommendation import (
    RecommendationGenerateRequest,
    RecommendationGenerateResponse,
    RecommendationRead,
    RecommendationUpdate,
)
from app.services.recommendation_service import (
    generate_project_recommendations,
    list_project_recommendations,
    update_recommendation_status,
)


router = APIRouter()


def _require_project_access(
    db: Session,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
) -> None:
    if get_project_by_id(db, project_id) is None:
        raise HTTPException(status_code=404, detail="Project not found.")
    if get_project_member(db, project_id, user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project membership is required.",
        )


def _get_visible_recommendation(
    db: Session,
    recommendation_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Recommendation:
    recommendation = get_recommendation_by_id(db, recommendation_id)
    if recommendation is None:
        raise HTTPException(status_code=404, detail="Recommendation not found.")
    _require_project_access(db, recommendation.project_id, user_id)
    return recommendation


@router.post(
    "/generate",
    response_model=RecommendationGenerateResponse,
)
def generate_recommendations_endpoint(
    request: RecommendationGenerateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> RecommendationGenerateResponse:
    _require_project_access(db, request.project_id, current_user.id)
    try:
        return generate_project_recommendations(
            db,
            project_id=request.project_id,
            workflow_id=request.workflow_id,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[RecommendationRead])
def list_recommendations_endpoint(
    project_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    workflow_id: uuid.UUID | None = None,
    recommendation_status: Annotated[
        RecommendationStatus | None,
        Query(alias="status"),
    ] = None,
    recommendation_type: RecommendationType | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Recommendation]:
    _require_project_access(db, project_id, current_user.id)
    return list_project_recommendations(
        db,
        project_id=project_id,
        workflow_id=workflow_id,
        status=(
            recommendation_status.value
            if recommendation_status is not None
            else None
        ),
        recommendation_type=(
            recommendation_type.value
            if recommendation_type is not None
            else None
        ),
        limit=limit,
        offset=offset,
    )


@router.get("/{recommendation_id}", response_model=RecommendationRead)
def get_recommendation_endpoint(
    recommendation_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Recommendation:
    return _get_visible_recommendation(db, recommendation_id, current_user.id)


@router.patch("/{recommendation_id}", response_model=RecommendationRead)
def update_recommendation_endpoint(
    recommendation_id: uuid.UUID,
    request: RecommendationUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Recommendation:
    recommendation = _get_visible_recommendation(
        db,
        recommendation_id,
        current_user.id,
    )
    if not request.model_fields_set:
        return recommendation
    target_status = request.status or RecommendationStatus(
        recommendation.status
    )
    try:
        return update_recommendation_status(
            db,
            recommendation_id,
            target_status,
            accepted_at=request.accepted_at,
            dismissed_at=request.dismissed_at,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
