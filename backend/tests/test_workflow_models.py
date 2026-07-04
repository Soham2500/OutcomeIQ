"""Import and metadata-registration tests for workflow logging models."""

from app.db.base import Base
from app.models.model_call import ModelCall
from app.models.tool_call import ToolCall
from app.models.workflow import Workflow
from app.models.workflow_configuration import WorkflowConfiguration
from app.models.workflow_run import WorkflowRun


def test_workflow_models_are_registered_with_base() -> None:
    """Workflow logging tables should be available to Alembic metadata."""

    expected_models = {
        Workflow: "workflows",
        WorkflowConfiguration: "workflow_configurations",
        WorkflowRun: "workflow_runs",
        ModelCall: "model_calls",
        ToolCall: "tool_calls",
    }

    assert {
        model.__tablename__ for model in expected_models
    } <= set(Base.metadata.tables)
    for model, table_name in expected_models.items():
        assert model.__table__ is Base.metadata.tables[table_name]
