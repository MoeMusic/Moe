"""audio format non null.

Revision ID: 4279789f5739
Revises: bf49ac6805f7
Create Date: 2022-10-30 15:31:38.324821

"""
import mediafile
import sqlalchemy as sa
from sqlalchemy.orm import Session, declarative_base

import moe
from alembic import op
from moe import config

# revision identifiers, used by Alembic.
revision = "4279789f5739"
down_revision = "bf49ac6805f7"
branch_labels = None
depends_on = None

Base = declarative_base()


class Track(Base):
    __tablename__ = "track"

    _id = sa.Column(sa.Integer, primary_key=True)
    path = sa.Column(moe.library.lib_item.PathType(), nullable=False, unique=True)
    audio_format = sa.Column(sa.String, nullable=False)


def upgrade():
    if not config.CONFIG:  # for tests that create tmp configs
        config.Config(init_db=False)  # read config to get library path

    # populate audio_format values before making it non-nullable
    with Session(bind=op.get_bind()) as session:
        tracks = session.query(Track).all()
        for track in tracks:
            audio_file = mediafile.MediaFile(track.path)

            track.audio_format = audio_file.type

        session.commit()

    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.alter_column("audio_format", existing_type=sa.String(), nullable=False)


def downgrade():
    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.alter_column("audio_format", existing_type=sa.String(), nullable=True)
