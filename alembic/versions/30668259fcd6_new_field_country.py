"""new field: country.

Revision ID: 30668259fcd6
Revises: 60608d9d2908
Create Date: 2022-10-06 20:35:34.296797

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "30668259fcd6"
down_revision = "60608d9d2908"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.add_column(sa.Column("country", sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.drop_column("country")
