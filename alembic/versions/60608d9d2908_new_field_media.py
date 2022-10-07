"""new field: media.

Revision ID: 60608d9d2908
Revises: fe0956c93730
Create Date: 2022-10-06 20:26:02.640360

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "60608d9d2908"
down_revision = "fe0956c93730"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.add_column(sa.Column("media", sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.drop_column("media")
