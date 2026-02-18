"""initial placeholder migration

Revision ID: 0001_initial_placeholder
Revises:
Create Date: 2026-02-18

"""

from typing import Sequence

revision = "0001_initial_placeholder"
down_revision = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    """No-op initial migration for scaffolding."""


def downgrade() -> None:
    """No-op downgrade for scaffolding."""
