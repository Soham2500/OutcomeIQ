"""Protected pricing-rate and workflow-run cost endpoints."""

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.model_pricing_rate import ModelPricingRate
from app.models.user import User
from app.models.workflow_run_cost import WorkflowRunCost
from app.repositories.model_pricing_rate_repository import (
    create_pricing_rate,
    list_pricing_rates,
)
from app.repositories.project_member_repository import get_project_member
from app.repositories.workflow_run_cost_repository import (
    get_cost_by_workflow_run_id,
)
from app.repositories.workflow_run_repository import get_workflow_run_by_id
from app.schemas.model_pricing_rate import (
    ModelPricingRateCreate,
    ModelPricingRateRead,
)
from app.schemas.workflow_run_cost import WorkflowRunCostRead
from app.services.cost_calculation_service import calculate_workflow_run_cost


router = APIRouter()


def _require_run_access(
    db: Session,
    workflow_run_id: uuid.UUID,
    user_id: uuid.UUID,
) -> None:
    workflow_run = get_workflow_run_by_id(db, workflow_run_id)
    if workflow_run is None:
        raise HTTPException(status_code=404, detail="Workflow run not found.")
    if get_project_member(db, workflow_run.project_id, user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Project membership is required.",
        )


@router.post(
    "/workflow-runs/{workflow_run_id}/calculate",
    response_model=WorkflowRunCostRead,
)
def calculate_workflow_run_cost_endpoint(
    workflow_run_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> WorkflowRunCost:
    _require_run_access(db, workflow_run_id, current_user.id)
    try:
        return calculate_workflow_run_cost(db, workflow_run_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get(
    "/workflow-runs/{workflow_run_id}",
    response_model=WorkflowRunCostRead,
)
def get_workflow_run_cost_endpoint(
    workflow_run_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> WorkflowRunCost:
    _require_run_access(db, workflow_run_id, current_user.id)
    cost = get_cost_by_workflow_run_id(db, workflow_run_id)
    if cost is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow run cost has not been calculated.",
        )
    return cost


@router.get("/pricing-rates", response_model=list[ModelPricingRateRead])
def list_pricing_rates_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_active_user)],
    provider: str | None = None,
    model_name: str | None = None,
    active_only: bool = True,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[ModelPricingRate]:
    return list_pricing_rates(
        db,
        provider=provider,
        model_name=model_name,
        active_only=active_only,
        limit=limit,
        offset=offset,
    )


@router.post(
    "/pricing-rates",
    response_model=ModelPricingRateRead,
    status_code=status.HTTP_201_CREATED,
)
def create_pricing_rate_endpoint(
    request: ModelPricingRateCreate,
    db: Annotated[Session, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_active_user)],
) -> ModelPricingRate:
    try:
        return create_pricing_rate(db, **request.model_dump(mode="python"))
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An equivalent pricing-rate version already exists.",
        ) from exc
