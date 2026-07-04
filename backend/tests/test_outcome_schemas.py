"""Validation tests for outcome tracking schemas."""

from decimal import Decimal
import uuid

from app.models.enums import WorkflowOutcomeStatus
from app.schemas.outcome_contract import (
    OutcomeContractCreate,
    OutcomeContractRead,
    OutcomeContractUpdate,
)
from app.schemas.outcome_metrics import CostPerSuccessfulOutcomeRead
from app.schemas.workflow_run_outcome import (
    WorkflowRunOutcomeCreate,
    WorkflowRunOutcomeRead,
    WorkflowRunOutcomeUpdate,
)


def test_outcome_schemas_accept_safe_business_evidence() -> None:
    contract = OutcomeContractCreate(
        project_id=uuid.uuid4(),
        name="Ticket resolution",
        success_criteria_json={"not_reopened_within_hours": 48},
    )
    outcome = WorkflowRunOutcomeCreate(status=WorkflowOutcomeStatus.SUCCEEDED)
    metrics = CostPerSuccessfulOutcomeRead(
        total_runs=4,
        successful_runs=2,
        failed_runs=1,
        pending_runs=1,
        total_cost_usd=Decimal("1.20000000"),
        cost_per_successful_outcome_usd=Decimal("0.60000000"),
        success_rate=Decimal("0.50000000"),
    )

    assert contract.success_window_hours == 48
    assert outcome.verification_source.value == "manual"
    assert metrics.cost_per_successful_outcome_usd == Decimal("0.60000000")
    assert OutcomeContractRead.model_config["from_attributes"] is True
    assert WorkflowRunOutcomeRead.model_config["from_attributes"] is True
    assert OutcomeContractUpdate(name="Updated").name == "Updated"
    assert WorkflowRunOutcomeUpdate(status="pending").status is not None
