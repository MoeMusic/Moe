"""Remove file_ext.

Revision ID: 7ea4ddf23121
Revises: b5507b03f9e3
Create Date: 2021-07-10 19:41:10.502542

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "7ea4ddf23121"
down_revision = "b5507b03f9e3"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("track") as batch_op:
        batch_op.drop_column("file_ext")


def downgrade():
    op.add_column(
        "track", sa.Column("file_ext", sa.String(), nullable=False, server_default="")
    )
