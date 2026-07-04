"""Shared SQLAlchemy declarative base and registered model metadata."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for OutcomeIQ SQLAlchemy models."""


# Import only the approved infrastructure model so Alembic can discover it.
# Future business models must be reviewed before they are registered here.
import app.models.system  # noqa: E402, F401
