"""remove audio_format field.

Revision ID: 880c5a2d80ed
Revises: bf49ac6805f7
Create Date: 2022-11-01 13:41:12.407819

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "880c5a2d80ed"
down_revision = "bf49ac6805f7"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.drop_column("audio_format")


def downgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.add_column(sa.Column("audio_format", sa.VARCHAR(), nullable=True))
