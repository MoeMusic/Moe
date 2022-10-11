"""new field barcode.

Revision ID: eb8c7e20a080
Revises: db3a470892c6
Create Date: 2022-10-11 14:51:44.788096

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "eb8c7e20a080"
down_revision = "db3a470892c6"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.add_column(sa.Column("barcode", sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.drop_column("barcode")
