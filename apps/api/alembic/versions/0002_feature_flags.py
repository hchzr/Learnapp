"""add feature flags table

Revision ID: 0002_feature_flags
Revises: 0001_initial_placeholder
Create Date: 2026-02-18

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision = "0002_feature_flags"
down_revision = "0001_initial_placeholder"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None

FEATURE_FLAG_NAMES = (
    "notion_sync",
    "todoist_sync",
    "drive_ingestion",
    "anki",
    "exercises",
    "planner",
)


def upgrade() -> None:
    op.create_table(
        "feature_flags",
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("name"),
    )

    feature_flags_table = sa.table(
        "feature_flags",
        sa.column("name", sa.String(length=64)),
        sa.column("enabled", sa.Boolean()),
    )
    op.bulk_insert(
        feature_flags_table,
        [{"name": name, "enabled": False} for name in FEATURE_FLAG_NAMES],
    )


def downgrade() -> None:
    op.drop_table("feature_flags")
