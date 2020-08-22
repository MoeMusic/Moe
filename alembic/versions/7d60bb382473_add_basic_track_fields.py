"""Adds basic track fields.

Revision ID: 7d60bb382473
Revises: c55ddce79421
Create Date: 2020-08-19 13:54:00.525214

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "7d60bb382473"
down_revision = "c55ddce79421"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "tracks",
        sa.Column("album", sa.String(), nullable=False, server_default="og_album"),
    )
    op.add_column(
        "tracks",
        sa.Column(
            "album_artist",
            sa.String(),
            nullable=False,
            server_default="og_album_artist",
        ),
    )
    op.add_column(
        "tracks",
        sa.Column("artist", sa.String(), nullable=False, server_default="og_artist"),
    )


def downgrade():
    op.drop_column("tracks", "artist")
    op.drop_column("tracks", "album_artist")
    op.drop_column("tracks", "album")
