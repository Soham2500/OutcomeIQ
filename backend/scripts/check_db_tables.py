"""Safely report whether the approved OutcomeIQ core tables exist."""

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


def print_missing_tables(missing_tables: list[str]) -> None:
    """Print a deterministic, secret-free missing-table report."""

    for table_name in missing_tables:
        print(f"{table_name.upper()} TABLE MISSING")


def main() -> int:
    """Inspect table metadata without creating, changing or dropping data."""

    settings = get_settings()
    if not settings.database_configured or db_session.engine is None:
        print_missing_tables(list(CORE_TABLES))
        print("Database is not configured or its engine is unavailable.")
        return 0

    try:
        inspector = inspect(db_session.engine)
        missing_tables = [
            table_name
            for table_name in CORE_TABLES
            if not inspector.has_table(table_name)
        ]
    except Exception:
        print_missing_tables(list(CORE_TABLES))
        print("Database table check could not complete.")
        return 1

    if missing_tables:
        print_missing_tables(missing_tables)
        return 0

    print("ALL CORE TABLES EXIST")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
