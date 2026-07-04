"""Import and deterministic calculation tests for the outcome service."""

from decimal import Decimal
from types import SimpleNamespace
import uuid

from app.services import outcome_service


def test_outcome_service_functions_are_importable() -> None:
    functions = (
        outcome_service.create_contract,
        outcome_service.record_workflow_run_outcome,
        outcome_service.get_workflow_run_outcome,
        outcome_service.calculate_cost_per_successful_outcome,
    )
    assert all(callable(function) for function in functions)


def test_cost_per_successful_outcome_is_deterministic(monkeypatch) -> None:
    run_ids = [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
    runs = [SimpleNamespace(id=run_id) for run_id in run_ids]

    class FakeSession:
        def scalars(self, _statement):
            return iter(runs)

    costs = {
        run_ids[0]: SimpleNamespace(total_cost_usd=Decimal("0.40")),
        run_ids[1]: SimpleNamespace(total_cost_usd=Decimal("0.30")),
    }
    outcomes = {
        run_ids[0]: SimpleNamespace(status="succeeded"),
        run_ids[1]: SimpleNamespace(status="failed"),
        run_ids[2]: None,
    }
    monkeypatch.setattr(
        outcome_service,
        "get_cost_by_workflow_run_id",
        lambda _db, run_id: costs.get(run_id),
    )
    monkeypatch.setattr(
        outcome_service,
        "get_outcome_by_workflow_run_id",
        lambda _db, run_id: outcomes[run_id],
    )

    metrics = outcome_service.calculate_cost_per_successful_outcome(
        FakeSession(),
    )

    assert metrics.total_runs == 3
    assert metrics.successful_runs == 1
    assert metrics.failed_runs == 1
    assert metrics.pending_runs == 1
    assert metrics.total_cost_usd == Decimal("0.70000000")
    assert metrics.cost_per_successful_outcome_usd == Decimal("0.70000000")
    assert metrics.success_rate == Decimal("0.33333333")
    assert "no cost summary" in (metrics.notes or "")
