"""Shared pytest configuration."""
import datetime
import random
import shutil
import textwrap
from pathlib import Path
from typing import Callable, Iterator
from unittest.mock import MagicMock

import pytest
import sqlalchemy
from sqlalchemy.orm.session import Session

from moe.config import Config
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.session import session_scope
from moe.library.track import Track
from moe.plugins import write as moe_write

RESOURCE_DIR = Path(__file__).parent / "resources"


@pytest.fixture
def tmp_session() -> Iterator[Session]:
    """Creates temporary Session instance for database interaction.

    The database is a temporary sqlite instance created in memory.

    Yields:
        session: temp Session instance
    """
    engine = sqlalchemy.create_engine("sqlite:///:memory:")

    config = Config(config_dir=MagicMock())
    config.init_db(engine=engine)

    with session_scope() as session:
        yield session


@pytest.fixture
def tmp_config(tmp_path_factory) -> Callable[[], Config]:
    """Instantiates a temporary configuration.

    This fixture must be declared, like a factory. If you want to use specific config
    settings, pass them in your declaration.

    Note:
        Any paths should be surrounded with triple single quotes ('''). This tells
        toml to treat the path as a raw string, and prevents it from thinking Windows
        paths are full of escape characters.

    Example::
        settings = f"library_path = '''~/Music'''"
        config = tmp_config(settings)

    Returns:
        The configuration instance.
    """

    def _tmp_config(settings: str = "") -> Config:
        config_dir = tmp_path_factory.mktemp("config")
        if settings:
            settings_path = config_dir / "config.toml"
            settings_path.write_text(textwrap.dedent(settings))

        return Config(config_dir=config_dir, settings_filename="config.toml")

    return _tmp_config


@pytest.fixture
def mock_track_factory() -> Callable[[], Track]:
    """Factory for mock Tracks that don't exist on the filesystem.

    Note:
        Each track will share the same album attributes, and thus will
        belong to the same album if a mock_track already exists in the database.
        If adding multiple tracks of the same album in one session, use
        `session.merge(track)` vice `session.add(track)`

    Args:
        track_num: Optional track number.
        album: Optional album to assign the track to.
        year: Optional year to include. Changing this will change which album the
            the track belongs to. This is not used if `album` is passed.

    Returns:
        Unique Track object with each call.
    """

    def _mock_track(track_num: int = 0, album: Album = None, year: int = 1996):
        if not album:
            album = Album(
                "OutKast", "ATLiens", datetime.date(year, 1, 1), path=MagicMock()
            )
        if not track_num:
            track_num = random.randint(1, 10000)
        return Track(
            album=album,
            path=MagicMock(),
            track_num=track_num,
            title="Jazzy Belle",
            genre="Hip Hop",
        )

    return _mock_track


@pytest.fixture
def mock_track(mock_track_factory) -> Track:
    """Creates a single mock Track object."""
    return mock_track_factory()


@pytest.fixture
def mock_album_factory(mock_extra_factory, mock_track_factory) -> Callable[[], Album]:
    """Factory for mock Albums that don't exist on the filesytem.

    Returns:
        Album with two tracks and two extras.
    """

    def _mock_album():
        year = random.randint(1, 1000)

        album = Album("OutKast", "ATLiens", datetime.date(year, 1, 1), path=MagicMock())

        mock_track_factory(track_num=1, album=album)
        mock_track_factory(track_num=2, album=album)
        mock_extra_factory(album=album)
        mock_extra_factory(album=album)

        return album

    return _mock_album


@pytest.fixture
def mock_album(mock_album_factory) -> Album:
    """Creates a single mock Album object."""
    return mock_album_factory()


@pytest.fixture
def mock_extra_factory() -> Callable[[], Extra]:
    """Factory for mock Extras that don't exist on the filesytem.

    Each extra will belong to the same album unless `year` or a different `album` is
    given.

    Args:
        album: Optional album to assign the extra to.
        year: Optional year to include. Changing this will change which album the
            the extra belongs to. This is not used if `album` is passed.

    Returns:
        Unique Extra object.
    """

    def mock_lt(self, other):
        return self.name < other.name

    def _mock_extra(album: Album = None, year: int = 1996):
        if not album:
            album = Album(
                "OutKast", "ATLiens", datetime.date(year, 1, 1), path=MagicMock()
            )

        mock_path = MagicMock()

        mock_path.__lt__ = mock_lt
        mock_path.name = f"{random.randint(1, 10000)}.txt"
        return Extra(mock_path, album)

    return _mock_extra


@pytest.fixture
def mock_extra(mock_extra_factory) -> Extra:
    """Creates a single mock Extra object."""
    return mock_extra_factory()


@pytest.fixture
def real_track_factory(
    empty_mp3_path, mock_track_factory, tmp_path_factory
) -> Callable[[], Track]:
    """Creates a Track on the filesystem.

    The track is copied to a temp location, so feel free to make any changes. Each
    track will belong to a single album.

    Args:
        track_num: Optional track number.
        album: Optional album to assign the track to. If given, assumes the album's path
            exists on the filesystem.
        year: Optional year. Changing this will change which album the track belongs to.
            Not used if `album` is passed.

    Note:
        If you don't need to interact with the filesystem, it's preferred to use
        `mock_track_factory`.

    Returns:
        Unique Track.
    """

    def _real_track(track_num: int = 0, album: Album = None, year: int = 1994):
        track = mock_track_factory(track_num, album, year)

        if not album:
            track.album_obj.path = tmp_path_factory.mktemp(
                f"{track.albumartist} - {track.album} {track.year}"
            )

        filename = f"{track.track_num} - {track.title}.mp3"
        track.path = track.album_obj.path / filename
        shutil.copyfile(empty_mp3_path, track.path)

        moe_write.write_tags(track)
        return track

    return _real_track


@pytest.fixture
def real_track(real_track_factory) -> Track:
    """Creates a single Track that exists on the filesystem.

    Note:
        If you do not need to interact with the filesytem, it is preferred to use
        `mock_track`

    Returns:
        Unique Track.
    """
    return real_track_factory()


@pytest.fixture
def real_album_factory(
    real_extra_factory, real_track_factory, tmp_path_factory
) -> Callable[[], Album]:
    """Factory for Albums that exist on the filesytem.

    Returns:
        Album with two tracks and two extras.
    """

    def _real_album_factory():
        artist = "Outkast"
        title = "ATLiens"
        year = random.randint(1, 1000)
        path = tmp_path_factory.mktemp(f"{artist} - {title} ({year})")

        album = Album(artist, title, datetime.date(year, 1, 1), path=path)

        real_track_factory(track_num=1, album=album)
        real_track_factory(track_num=2, album=album)
        real_extra_factory(album=album)
        real_extra_factory(album=album)

        return album

    return _real_album_factory


@pytest.fixture
def real_album(real_album_factory) -> Album:
    """Creates a single Album on the filesystem."""
    return real_album_factory()


@pytest.fixture
def real_extra_factory(mock_extra_factory, tmp_path_factory) -> Callable[[], Extra]:
    """Creates an Extra on the filesystem.

    The track is copied to a temp location, so feel free to make any changes. Each
    extra will belong to a single album.

    Args:
        album: Optional album to assign the track to. If given, assumes the album's path
            exists on the filesystem.
        year: Optional year. Changing this will change which album the track belongs to.
            Not used if `album` is passed.

    Returns:
        Unique Extra.
    """

    def _real_extra(album: Album = None, year: int = 1994):
        extra = mock_extra_factory(album, year)

        if not album:
            extra.album_obj.path = tmp_path_factory.mktemp(
                "Jacobs Awesome Band - Cool Song (2021)"
            )

        filename = f"{random.randint(1, 10000)}.txt"
        extra.path = extra.album_obj.path / filename
        extra.path.touch()

        return extra

    return _real_extra


@pytest.fixture
def real_extra(real_extra_factory) -> Extra:
    """Creates a single Extra that exists on the filesystem."""
    return real_extra_factory()


@pytest.fixture
def empty_mp3_path() -> Path:
    """Path to an mp3 file with no tags."""
    return RESOURCE_DIR / "empty.mp3"


@pytest.fixture
def reqd_mp3_path() -> Path:
    """Path to an mp3 file with the minimum required tags."""
    return RESOURCE_DIR / "reqd.mp3"


@pytest.fixture
def full_mp3_path() -> Path:
    """Path to an mp3 file with every tag."""
    return RESOURCE_DIR / "full.mp3"
