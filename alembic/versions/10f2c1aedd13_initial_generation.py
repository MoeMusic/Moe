"""Initial generation.

Revision ID: 10f2c1aedd13
Revises:
Create Date: 2021-06-27 19:39:21.312631

"""
import sqlalchemy as sa

import moe
from alembic import op

# revision identifiers, used by Alembic.
revision = "10f2c1aedd13"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "album",
        sa.Column("_id", sa.Integer(), nullable=False),
        sa.Column("artist", sa.String(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("disc_total", sa.Integer(), nullable=False),
        sa.Column("mb_album_id", sa.String(), nullable=False),
        sa.Column("path", moe.core.library.lib_item.PathType(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("_id"),
        sa.UniqueConstraint("artist", "title", "date"),
        sa.UniqueConstraint("path"),
    )
    op.create_table(
        "genre",
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )
    op.create_table(
        "extras",
        sa.Column("_id", sa.Integer(), nullable=False),
        sa.Column("_filename", sa.String(), nullable=False),
        sa.Column("_path", moe.core.library.lib_item.PathType(), nullable=False),
        sa.Column("_album_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["_album_id"],
            ["album._id"],
        ),
        sa.PrimaryKeyConstraint("_id"),
        sa.UniqueConstraint("_filename", "_album_id"),
        sa.UniqueConstraint("_path"),
    )
    op.create_table(
        "track",
        sa.Column("_id", sa.Integer(), nullable=False),
        sa.Column("artist", sa.String(), nullable=False),
        sa.Column("disc", sa.Integer(), nullable=False),
        sa.Column("file_ext", sa.String(), nullable=False),
        sa.Column("mb_track_id", sa.String(), nullable=False),
        sa.Column("path", moe.core.library.lib_item.PathType(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("track_num", sa.Integer(), nullable=False),
        sa.Column("_album_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["_album_id"],
            ["album._id"],
        ),
        sa.PrimaryKeyConstraint("_id"),
        sa.UniqueConstraint("disc", "track_num", "_album_id"),
        sa.UniqueConstraint("path"),
    )
    op.create_table(
        "track_genre",
        sa.Column("genre", sa.String(), nullable=True),
        sa.Column("track_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["genre"],
            ["genre.name"],
        ),
        sa.ForeignKeyConstraint(
            ["track_id"],
            ["track._id"],
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("track_genre")
    op.drop_table("track")
    op.drop_table("extras")
    op.drop_table("genre")
    op.drop_table("album")
    # ### end Alembic commands ###