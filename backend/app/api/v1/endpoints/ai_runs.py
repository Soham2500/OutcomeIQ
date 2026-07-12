"""Authenticated real AI run endpoints."""

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.ai_run import AiRunCreate, AiRunListItem, AiRunRead
from app.services.ai.service import (
    AiRunValidationError,
    create_ai_run,
    list_ai_runs,
)


router = APIRouter()


@router.post("/runs", response_model=AiRunRead, status_code=status.HTTP_201_CREATED)
def create_ai_run_endpoint(
    request: AiRunCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> AiRunRead:
    try:
        return create_ai_run(db, request, current_user)
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project membership is required.",
        ) from exc
    except AiRunValidationError as exc:
        message = str(exc)
        status_code = (
            status.HTTP_404_NOT_FOUND
            if message == "Project not found."
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=message) from exc


@router.get("/runs", response_model=list[AiRunListItem])
def list_ai_runs_endpoint(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    project_id: uuid.UUID | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[AiRunListItem]:
    try:
        return list_ai_runs(
            db,
            current_user=current_user,
            project_id=project_id,
            limit=limit,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project membership is required.",
        ) from exc
