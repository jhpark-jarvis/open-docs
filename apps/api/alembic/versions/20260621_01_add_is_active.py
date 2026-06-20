"""add is_active to nexon notice events

Revision ID: 20260621_01_add_is_active
Revises: 20260620_01_nexon_notice
Create Date: 2026-06-21 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260621_01_add_is_active"
down_revision = "20260620_01_nexon_notice"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "nexon_notice_events",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column("nexon_notice_events", "is_active")
