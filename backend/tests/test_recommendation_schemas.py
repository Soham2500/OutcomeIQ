"""Validation tests for recommendation schemas."""

from datetime import datetime, timezone
from decimal import Decimal
import uuid

from app.schemas.recommendation import (
    RecommendationGenerateRequest,
    RecommendationGenerateResponse,
    RecommendationRead,
    RecommendationUpdate,
)


def test_recommendation_schemas_accept_rule_based_data() -> None:
    request = RecommendationGenerateRequest(project_id=uuid.uuid4())
    response = RecommendationGenerateResponse(
        project_id=request.project_id,
        generated_count=0,
        recommendations=[],
    )
    update = RecommendationUpdate(status="dismissed")
    now = datetime.now(timezone.utc)
    recommendation = RecommendationRead(
        id=uuid.uuid4(),
        project_id=request.project_id,
        workflow_id=None,
        recommendation_type="cost_per_success_opportunity",
        severity="low",
        status="open",
        title="Track cost per successful outcome for optimization",
        description=None,
        current_metric_json={"successful_outcomes": 1},
        suggested_action_json={"action": "compare_before_scaling"},
        potential_savings_usd=None,
        confidence_score=Decimal("0.7500"),
        generated_at=now,
        accepted_at=None,
        dismissed_at=None,
        created_at=now,
        updated_at=now,
    )

    assert response.generated_count == 0
    assert update.status is not None and update.status.value == "dismissed"
    assert recommendation.confidence_score == Decimal("0.7500")
    assert RecommendationRead.model_config["from_attributes"] is True
