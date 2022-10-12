"""new field track_total.

Revision ID: 32e9fea590b7
Revises: eb8c7e20a080
Create Date: 2022-10-12 13:59:57.620933

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "32e9fea590b7"
down_revision = "eb8c7e20a080"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.add_column(sa.Column("track_total", sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.drop_column("track_total")
