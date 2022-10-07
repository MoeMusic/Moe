"""new field: label.

Revision ID: 817440447857
Revises: 30668259fcd6
Create Date: 2022-10-06 20:39:23.733361

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "817440447857"
down_revision = "30668259fcd6"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.add_column(sa.Column("label", sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.drop_column("label")
