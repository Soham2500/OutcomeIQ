"""Validation tests for workflow logging request schemas."""

import uuid

from app.models.enums import WorkflowRunTrigger
from app.schemas.model_call import ModelCallCreate
from app.schemas.tool_call import ToolCallCreate
from app.schemas.workflow import WorkflowCreate
from app.schemas.workflow_configuration import WorkflowConfigurationCreate
from app.schemas.workflow_run import (
    WorkflowRunCompleteRequest,
    WorkflowRunCreate,
    WorkflowRunFailRequest,
)


def test_workflow_logging_schemas_accept_simulated_data() -> None:
    project_id = uuid.uuid4()
    workflow_id = uuid.uuid4()

    workflow = WorkflowCreate(
        project_id=project_id,
        name="AI Support Resolution",
        slug="ai-support-resolution",
    )
    configuration = WorkflowConfigurationCreate(
        name="Balanced configuration",
        version_label="balanced-v1",
        strategy_name="balanced",
        config_json={"provider": "simulated"},
    )
    workflow_run = WorkflowRunCreate(
        project_id=project_id,
        workflow_id=workflow_id,
        trigger_type=WorkflowRunTrigger.SIMULATED,
        external_reference="support-ticket-123",
    )
    model_call = ModelCallCreate(
        sequence_number=1,
        provider="simulated",
        model_name="simulated-classifier-v1",
        prompt_tokens=100,
        completion_tokens=20,
        total_tokens=120,
    )
    tool_call = ToolCallCreate(
        sequence_number=2,
        tool_name="ticket_status_check",
    )

    assert workflow.project_id == project_id
    assert configuration.config_json == {"provider": "simulated"}
    assert workflow_run.trigger_type is WorkflowRunTrigger.SIMULATED
    assert model_call.total_tokens == 120
    assert tool_call.tool_name == "ticket_status_check"
    assert WorkflowRunCompleteRequest(latency_ms=250).latency_ms == 250
    assert WorkflowRunFailRequest(error_message="simulated failure").error_message
