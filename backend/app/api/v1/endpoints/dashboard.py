"""Protected read-only project dashboard analytics endpoints."""

from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import require_project_member
from app.db.session import get_db
from app.models.project_member import ProjectMember
from app.schemas.dashboard import (
    CostDashboardSummaryRead,
    OutcomeDashboardSummaryRead,
    ProjectDashboardOverviewRead,
    WorkflowRunDashboardRead,
)
from app.services.dashboard_analytics_service import (
    get_project_cost_summary,
    get_project_outcome_summary,
    get_project_overview,
    list_project_workflow_runs,
)


router = APIRouter()


@router.get(
    "/projects/{project_id}/overview",
    response_model=ProjectDashboardOverviewRead,
)
def get_project_dashboard_overview_endpoint(
    project_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    _membership: Annotated[ProjectMember, Depends(require_project_member)],
) -> ProjectDashboardOverviewRead:
    return get_project_overview(db, project_id)


@router.get(
    "/projects/{project_id}/workflow-runs",
    response_model=list[WorkflowRunDashboardRead],
)
def list_project_dashboard_runs_endpoint(
    project_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    _membership: Annotated[ProjectMember, Depends(require_project_member)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[WorkflowRunDashboardRead]:
    return list_project_workflow_runs(
        db,
        project_id,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/projects/{project_id}/cost-summary",
    response_model=CostDashboardSummaryRead,
)
def get_project_cost_summary_endpoint(
    project_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    _membership: Annotated[ProjectMember, Depends(require_project_member)],
) -> CostDashboardSummaryRead:
    return get_project_cost_summary(db, project_id)


@router.get(
    "/projects/{project_id}/outcome-summary",
    response_model=OutcomeDashboardSummaryRead,
)
def get_project_outcome_summary_endpoint(
    project_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    _membership: Annotated[ProjectMember, Depends(require_project_member)],
) -> OutcomeDashboardSummaryRead:
    return get_project_outcome_summary(db, project_id)
