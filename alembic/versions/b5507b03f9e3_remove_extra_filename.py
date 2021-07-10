"""Remove extra filename and rename `_path` to `path`.

Revision ID: b5507b03f9e3
Revises: 10f2c1aedd13
Create Date: 2021-07-10 11:11:45.762003

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "b5507b03f9e3"
down_revision = "10f2c1aedd13"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("extras") as batch_op:
        batch_op.alter_column("_path", new_column_name="path")
        batch_op.drop_column("_filename")


def downgrade():
    with op.batch_alter_table("extras") as batch_op:
        batch_op.alter_column("path", new_column_name="_path")
        batch_op.add_column("extras", sa.Column("_filename", sa.String, nullable=False))
