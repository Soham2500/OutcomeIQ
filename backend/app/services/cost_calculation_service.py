"""Deterministic cost calculation from recorded workflow telemetry."""

from decimal import Decimal, ROUND_HALF_UP
import uuid

from sqlalchemy.orm import Session

from app.models.enums import CostCalculationStatus
from app.models.model_call import ModelCall
from app.models.workflow_run_cost import WorkflowRunCost
from app.repositories.model_call_repository import list_model_calls
from app.repositories.model_pricing_rate_repository import get_active_rate
from app.repositories.tool_call_repository import list_tool_calls
from app.repositories.workflow_run_cost_repository import upsert_workflow_run_cost
from app.repositories.workflow_run_repository import get_workflow_run_by_id


TOKENS_PER_THOUSAND = Decimal("1000")
MONEY_QUANTUM = Decimal("0.00000001")


def _money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def calculate_model_call_cost(
    db: Session,
    model_call: ModelCall,
) -> dict[str, object]:
    """Calculate one call using a configured rate or recorded estimate."""

    rate = get_active_rate(
        db,
        provider=model_call.provider,
        model_name=model_call.model_name,
        currency="USD",
    )
    if rate is not None:
        prompt_cost = (
            Decimal(model_call.prompt_tokens)
            / TOKENS_PER_THOUSAND
            * rate.input_token_price_per_1k
        )
        completion_cost = (
            Decimal(model_call.completion_tokens)
            / TOKENS_PER_THOUSAND
            * rate.output_token_price_per_1k
        )
        return {
            "cost_usd": _money(prompt_cost + completion_cost),
            "status": CostCalculationStatus.CALCULATED.value,
            "source": "pricing_rate",
            "note": None,
        }

    if model_call.estimated_cost_usd is not None:
        return {
            "cost_usd": _money(Decimal(str(model_call.estimated_cost_usd))),
            "status": CostCalculationStatus.PARTIAL.value,
            "source": "model_call_estimate",
            "note": (
                f"missing_rate:{model_call.provider}/{model_call.model_name};"
                "used_recorded_estimate"
            ),
        }

    return {
        "cost_usd": Decimal("0.00000000"),
        "status": CostCalculationStatus.PARTIAL.value,
        "source": "missing",
        "note": (
            f"missing_rate:{model_call.provider}/{model_call.model_name};"
            "missing_estimate"
        ),
    }


def calculate_workflow_run_cost(
    db: Session,
    workflow_run_id: uuid.UUID,
) -> WorkflowRunCost:
    """Calculate and persist one workflow run's current cost summary."""

    workflow_run = get_workflow_run_by_id(db, workflow_run_id)
    if workflow_run is None:
        raise LookupError("Workflow run not found.")

    model_calls = list_model_calls(db, workflow_run_id)
    tool_calls = list_tool_calls(db, workflow_run_id)
    prompt_tokens = sum(call.prompt_tokens for call in model_calls)
    completion_tokens = sum(call.completion_tokens for call in model_calls)
    total_tokens = sum(call.total_tokens for call in model_calls)

    model_cost = Decimal("0")
    tool_cost = Decimal("0")
    notes: list[str] = []

    for model_call in model_calls:
        result = calculate_model_call_cost(db, model_call)
        cost_value = result["cost_usd"]
        if not isinstance(cost_value, Decimal):
            raise TypeError("Model cost calculation returned a non-Decimal value.")
        model_cost += cost_value
        if result["status"] == CostCalculationStatus.PARTIAL.value:
            note = result["note"]
            if isinstance(note, str):
                notes.append(note)

    for tool_call in tool_calls:
        if tool_call.estimated_cost_usd is None:
            notes.append(f"missing_tool_estimate:{tool_call.tool_name}")
            continue
        tool_cost += Decimal(str(tool_call.estimated_cost_usd))

    model_cost = _money(model_cost)
    tool_cost = _money(tool_cost)
    total_cost = _money(model_cost + tool_cost)
    calculation_status = (
        CostCalculationStatus.PARTIAL.value
        if notes
        else CostCalculationStatus.CALCULATED.value
    )

    return upsert_workflow_run_cost(
        db,
        workflow_run_id=workflow_run_id,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        model_call_count=len(model_calls),
        tool_call_count=len(tool_calls),
        model_cost_usd=model_cost,
        tool_cost_usd=tool_cost,
        total_cost_usd=total_cost,
        currency="USD",
        calculation_status=calculation_status,
        calculation_notes="; ".join(notes) if notes else None,
    )
