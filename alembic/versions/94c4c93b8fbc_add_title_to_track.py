"""Add title to track.

Revision ID: 94c4c93b8fbc
Revises:
Create Date: 2020-08-13 19:28:50.513575

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "94c4c93b8fbc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "tracks",
        sa.Column("title", sa.String(), nullable=False, server_default="og_title"),
    )


def downgrade():
    op.drop_column("tracks", "title")
