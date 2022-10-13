"""new field audio_format.

Revision ID: ab11c34c1d0b
Revises: 0ce5960a081e
Create Date: 2022-10-13 15:55:35.303129

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "ab11c34c1d0b"
down_revision = "0ce5960a081e"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.add_column(sa.Column("audio_format", sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.drop_column("audio_format")
