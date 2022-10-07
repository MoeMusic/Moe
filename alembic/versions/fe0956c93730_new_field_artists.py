"""new field: artists.

Revision ID: fe0956c93730
Revises: 6d4e785df5cb
Create Date: 2022-10-06 18:26:11.939381

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "fe0956c93730"
down_revision = "6d4e785df5cb"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "artist",
        sa.Column("_id", sa.Integer(), nullable=False),
        sa.Column("_track_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["_track_id"],
            ["track._id"],
        ),
        sa.PrimaryKeyConstraint("_id"),
    )


def downgrade():
    op.drop_table("artist")
