"""Add composer, composers, and composer_sort fields.

Revision ID: 5e0ebfebadeb
Revises: ab5db9861d30
Create Date: 2025-06-13 23:00:55.350292

"""

import sqlalchemy as sa
from alembic import op

import moe

# revision identifiers, used by Alembic.
revision = "5e0ebfebadeb"
down_revision = "ab5db9861d30"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.add_column(sa.Column("composer", sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column("composers", moe.library.lib_item.SetType(), nullable=True)
        )
        batch_op.add_column(sa.Column("composer_sort", sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.drop_column("composer_sort")
        batch_op.drop_column("composers")
        batch_op.drop_column("composer")
