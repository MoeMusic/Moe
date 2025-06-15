"""new field: composer.

Revision ID: 31e896e9a709
Revises: ab5db9861d30
Create Date: 2025-06-15 07:32:44.896247

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "31e896e9a709"
down_revision = "ab5db9861d30"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.add_column(sa.Column("composer", sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.drop_column("composer")
