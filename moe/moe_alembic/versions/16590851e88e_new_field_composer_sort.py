"""new field: composer_sort.

Revision ID: 16590851e88e
Revises: 31e896e9a709
Create Date: 2025-06-15 07:42:32.888489

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "16590851e88e"
down_revision = "31e896e9a709"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.add_column(sa.Column("composer_sort", sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.drop_column("composer_sort")
