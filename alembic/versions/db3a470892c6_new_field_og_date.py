"""new field: og_date.

Revision ID: db3a470892c6
Revises: 817440447857
Create Date: 2022-10-08 06:20:42.841502

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "db3a470892c6"
down_revision = "817440447857"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.add_column(sa.Column("original_date", sa.Date(), nullable=True))


def downgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.drop_column("original_date")
