"""Rename custom fields.

Revision ID: ab5db9861d30
Revises: 880c5a2d80ed
Create Date: 2022-12-11 15:24:10.227924

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "ab5db9861d30"
down_revision = "880c5a2d80ed"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.alter_column("_custom_fields", new_column_name="custom")

    with op.batch_alter_table("extra", schema=None) as batch_op:
        batch_op.alter_column("_custom_fields", new_column_name="custom")

    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.alter_column("_custom_fields", new_column_name="custom")


def downgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.alter_column("custom", new_column_name="_custom_fields")

    with op.batch_alter_table("extra", schema=None) as batch_op:
        batch_op.alter_column("custom", new_column_name="_custom_fields")

    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.alter_column("custom", new_column_name="_custom_fields")
