"""Safely report whether all required OutcomeIQ tables exist."""

from sqlalchemy import inspect

from app.core.config import get_settings
from app.db import session as db_session


CORE_TABLES = (
    "system_metadata",
    "users",
    "organizations",
    "projects",
    "project_members",
    "audit_events",
)

WORKFLOW_TABLES = (
    "workflows",
    "workflow_configurations",
    "workflow_runs",
    "model_calls",
    "tool_calls",
)

COST_TABLES = (
    "model_pricing_rates",
    "workflow_run_costs",
)

OUTCOME_TABLES = (
    "outcome_contracts",
    "workflow_run_outcomes",
)

RECOMMENDATION_TABLES = (
    "recommendations",
)

REQUIRED_TABLES = (
    CORE_TABLES
    + WORKFLOW_TABLES
    + COST_TABLES
    + OUTCOME_TABLES
    + RECOMMENDATION_TABLES
)


def print_missing_tables(missing_tables: list[str]) -> None:
    """Print a deterministic, secret-free missing-table report."""

    for table_name in missing_tables:
        print(f"{table_name.upper()} TABLE MISSING")


def main() -> int:
    """Inspect table metadata without creating, changing or dropping data."""

    settings = get_settings()
    if not settings.database_configured or db_session.engine is None:
        print_missing_tables(list(REQUIRED_TABLES))
        print("Database is not configured or its engine is unavailable.")
        return 0

    try:
        inspector = inspect(db_session.engine)
        missing_tables = [
            table_name
            for table_name in REQUIRED_TABLES
            if not inspector.has_table(table_name)
        ]
    except Exception:
        print_missing_tables(list(REQUIRED_TABLES))
        print("Database table check could not complete.")
        return 1

    if missing_tables:
        print_missing_tables(missing_tables)
        return 0

    print("ALL REQUIRED TABLES EXIST")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
