"""Database access functions for model-call telemetry."""

from decimal import Decimal
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.model_call import ModelCall


def create_model_call(
    db: Session,
    workflow_run_id: uuid.UUID,
    sequence_number: int,
    provider: str,
    model_name: str,
    call_type: str | None = None,
    status: str = "succeeded",
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    total_tokens: int = 0,
    latency_ms: int | None = None,
    estimated_cost_usd: Decimal | None = None,
    is_retry: bool = False,
    is_fallback: bool = False,
    request_summary: str | None = None,
    response_summary: str | None = None,
    error_message: str | None = None,
    metadata_json: dict[str, object] | None = None,
) -> ModelCall:
    model_call = ModelCall(
        workflow_run_id=workflow_run_id,
        sequence_number=sequence_number,
        provider=provider,
        model_name=model_name,
        call_type=call_type,
        status=status,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        latency_ms=latency_ms,
        estimated_cost_usd=estimated_cost_usd,
        is_retry=is_retry,
        is_fallback=is_fallback,
        request_summary=request_summary,
        response_summary=response_summary,
        error_message=error_message,
        metadata_json=metadata_json,
    )
    db.add(model_call)
    db.commit()
    db.refresh(model_call)
    return model_call


def list_model_calls(
    db: Session,
    workflow_run_id: uuid.UUID,
) -> list[ModelCall]:
    statement = (
        select(ModelCall)
        .where(ModelCall.workflow_run_id == workflow_run_id)
        .order_by(ModelCall.sequence_number, ModelCall.id)
    )
    return list(db.scalars(statement))
