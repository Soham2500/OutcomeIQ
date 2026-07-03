"""SQLAlchemy engine and request-session foundation.

The engine and session factory are created only when DATABASE_URL is present.
SQLAlchemy engine construction is lazy with respect to network I/O: it does
not connect to PostgreSQL during module import. Tables are never created here.
"""

from collections.abc import Generator
import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


logger = logging.getLogger(__name__)
settings = get_settings()

engine: Engine | None = None
SessionLocal: sessionmaker[Session] | None = None
engine_initialization_error: str | None = None

if settings.database_configured:
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
        )
        SessionLocal = sessionmaker(
            bind=engine,
            autoflush=False,
            expire_on_commit=False,
        )
    except Exception as exc:  # Configuration errors must not leak the URL.
        engine_initialization_error = "Database engine initialization failed."
        logger.warning(
            "Database engine initialization failed (%s)",
            type(exc).__name__,
        )


def get_db() -> Generator[Session, None, None]:
    """Yield one SQLAlchemy session and always close it safely.

    This dependency will be used by database-backed FastAPI routes from Day 3
    onward. It does not commit automatically and it never creates tables.
    """

    if SessionLocal is None:
        raise RuntimeError(
            "Database is not configured. Set DATABASE_URL in backend/.env."
        )

    database_session = SessionLocal()
    try:
        yield database_session
    except Exception:
        database_session.rollback()
        raise
    finally:
        database_session.close()
