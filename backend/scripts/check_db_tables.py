"""Safely report whether the system_metadata table exists."""

from sqlalchemy import inspect

from app.core.config import get_settings
from app.db import session as db_session


def main() -> int:
    """Inspect table metadata without creating, changing or dropping data."""

    settings = get_settings()
    if not settings.database_configured or db_session.engine is None:
        print("SYSTEM_METADATA TABLE MISSING")
        print("Database is not configured or its engine is unavailable.")
        return 0

    try:
        exists = inspect(db_session.engine).has_table("system_metadata")
    except Exception:
        print("SYSTEM_METADATA TABLE MISSING")
        print("Database table check could not complete.")
        return 1

    if exists:
        print("SYSTEM_METADATA TABLE EXISTS")
    else:
        print("SYSTEM_METADATA TABLE MISSING")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
