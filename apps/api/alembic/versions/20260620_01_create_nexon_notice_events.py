"""create nexon notice events table

Revision ID: 20260620_01_nexon_notice
Revises: 
Create Date: 2026-06-20 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260620_01_nexon_notice"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "nexon_notice_events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("notice_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("url", sa.String(length=1024), nullable=False),
        sa.Column("notice_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("event_start_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("event_end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("contents", sa.Text(), nullable=True),
        sa.Column("raw_payload", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_nexon_notice_events_notice_id"),
        "nexon_notice_events",
        ["notice_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_nexon_notice_events_notice_id"), table_name="nexon_notice_events")
    op.drop_table("nexon_notice_events")
