"""Database access functions for tool-call telemetry."""

from decimal import Decimal
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tool_call import ToolCall


def create_tool_call(
    db: Session,
    workflow_run_id: uuid.UUID,
    sequence_number: int,
    tool_name: str,
    status: str = "succeeded",
    latency_ms: int | None = None,
    estimated_cost_usd: Decimal | None = None,
    input_summary: str | None = None,
    output_summary: str | None = None,
    error_message: str | None = None,
    metadata_json: dict[str, object] | None = None,
) -> ToolCall:
    tool_call = ToolCall(
        workflow_run_id=workflow_run_id,
        sequence_number=sequence_number,
        tool_name=tool_name,
        status=status,
        latency_ms=latency_ms,
        estimated_cost_usd=estimated_cost_usd,
        input_summary=input_summary,
        output_summary=output_summary,
        error_message=error_message,
        metadata_json=metadata_json,
    )
    db.add(tool_call)
    db.commit()
    db.refresh(tool_call)
    return tool_call


def list_tool_calls(
    db: Session,
    workflow_run_id: uuid.UUID,
) -> list[ToolCall]:
    statement = (
        select(ToolCall)
        .where(ToolCall.workflow_run_id == workflow_run_id)
        .order_by(ToolCall.sequence_number, ToolCall.id)
    )
    return list(db.scalars(statement))
