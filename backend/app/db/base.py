"""Shared SQLAlchemy declarative base for OutcomeIQ."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all future OutcomeIQ SQLAlchemy models."""


# Business model modules will be imported here later so Alembic can discover
# their metadata. Day 3 Prompt 1 intentionally defines no domain models.
