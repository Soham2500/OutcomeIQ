"""Unified AI run service for Gemini and OpenAI."""

from decimal import Decimal, InvalidOperation
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.ai_run import AiRun
from app.models.user import User
from app.repositories.project_member_repository import (
    get_project_member,
    list_user_project_memberships,
)
from app.repositories.project_repository import get_project_by_id
from app.schemas.ai_run import AiRunCreate, AiRunListItem, AiRunRead
from app.services.ai.costing import calculate_ai_cost
from app.services.ai.providers.base import AiProviderError, ProviderResult
from app.services.ai.providers.gemini import GeminiProvider
from app.services.ai.providers.openai import OpenAIProvider


ALLOWED_PROVIDERS = {"gemini", "openai"}
PROMPT_PREVIEW_LENGTH = 500
RESPONSE_PREVIEW_LENGTH = 1000


class AiRunValidationError(ValueError):
    """Raised when an AI run request is invalid or unauthorized."""


def _preview(value: str, max_length: int) -> str:
    cleaned = " ".join(value.strip().split())
    return cleaned[:max_length]


def _usd_to_inr_rate() -> Decimal:
    settings = get_settings()
    try:
        return Decimal(str(settings.USD_TO_INR_RATE))
    except (InvalidOperation, ValueError) as exc:
        raise AiRunValidationError("USD_TO_INR_RATE must be a valid decimal.") from exc


def _normalize_provider(provider: str | None) -> str:
    settings = get_settings()
    selected = (provider or settings.DEFAULT_AI_PROVIDER or "gemini").strip().lower()
    if selected not in ALLOWED_PROVIDERS:
        raise AiRunValidationError("Provider must be either gemini or openai.")
    return selected


def _select_model(provider: str, model: str | None) -> str:
    settings = get_settings()
    if model and model.strip():
        return model.strip()
    if provider == "gemini":
        return (
            settings.DEFAULT_GEMINI_MODEL
            or settings.DEFAULT_AI_MODEL
            or "gemini-3.5-flash"
        )
    return settings.DEFAULT_OPENAI_MODEL or settings.DEFAULT_AI_MODEL or "gpt-4o-mini"


def _provider(provider: str):
    if provider == "gemini":
        return GeminiProvider()
    if provider == "openai":
        return OpenAIProvider()
    raise AiRunValidationError("Provider must be either gemini or openai.")


def _empty_failed_result(provider: str, model: str) -> ProviderResult:
    return ProviderResult(
        provider=provider,
        model=model,
        response_text="",
        input_tokens=0,
        output_tokens=0,
        total_tokens=0,
        raw_usage={},
        latency_ms=0,
    )


def _to_read(run: AiRun, response_text: str | None = None) -> AiRunRead:
    return AiRunRead(
        id=run.id,
        project_id=run.project_id,
        workflow_name=run.workflow_name,
        provider=run.provider,
        model=run.model,
        response_text=response_text,
        prompt_preview=run.prompt_preview,
        response_preview=run.response_preview,
        status=run.status,
        error_message=run.error_message,
        input_tokens=run.input_tokens,
        output_tokens=run.output_tokens,
        total_tokens=run.total_tokens,
        cost_usd=run.cost_usd,
        cost_inr=run.cost_inr,
        currency=run.currency,
        pricing_unknown=run.pricing_unknown,
        latency_ms=run.latency_ms,
        created_at=run.created_at,
    )


def create_ai_run(
    db: Session,
    request: AiRunCreate,
    current_user: User,
) -> AiRunRead:
    if get_project_by_id(db, request.project_id) is None:
        raise AiRunValidationError("Project not found.")
    if get_project_member(db, request.project_id, current_user.id) is None:
        raise PermissionError("Project membership is required.")

    provider = _normalize_provider(request.provider)
    model = _select_model(provider, request.model)
    result = _empty_failed_result(provider, model)
    status = "succeeded"
    safe_error = None

    try:
        result = _provider(provider).run(request.prompt, model)
    except AiProviderError as exc:
        status = "failed"
        safe_error = str(exc)

    ai_cost = calculate_ai_cost(
        provider=provider,
        model=model,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        usd_to_inr_rate=_usd_to_inr_rate(),
    )
    run = AiRun(
        user_id=current_user.id,
        project_id=request.project_id,
        workflow_name=request.workflow_name,
        provider=provider,
        model=model,
        prompt_preview=_preview(request.prompt, PROMPT_PREVIEW_LENGTH),
        response_preview=(
            _preview(result.response_text, RESPONSE_PREVIEW_LENGTH)
            if result.response_text
            else None
        ),
        status=status,
        error_message=safe_error,
        latency_ms=result.latency_ms,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        total_tokens=result.total_tokens,
        cost_usd=ai_cost.cost_usd,
        cost_inr=ai_cost.cost_inr,
        currency=get_settings().COST_CURRENCY,
        pricing_unknown=ai_cost.pricing_unknown,
        raw_usage_json=result.raw_usage,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return _to_read(run, response_text=result.response_text if status == "succeeded" else None)


def list_ai_runs(
    db: Session,
    current_user: User,
    project_id: uuid.UUID | None = None,
    limit: int = 50,
) -> list[AiRunListItem]:
    memberships = list_user_project_memberships(db, current_user.id)
    allowed_project_ids = {membership.project_id for membership in memberships}
    if project_id is not None:
        if project_id not in allowed_project_ids:
            raise PermissionError("Project membership is required.")
        allowed_project_ids = {project_id}
    if not allowed_project_ids:
        return []

    rows = db.scalars(
        select(AiRun)
        .where(AiRun.project_id.in_(allowed_project_ids))
        .order_by(AiRun.created_at.desc(), AiRun.id.desc())
        .limit(min(max(limit, 1), 100))
    )
    return [AiRunListItem.model_validate(row) for row in rows]
