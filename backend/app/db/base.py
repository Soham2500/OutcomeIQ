"""Shared SQLAlchemy declarative base and registered model metadata."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for OutcomeIQ SQLAlchemy models."""


# Import approved models so Alembic can discover their metadata. Recommendation
# and decision models remain deferred to later milestones.
import app.models.system  # noqa: E402, F401
import app.models.user  # noqa: E402, F401
import app.models.organization  # noqa: E402, F401
import app.models.project  # noqa: E402, F401
import app.models.project_member  # noqa: E402, F401
import app.models.audit_event  # noqa: E402, F401
import app.models.workflow  # noqa: E402, F401
import app.models.workflow_configuration  # noqa: E402, F401
import app.models.workflow_run  # noqa: E402, F401
import app.models.model_call  # noqa: E402, F401
import app.models.tool_call  # noqa: E402, F401
import app.models.model_pricing_rate  # noqa: E402, F401
import app.models.workflow_run_cost  # noqa: E402, F401
import app.models.outcome_contract  # noqa: E402, F401
import app.models.workflow_run_outcome  # noqa: E402, F401
import app.models.recommendation  # noqa: E402, F401
import app.models.plan  # noqa: E402, F401
import app.models.subscription  # noqa: E402, F401
import app.models.payment_event  # noqa: E402, F401
import app.models.usage_counter  # noqa: E402, F401
