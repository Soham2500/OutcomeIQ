"""Infrastructure-only SQLAlchemy models."""

from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class SystemMetadata(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Store safe internal metadata used to validate database migrations."""

    __tablename__ = "system_metadata"
    __table_args__ = (
        UniqueConstraint("key", name="uq_system_metadata_key"),
    )

    key: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
