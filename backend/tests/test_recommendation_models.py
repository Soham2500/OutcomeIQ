"""Metadata-registration tests for recommendation storage."""

from app.db.base import Base
from app.models.recommendation import Recommendation


def test_recommendation_model_is_registered_with_base() -> None:
    assert "recommendations" in Base.metadata.tables
    assert Recommendation.__table__ is Base.metadata.tables["recommendations"]
