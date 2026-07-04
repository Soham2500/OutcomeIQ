"""Application service for safe, simulated workflow telemetry logging."""

import uuid

from sqlalchemy.orm import Session

from app.models.enums import AuditAction, WorkflowRunStatus
from app.models.model_call import ModelCall
from app.models.tool_call import ToolCall
from app.models.workflow import Workflow
from app.models.workflow_configuration import WorkflowConfiguration
from app.models.workflow_run import WorkflowRun
from app.repositories.model_call_repository import create_model_call, list_model_calls
from app.repositories.project_repository import get_project_by_id
from app.repositories.tool_call_repository import create_tool_call, list_tool_calls
from app.repositories.workflow_configuration_repository import (
    create_workflow_configuration,
    get_configuration_by_id,
    get_configuration_by_version,
)
from app.repositories.workflow_repository import (
    create_workflow,
    get_workflow_by_id,
    get_workflow_by_slug,
)
from app.repositories.workflow_run_repository import (
    complete_workflow_run,
    create_workflow_run,
    fail_workflow_run,
    get_workflow_run_by_id,
    mark_workflow_run_running,
)
from app.schemas.model_call import ModelCallCreate
from app.schemas.tool_call import ToolCallCreate
from app.schemas.workflow import WorkflowCreate
from app.schemas.workflow_configuration import WorkflowConfigurationCreate
from app.schemas.workflow_run import (
    WorkflowRunCompleteRequest,
    WorkflowRunCreate,
    WorkflowRunFailRequest,
)
from app.services.audit_service import record_audit_event


def create_workflow_for_project(
    db: Session,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
    data: WorkflowCreate,
) -> Workflow:
    if data.project_id != project_id:
        raise ValueError("Workflow project does not match the requested project.")
    if get_project_by_id(db, project_id) is None:
        raise LookupError("Project not found.")
    if get_workflow_by_slug(db, project_id, data.slug) is not None:
        raise ValueError("Workflow slug is already in use for this project.")

    workflow = create_workflow(
        db,
        project_id=project_id,
        name=data.name,
        slug=data.slug,
        description=data.description,
        created_by_user_id=user_id,
    )
    record_audit_event(
        db,
        action=AuditAction.CREATE.value,
        message="Workflow created",
        actor_user_id=user_id,
        project_id=project_id,
        entity_type="workflow",
        entity_id=str(workflow.id),
    )
    return workflow


def create_configuration_for_workflow(
    db: Session,
    workflow_id: uuid.UUID,
    user_id: uuid.UUID,
    data: WorkflowConfigurationCreate,
) -> WorkflowConfiguration:
    workflow = get_workflow_by_id(db, workflow_id)
    if workflow is None:
        raise LookupError("Workflow not found.")
    if get_configuration_by_version(
        db,
        workflow_id,
        data.version_label,
    ) is not None:
        raise ValueError(
            "Configuration version is already in use for this workflow."
        )

    configuration = create_workflow_configuration(
        db,
        workflow_id=workflow_id,
        created_by_user_id=user_id,
        **data.model_dump(mode="json"),
    )
    record_audit_event(
        db,
        action=AuditAction.CREATE.value,
        message="Workflow configuration created",
        actor_user_id=user_id,
        project_id=workflow.project_id,
        entity_type="workflow_configuration",
        entity_id=str(configuration.id),
    )
    return configuration


def start_workflow_run(
    db: Session,
    project_id: uuid.UUID,
    workflow_id: uuid.UUID,
    user_id: uuid.UUID,
    data: WorkflowRunCreate,
) -> WorkflowRun:
    if data.project_id != project_id or data.workflow_id != workflow_id:
        raise ValueError("Workflow run identifiers are inconsistent.")

    workflow = get_workflow_by_id(db, workflow_id)
    if workflow is None:
        raise LookupError("Workflow not found.")
    if workflow.project_id != project_id:
        raise ValueError("Workflow does not belong to the selected project.")
    if data.configuration_id is not None:
        configuration = get_configuration_by_id(db, data.configuration_id)
        if configuration is None:
            raise LookupError("Workflow configuration not found.")
        if configuration.workflow_id != workflow_id:
            raise ValueError(
                "Workflow configuration does not belong to the workflow."
            )

    workflow_run = create_workflow_run(
        db,
        project_id=project_id,
        workflow_id=workflow_id,
        configuration_id=data.configuration_id,
        triggered_by_user_id=user_id,
        trigger_type=data.trigger_type.value,
        external_reference=data.external_reference,
        input_summary=data.input_summary,
        metadata_json=data.metadata_json,
    )
    workflow_run = mark_workflow_run_running(db, workflow_run)
    record_audit_event(
        db,
        action=AuditAction.CREATE.value,
        message="Workflow run started",
        actor_user_id=user_id,
        project_id=project_id,
        entity_type="workflow_run",
        entity_id=str(workflow_run.id),
    )
    return workflow_run


def _get_running_run(db: Session, workflow_run_id: uuid.UUID) -> WorkflowRun:
    workflow_run = get_workflow_run_by_id(db, workflow_run_id)
    if workflow_run is None:
        raise LookupError("Workflow run not found.")
    if workflow_run.status != WorkflowRunStatus.RUNNING.value:
        raise ValueError("Telemetry can only be recorded for a running workflow run.")
    return workflow_run


def record_model_call(
    db: Session,
    workflow_run_id: uuid.UUID,
    data: ModelCallCreate,
) -> ModelCall:
    _get_running_run(db, workflow_run_id)
    return create_model_call(
        db,
        workflow_run_id=workflow_run_id,
        **data.model_dump(mode="json"),
    )


def record_tool_call(
    db: Session,
    workflow_run_id: uuid.UUID,
    data: ToolCallCreate,
) -> ToolCall:
    _get_running_run(db, workflow_run_id)
    return create_tool_call(
        db,
        workflow_run_id=workflow_run_id,
        **data.model_dump(mode="json"),
    )


def complete_run(
    db: Session,
    workflow_run_id: uuid.UUID,
    data: WorkflowRunCompleteRequest,
) -> WorkflowRun:
    workflow_run = _get_running_run(db, workflow_run_id)
    workflow_run = complete_workflow_run(
        db,
        workflow_run,
        **data.model_dump(mode="json"),
    )
    record_audit_event(
        db,
        action=AuditAction.UPDATE.value,
        message="Workflow run completed",
        actor_user_id=workflow_run.triggered_by_user_id,
        project_id=workflow_run.project_id,
        entity_type="workflow_run",
        entity_id=str(workflow_run.id),
    )
    return workflow_run


def fail_run(
    db: Session,
    workflow_run_id: uuid.UUID,
    data: WorkflowRunFailRequest,
) -> WorkflowRun:
    workflow_run = _get_running_run(db, workflow_run_id)
    workflow_run = fail_workflow_run(
        db,
        workflow_run,
        **data.model_dump(mode="json"),
    )
    record_audit_event(
        db,
        action=AuditAction.UPDATE.value,
        message="Workflow run failed",
        actor_user_id=workflow_run.triggered_by_user_id,
        project_id=workflow_run.project_id,
        entity_type="workflow_run",
        entity_id=str(workflow_run.id),
    )
    return workflow_run


def get_workflow_run_trace(
    db: Session,
    workflow_run_id: uuid.UUID,
) -> dict[str, object]:
    workflow_run = get_workflow_run_by_id(db, workflow_run_id)
    if workflow_run is None:
        raise LookupError("Workflow run not found.")
    return {
        "workflow_run": workflow_run,
        "model_calls": list_model_calls(db, workflow_run_id),
        "tool_calls": list_tool_calls(db, workflow_run_id),
    }
