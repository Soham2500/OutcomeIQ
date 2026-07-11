"""Usage limit helpers for subscription-aware soft enforcement."""

from datetime import datetime, timezone
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.usage_counter import UsageCounter
from app.models.workflow_run import WorkflowRun
from app.services.billing_service import get_current_plan_and_subscription


LIMIT_MESSAGE = "Plan limit reached. Please upgrade your subscription."


def current_period_month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def count_user_projects(db: Session, user_id: uuid.UUID) -> int:
    return int(
        db.scalar(
            select(func.count(Project.id))
            .join(ProjectMember, ProjectMember.project_id == Project.id)
            .where(ProjectMember.user_id == user_id)
        )
        or 0
    )


def count_user_workflow_runs_for_month(
    db: Session,
    user_id: uuid.UUID,
    period_month: str,
) -> int:
    period_start = datetime.strptime(period_month, "%Y-%m").replace(tzinfo=timezone.utc)
    if period_start.month == 12:
        period_end = period_start.replace(year=period_start.year + 1, month=1)
    else:
        period_end = period_start.replace(month=period_start.month + 1)
    return int(
        db.scalar(
            select(func.count(WorkflowRun.id))
            .join(ProjectMember, ProjectMember.project_id == WorkflowRun.project_id)
            .where(ProjectMember.user_id == user_id)
            .where(WorkflowRun.created_at >= period_start)
            .where(WorkflowRun.created_at < period_end)
        )
        or 0
    )


def get_or_create_usage_counter(
    db: Session,
    user_id: uuid.UUID,
    period_month: str | None = None,
) -> UsageCounter:
    period = period_month or current_period_month()
    counter = db.scalar(
        select(UsageCounter).where(
            UsageCounter.user_id == user_id,
            UsageCounter.period_month == period,
        )
    )
    if counter is not None:
        return counter

    counter = UsageCounter(
        user_id=user_id,
        period_month=period,
        workflow_runs_used=count_user_workflow_runs_for_month(db, user_id, period),
        projects_used=count_user_projects(db, user_id),
    )
    db.add(counter)
    db.commit()
    db.refresh(counter)
    return counter


def get_usage_summary(db: Session, user_id: uuid.UUID) -> dict[str, int | str]:
    plan, _subscription = get_current_plan_and_subscription(db, user_id)
    period = current_period_month()
    counter = get_or_create_usage_counter(db, user_id, period)
    projects_used = count_user_projects(db, user_id)
    workflow_runs_used = count_user_workflow_runs_for_month(db, user_id, period)
    counter.projects_used = projects_used
    counter.workflow_runs_used = workflow_runs_used
    db.add(counter)
    db.commit()
    return {
        "period_month": period,
        "projects_used": projects_used,
        "max_projects": plan.max_projects,
        "workflow_runs_used": workflow_runs_used,
        "max_workflow_runs_per_month": plan.max_workflow_runs_per_month,
    }


def check_project_creation_limit(db: Session, user_id: uuid.UUID) -> None:
    plan, _subscription = get_current_plan_and_subscription(db, user_id)
    if count_user_projects(db, user_id) >= plan.max_projects:
        raise PermissionError(LIMIT_MESSAGE)


def check_workflow_run_monthly_limit(db: Session, user_id: uuid.UUID) -> None:
    plan, _subscription = get_current_plan_and_subscription(db, user_id)
    used = count_user_workflow_runs_for_month(db, user_id, current_period_month())
    if used >= plan.max_workflow_runs_per_month:
        raise PermissionError(LIMIT_MESSAGE)


def increment_workflow_run_usage(db: Session, user_id: uuid.UUID) -> UsageCounter:
    counter = get_or_create_usage_counter(db, user_id)
    counter.workflow_runs_used += 1
    db.add(counter)
    db.commit()
    db.refresh(counter)
    return counter
