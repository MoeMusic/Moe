"""Rename album_artist to albumartist.

It seems albumartist as one word is more common.

Revision ID: 883cc62bc334
Revises: 7d60bb382473
Create Date: 2020-08-21 18:04:01.010695

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "883cc62bc334"
down_revision = "7d60bb382473"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("tracks", "album_artist", new_column_name="albumartist")


def downgrade():
    op.alter_column("tracks", "albumartist", new_column_name="album_artist")
