"""Database access functions for rule-based recommendations."""

from datetime import datetime, timezone
from decimal import Decimal
import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.enums import RecommendationStatus
from app.models.recommendation import Recommendation


UPDATABLE_FIELDS = {"status", "accepted_at", "dismissed_at"}


def create_recommendation(
    db: Session,
    project_id: uuid.UUID,
    title: str,
    recommendation_type: str,
    severity: str = "medium",
    workflow_id: uuid.UUID | None = None,
    description: str | None = None,
    current_metric_json: dict[str, object] | None = None,
    suggested_action_json: dict[str, object] | None = None,
    potential_savings_usd: Decimal | None = None,
    confidence_score: Decimal | None = None,
) -> Recommendation:
    recommendation = Recommendation(
        project_id=project_id,
        workflow_id=workflow_id,
        recommendation_type=recommendation_type,
        severity=severity,
        title=title,
        description=description,
        current_metric_json=current_metric_json,
        suggested_action_json=suggested_action_json,
        potential_savings_usd=potential_savings_usd,
        confidence_score=confidence_score,
        generated_at=datetime.now(timezone.utc),
    )
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    return recommendation


def list_recommendations(
    db: Session,
    project_id: uuid.UUID | None = None,
    workflow_id: uuid.UUID | None = None,
    status: str | None = None,
    recommendation_type: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Recommendation]:
    statement = select(Recommendation)
    if project_id is not None:
        statement = statement.where(Recommendation.project_id == project_id)
    if workflow_id is not None:
        statement = statement.where(Recommendation.workflow_id == workflow_id)
    if status is not None:
        statement = statement.where(Recommendation.status == status)
    if recommendation_type is not None:
        statement = statement.where(
            Recommendation.recommendation_type == recommendation_type
        )
    statement = (
        statement.order_by(
            Recommendation.generated_at.desc(),
            Recommendation.id.desc(),
        )
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement))


def get_recommendation_by_id(
    db: Session,
    recommendation_id: uuid.UUID,
) -> Recommendation | None:
    return db.get(Recommendation, recommendation_id)


def update_recommendation(
    db: Session,
    recommendation: Recommendation,
    **fields: object,
) -> Recommendation:
    if set(fields) - UPDATABLE_FIELDS:
        raise ValueError("Unsupported recommendation update field.")
    for field_name, value in fields.items():
        setattr(recommendation, field_name, value)
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    return recommendation


def delete_open_recommendations_for_project(
    db: Session,
    project_id: uuid.UUID,
    workflow_id: uuid.UUID | None = None,
) -> int:
    statement = delete(Recommendation).where(
        Recommendation.project_id == project_id,
        Recommendation.status == RecommendationStatus.OPEN.value,
    )
    if workflow_id is None:
        statement = statement.where(Recommendation.workflow_id.is_(None))
    else:
        statement = statement.where(Recommendation.workflow_id == workflow_id)
    result = db.execute(statement)
    db.commit()
    return int(result.rowcount or 0)
