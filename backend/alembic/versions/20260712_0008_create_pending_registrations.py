"""Create pending registration OTP table.

Revision ID: 0008_pending_registrations
Revises: 0007_billing
Create Date: 2026-07-12
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0008_pending_registrations"
down_revision: str | None = "0007_billing"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create table for email OTP registrations pending verification."""

    op.create_table(
        "pending_registrations",
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("full_name", sa.String(length=160), nullable=True),
        sa.Column("hashed_password", sa.Text(), nullable=False),
        sa.Column("hashed_otp", sa.Text(), nullable=False),
        sa.Column("otp_expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "otp_attempts",
            sa.Integer(),
            server_default="0",
            nullable=False,
        ),
        sa.Column("last_sent_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_pending_registrations_email",
        "pending_registrations",
        ["email"],
        unique=True,
    )
    op.create_index(
        "ix_pending_registrations_otp_expires_at",
        "pending_registrations",
        ["otp_expires_at"],
        unique=False,
    )


def downgrade() -> None:
    """Drop pending registration OTP table."""

    op.drop_table("pending_registrations")
