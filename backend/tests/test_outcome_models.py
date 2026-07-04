"""Metadata-registration tests for outcome tracking models."""

from app.db.base import Base
from app.models.outcome_contract import OutcomeContract
from app.models.workflow_run_outcome import WorkflowRunOutcome


def test_outcome_models_are_registered_with_base() -> None:
    expected_models = {
        OutcomeContract: "outcome_contracts",
        WorkflowRunOutcome: "workflow_run_outcomes",
    }

    assert {
        model.__tablename__ for model in expected_models
    } <= set(Base.metadata.tables)
    for model, table_name in expected_models.items():
        assert model.__table__ is Base.metadata.tables[table_name]
