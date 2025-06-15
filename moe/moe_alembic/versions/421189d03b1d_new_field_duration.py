"""new field: duration.

Revision ID: 421189d03b1d
Revises: ab5db9861d30
Create Date: 2025-06-15 08:24:02.305917

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "421189d03b1d"
down_revision = "ab5db9861d30"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.add_column(sa.Column("duration", sa.Float(), nullable=True))


def downgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.drop_column("duration")
