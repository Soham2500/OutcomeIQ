"""Placeholder for the future SQLAlchemy database session setup.

Day 1 intentionally does not create an engine, open a PostgreSQL connection,
or create database tables. The engine and session factory will be configured
on Day 3 after the SQLAlchemy model and migration approach is introduced.
"""

from typing import Final


DATABASE_SESSION_CONFIGURED: Final[bool] = False


def get_db_session() -> None:
    """Fail clearly if a future endpoint uses the database too early."""

    raise RuntimeError("Database sessions are not configured yet; planned for Day 3.")
