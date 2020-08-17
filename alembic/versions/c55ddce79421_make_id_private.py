"""Make id private.

This also helps deconflict with the python builtin `id()`

Revision ID: c55ddce79421
Revises: 94c4c93b8fbc
Create Date: 2020-08-16 11:10:28.135894

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "c55ddce79421"
down_revision = "94c4c93b8fbc"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("tracks", "id", new_column_name="_id")


def downgrade():
    op.alter_column("tracks", "_id", new_column_name="id")
