"""Shared SQLAlchemy declarative base and registered model metadata."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for OutcomeIQ SQLAlchemy models."""


# Import only the approved infrastructure and core identity/project models so
# Alembic can discover them. Workflow, cost and outcome models remain deferred.
import app.models.system  # noqa: E402, F401
import app.models.user  # noqa: E402, F401
import app.models.organization  # noqa: E402, F401
import app.models.project  # noqa: E402, F401
import app.models.project_member  # noqa: E402, F401
import app.models.audit_event  # noqa: E402, F401
