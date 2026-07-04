"""Import tests for the workflow logging application service."""

from app.services.workflow_logging_service import (
    complete_run,
    create_configuration_for_workflow,
    create_workflow_for_project,
    fail_run,
    get_workflow_run_trace,
    record_model_call,
    record_tool_call,
    start_workflow_run,
)


def test_workflow_service_functions_are_importable() -> None:
    functions = (
        create_workflow_for_project,
        create_configuration_for_workflow,
        start_workflow_run,
        record_model_call,
        record_tool_call,
        complete_run,
        fail_run,
        get_workflow_run_trace,
    )
    assert all(callable(function) for function in functions)
