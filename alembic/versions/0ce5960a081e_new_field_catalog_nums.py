"""new field catalog_nums.

Revision ID: 0ce5960a081e
Revises: 32e9fea590b7
Create Date: 2022-10-12 16:13:33.297005

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0ce5960a081e"
down_revision = "32e9fea590b7"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "catalog_num",
        sa.Column("_id", sa.Integer(), nullable=False),
        sa.Column("_album_id", sa.Integer(), nullable=True),
        sa.Column("catalog_num", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["_album_id"],
            ["album._id"],
        ),
        sa.PrimaryKeyConstraint("_id"),
    )


def downgrade():
    op.drop_table("catalog_num")
