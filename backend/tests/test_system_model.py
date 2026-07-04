"""Tests for the first infrastructure-only SQLAlchemy model."""

from sqlalchemy import UniqueConstraint

from app.db.base import Base
from app.models.system import SystemMetadata


def test_system_metadata_is_registered_with_base() -> None:
    """The model should be importable and visible to Alembic metadata."""

    assert SystemMetadata.__tablename__ == "system_metadata"
    assert "system_metadata" in Base.metadata.tables

    table = Base.metadata.tables["system_metadata"]
    assert set(table.columns.keys()) == {
        "id",
        "key",
        "value",
        "description",
        "created_at",
        "updated_at",
    }
    assert table.c.id.primary_key
    assert not table.c.key.nullable
    assert table.c.value.nullable
    assert table.c.description.nullable
    assert any(
        isinstance(constraint, UniqueConstraint)
        and constraint.name == "uq_system_metadata_key"
        for constraint in table.constraints
    )
