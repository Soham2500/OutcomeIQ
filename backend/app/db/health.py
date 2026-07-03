"""Safe database connectivity checks for readiness and local diagnostics."""

import logging

from sqlalchemy import text

from app.core.config import get_settings
from app.db import session as db_session


logger = logging.getLogger(__name__)
settings = get_settings()


def check_database_connection() -> dict[str, str]:
    """Return a safe database status without exposing connection details."""

    if not settings.database_configured:
        return {"status": "not_configured"}

    if db_session.engine is None:
        return {
            "status": "error",
            "message": db_session.engine_initialization_error
            or "Database engine is unavailable.",
        }

    try:
        with db_session.engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar_one()

        if result == 1:
            return {"status": "connected"}

        return {
            "status": "error",
            "message": "Database connection check returned an unexpected result.",
        }
    except Exception as exc:
        logger.warning(
            "Database connection check failed (%s)",
            type(exc).__name__,
        )
        return {
            "status": "error",
            "message": "Database connection check failed.",
        }
