"""Import tests for outcome tracking repositories."""

from app.repositories.outcome_contract_repository import (
    create_outcome_contract,
    get_outcome_contract_by_id,
    get_outcome_contract_by_name,
    list_outcome_contracts,
    update_outcome_contract,
)
from app.repositories.workflow_run_outcome_repository import (
    create_or_update_workflow_run_outcome,
    get_outcome_by_workflow_run_id,
    list_outcomes,
)


def test_outcome_repository_functions_are_importable() -> None:
    functions = (
        create_outcome_contract,
        get_outcome_contract_by_id,
        get_outcome_contract_by_name,
        list_outcome_contracts,
        update_outcome_contract,
        create_or_update_workflow_run_outcome,
        get_outcome_by_workflow_run_id,
        list_outcomes,
    )
    assert all(callable(function) for function in functions)
