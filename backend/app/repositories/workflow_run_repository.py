"""Database access functions for workflow runs."""

from datetime import datetime, timezone
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import WorkflowRunStatus
from app.models.project_member import ProjectMember
from app.models.workflow_run import WorkflowRun


def create_workflow_run(
    db: Session,
    project_id: uuid.UUID,
    workflow_id: uuid.UUID,
    configuration_id: uuid.UUID | None = None,
    triggered_by_user_id: uuid.UUID | None = None,
    trigger_type: str = "manual",
    external_reference: str | None = None,
    input_summary: str | None = None,
    metadata_json: dict[str, object] | None = None,
) -> WorkflowRun:
    workflow_run = WorkflowRun(
        project_id=project_id,
        workflow_id=workflow_id,
        configuration_id=configuration_id,
        triggered_by_user_id=triggered_by_user_id,
        trigger_type=trigger_type,
        external_reference=external_reference,
        input_summary=input_summary,
        metadata_json=metadata_json,
    )
    db.add(workflow_run)
    db.commit()
    db.refresh(workflow_run)
    return workflow_run


def get_workflow_run_by_id(
    db: Session,
    workflow_run_id: uuid.UUID,
) -> WorkflowRun | None:
    return db.get(WorkflowRun, workflow_run_id)


def list_workflow_runs(
    db: Session,
    project_id: uuid.UUID | None = None,
    workflow_id: uuid.UUID | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[WorkflowRun]:
    statement = select(WorkflowRun)
    if project_id is not None:
        statement = statement.where(WorkflowRun.project_id == project_id)
    if workflow_id is not None:
        statement = statement.where(WorkflowRun.workflow_id == workflow_id)
    if status is not None:
        statement = statement.where(WorkflowRun.status == status)
    statement = (
        statement.order_by(WorkflowRun.created_at, WorkflowRun.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def list_workflow_runs_for_user(
    db: Session,
    user_id: uuid.UUID,
    project_id: uuid.UUID | None = None,
    workflow_id: uuid.UUID | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[WorkflowRun]:
    """List only runs belonging to projects visible to a user."""

    statement = (
        select(WorkflowRun)
        .join(ProjectMember, ProjectMember.project_id == WorkflowRun.project_id)
        .where(ProjectMember.user_id == user_id)
    )
    if project_id is not None:
        statement = statement.where(WorkflowRun.project_id == project_id)
    if workflow_id is not None:
        statement = statement.where(WorkflowRun.workflow_id == workflow_id)
    if status is not None:
        statement = statement.where(WorkflowRun.status == status)
    statement = (
        statement.order_by(WorkflowRun.created_at, WorkflowRun.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def mark_workflow_run_running(
    db: Session,
    workflow_run: WorkflowRun,
) -> WorkflowRun:
    workflow_run.status = WorkflowRunStatus.RUNNING.value
    workflow_run.started_at = datetime.now(timezone.utc)
    db.add(workflow_run)
    db.commit()
    db.refresh(workflow_run)
    return workflow_run


def complete_workflow_run(
    db: Session,
    workflow_run: WorkflowRun,
    output_summary: str | None = None,
    latency_ms: int | None = None,
    metadata_json: dict[str, object] | None = None,
) -> WorkflowRun:
    workflow_run.status = WorkflowRunStatus.SUCCEEDED.value
    workflow_run.output_summary = output_summary
    workflow_run.latency_ms = latency_ms
    workflow_run.completed_at = datetime.now(timezone.utc)
    if metadata_json is not None:
        workflow_run.metadata_json = metadata_json
    db.add(workflow_run)
    db.commit()
    db.refresh(workflow_run)
    return workflow_run


def fail_workflow_run(
    db: Session,
    workflow_run: WorkflowRun,
    error_message: str | None = None,
    latency_ms: int | None = None,
) -> WorkflowRun:
    workflow_run.status = WorkflowRunStatus.FAILED.value
    workflow_run.error_message = error_message
    workflow_run.latency_ms = latency_ms
    workflow_run.completed_at = datetime.now(timezone.utc)
    db.add(workflow_run)
    db.commit()
    db.refresh(workflow_run)
    return workflow_run
