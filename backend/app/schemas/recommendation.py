"""Pydantic schemas for rule-based recommendations."""

from datetime import datetime
from decimal import Decimal
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import (
    RecommendationSeverity,
    RecommendationStatus,
    RecommendationType,
)


class RecommendationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    workflow_id: uuid.UUID | None
    recommendation_type: RecommendationType
    severity: RecommendationSeverity
    status: RecommendationStatus
    title: str
    description: str | None
    current_metric_json: dict[str, object] | None
    suggested_action_json: dict[str, object] | None
    potential_savings_usd: Decimal | None
    confidence_score: Decimal | None
    generated_at: datetime | None
    accepted_at: datetime | None
    dismissed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class RecommendationGenerateRequest(BaseModel):
    project_id: uuid.UUID
    workflow_id: uuid.UUID | None = None


class RecommendationGenerateResponse(BaseModel):
    project_id: uuid.UUID
    workflow_id: uuid.UUID | None = None
    generated_count: int = Field(ge=0)
    recommendations: list[RecommendationRead]


class RecommendationUpdate(BaseModel):
    status: RecommendationStatus | None = None
    accepted_at: datetime | None = None
    dismissed_at: datetime | None = None
