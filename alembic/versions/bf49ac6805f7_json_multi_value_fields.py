"""json multi value fields.

Revision ID: bf49ac6805f7
Revises: ab11c34c1d0b
Create Date: 2022-10-17 21:09:09.265544

"""
import sqlalchemy as sa
from sqlalchemy.ext.mutable import MutableSet
from sqlalchemy.orm import Session, declarative_base

from alembic import op
from moe.library.lib_item import SetType

# revision identifiers, used by Alembic.
revision = "bf49ac6805f7"
down_revision = "ab11c34c1d0b"
branch_labels = None
depends_on = None

Base = declarative_base()


class _Artist(Base):
    """A track can have multiple artists."""

    __tablename__ = "artist"

    _id = sa.Column(sa.Integer, primary_key=True)
    _track_id = sa.Column(sa.Integer, sa.ForeignKey("track._id"))
    name = sa.Column(sa.String, nullable=False)

    def __init__(self, name: str):
        self.name = name


class _Genre(Base):
    """A track can have multiple genres."""

    __tablename__ = "genre"

    _id = sa.Column(sa.Integer, primary_key=True)
    _track_id = sa.Column(sa.Integer, sa.ForeignKey("track._id"))
    name = sa.Column(sa.String, nullable=False)

    def __init__(self, name: str):
        self.name = name


class _CatalogNums(Base):
    """An album can have multiple catalog numbers."""

    __tablename__ = "catalog_num"

    _id = sa.Column(sa.Integer, primary_key=True)
    _album_id = sa.Column(sa.Integer, sa.ForeignKey("album._id"))
    catalog_num = sa.Column(sa.String, nullable=False)

    def __init__(self, catalog_num: str):
        self.catalog_num = catalog_num


class Track(Base):
    __tablename__ = "track"

    _id = sa.Column(sa.Integer, primary_key=True)
    artists = MutableSet.as_mutable(sa.Column(SetType))
    genres = MutableSet.as_mutable(sa.Column(SetType))


class Album(Base):
    __tablename__ = "album"

    _id = sa.Column(sa.Integer, primary_key=True)
    catalog_nums = MutableSet.as_mutable(sa.Column(SetType))


def upgrade():
    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("catalog_nums", MutableSet.as_mutable(SetType()), nullable=True)
        )

    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("artists", MutableSet.as_mutable(SetType()), nullable=True)
        )
        batch_op.add_column(
            sa.Column("genres", MutableSet.as_mutable(SetType()), nullable=True)
        )

    with Session(bind=op.get_bind()) as session:
        tracks = session.query(Track).all()
        for track in tracks:
            genres = session.query(_Genre).filter(_Genre._track_id == track._id).all()
            track.genres = {genre.name for genre in genres}

            artists = (
                session.query(_Artist).filter(_Artist._track_id == track._id).all()
            )
            track.artists = {artist.name for artist in artists}

        albums = session.query(Album).all()
        for album in albums:
            catalog_nums = (
                session.query(_CatalogNums)
                .filter(_CatalogNums._album_id == album._id)
                .all()
            )
            album.catalog_nums = {
                catalog_num.catalog_num for catalog_num in catalog_nums
            }
        session.commit()

    op.drop_table("genre")
    op.drop_table("catalog_num")
    op.drop_table("artist")


def downgrade():
    op.create_table(
        "artist",
        sa.Column("_id", sa.INTEGER(), nullable=False),
        sa.Column("_track_id", sa.INTEGER(), nullable=True),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.ForeignKeyConstraint(
            ["_track_id"],
            ["track._id"],
        ),
        sa.PrimaryKeyConstraint("_id"),
    )
    op.create_table(
        "catalog_num",
        sa.Column("_id", sa.INTEGER(), nullable=False),
        sa.Column("_album_id", sa.INTEGER(), nullable=True),
        sa.Column("catalog_num", sa.VARCHAR(), nullable=False),
        sa.ForeignKeyConstraint(
            ["_album_id"],
            ["album._id"],
        ),
        sa.PrimaryKeyConstraint("_id"),
    )
    op.create_table(
        "genre",
        sa.Column("_id", sa.INTEGER(), nullable=False),
        sa.Column("_track_id", sa.INTEGER(), nullable=True),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.ForeignKeyConstraint(
            ["_track_id"],
            ["track._id"],
        ),
        sa.PrimaryKeyConstraint("_id"),
    )

    with Session(bind=op.get_bind()) as session:
        tracks = session.query(Track).all()
        for track in tracks:
            genres = track.genres
            if genres is not None:
                for genre in genres:
                    db_genre = _Genre(genre)
                    db_genre._track_id = track._id
                    session.add(db_genre)

            artists = track.artists
            if artists is not None:
                for artist in artists:
                    db_artist = _Artist(artist)
                    db_artist._track_id = track._id
                    session.add(db_artist)

        albums = session.query(Album).all()
        for album in albums:
            catalog_nums = album.catalog_nums
            if catalog_nums is not None:
                for catalog_num in catalog_nums:
                    db_catalog_num = _CatalogNums(catalog_num)
                    db_catalog_num._album_id = album._id
                    session.add(db_catalog_num)

        session.commit()

    with op.batch_alter_table("track", schema=None) as batch_op:
        batch_op.drop_column("genres")
        batch_op.drop_column("artists")

    with op.batch_alter_table("album", schema=None) as batch_op:
        batch_op.drop_column("catalog_nums")
