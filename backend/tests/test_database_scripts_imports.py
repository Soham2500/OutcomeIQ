"""Import-safety tests for read-only database diagnostic scripts."""

from app.db import health as database_health
from scripts import inspect_db_schema, validate_alembic_state


def test_database_diagnostic_modules_are_importable_without_execution() -> None:
    assert callable(database_health.check_database_connection)
    assert callable(inspect_db_schema.main)
    assert callable(validate_alembic_state.main)
    assert callable(validate_alembic_state.validate_alembic_state)
    assert inspect_db_schema.KNOWN_CORE_TABLES == (
        "system_metadata",
        "users",
        "organizations",
        "projects",
        "project_members",
        "audit_events",
    )
