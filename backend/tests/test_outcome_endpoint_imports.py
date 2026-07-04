"""Import tests for protected outcome endpoints."""

from app.api.v1.endpoints import outcomes


def test_outcome_endpoint_functions_are_importable() -> None:
    functions = (
        outcomes.create_outcome_contract_endpoint,
        outcomes.list_outcome_contracts_endpoint,
        outcomes.get_outcome_contract_endpoint,
        outcomes.update_outcome_contract_endpoint,
        outcomes.record_workflow_run_outcome_endpoint,
        outcomes.get_workflow_run_outcome_endpoint,
        outcomes.get_cost_per_successful_outcome_endpoint,
    )
    assert all(callable(function) for function in functions)
