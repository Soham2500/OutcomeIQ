"""Import tests for workflow logging repositories."""

from app.repositories.model_call_repository import (
    create_model_call,
    list_model_calls,
)
from app.repositories.tool_call_repository import (
    create_tool_call,
    list_tool_calls,
)
from app.repositories.workflow_configuration_repository import (
    create_workflow_configuration,
    get_configuration_by_id,
    get_configuration_by_version,
    list_configurations,
    update_configuration,
)
from app.repositories.workflow_repository import (
    create_workflow,
    get_workflow_by_id,
    get_workflow_by_slug,
    list_workflows,
    update_workflow,
)
from app.repositories.workflow_run_repository import (
    complete_workflow_run,
    create_workflow_run,
    fail_workflow_run,
    get_workflow_run_by_id,
    list_workflow_runs,
    mark_workflow_run_running,
)


def test_workflow_repository_functions_are_importable() -> None:
    functions = (
        create_workflow,
        get_workflow_by_id,
        get_workflow_by_slug,
        list_workflows,
        update_workflow,
        create_workflow_configuration,
        get_configuration_by_id,
        get_configuration_by_version,
        list_configurations,
        update_configuration,
        create_workflow_run,
        get_workflow_run_by_id,
        list_workflow_runs,
        mark_workflow_run_running,
        complete_workflow_run,
        fail_workflow_run,
        create_model_call,
        list_model_calls,
        create_tool_call,
        list_tool_calls,
    )
    assert all(callable(function) for function in functions)
