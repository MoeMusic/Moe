"""Shared pytest configuration."""
import pathlib
import random
import shutil
import textwrap
from typing import Callable, Iterator, cast
from unittest.mock import MagicMock

import pytest
import sqlalchemy
from sqlalchemy.orm.session import Session

from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins import write as moe_write


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
        year: Optional year to include. Changing this will change which album the
            the track belongs to.

    Returns:
        Unique Track object with each call.
    """

    def _mock_track(year: int = 1996):
        album = Album("Outkast", "ATLiens", year, path=MagicMock())
        track_num = random.randint(1, 1000)
        return Track(
            album=album,
            track_num=track_num,
            filename=f"{track_num} - Jazzy Belle.mp3",
            title="Jazzy Belle",
        )

    return _mock_track


@pytest.fixture
def mock_track(mock_track_factory) -> Track:
    """Creates a single mock Track object."""
    return mock_track_factory()


@pytest.fixture
def mock_album_factory(mock_track_factory) -> Callable[[], Album]:
    """Factory for mock Albums that don't exist on the filesytem."""

    def _mock_album():
        return mock_track_factory(random.randint(1, 1000)).album_obj

    return _mock_album


@pytest.fixture
def mock_album(mock_album_factory) -> Album:
    """Creates a single mock Album object."""
    return mock_album_factory()


@pytest.fixture
def real_track_factory(tmp_path_factory) -> Callable[[], Track]:
    """Creates a Track on the filesystem.

    The track is copied to a temp location, so feel free to make any changes. Each
    track will belong to a single album.

    Args:
        path: Optional album directory to place the track under.
        year: Optional year to include. Changing this will change which album the
            the track belongs to.

    Note:
        If you don't need to interact with the filesystem, it's preferred to use
        `mock_track_factory`.

    Returns:
        Unique Track.
    """

    def _real_track(album_dir: pathlib.Path = None, year: int = 1994):
        album = "Illmatic"
        albumartist = "Nas"
        track_num = random.randint(1, 1000)
        title = "N.Y. State of Mind"

        if not album_dir:
            album_dir = tmp_path_factory.mktemp(f"{albumartist} - {album} ({year})")

        filename = f"{track_num} - {title}"
        shutil.copyfile(
            "tests/resources/empty.mp3", cast(pathlib.Path, album_dir) / filename
        )

        album_obj = Album(
            artist=albumartist,
            title=album,
            year=year,
            path=cast(pathlib.Path, album_dir),
        )
        track = Track(
            album=album_obj,
            genre=["East Coast Hip Hop", "Hip Hop"],
            title=title,
            filename=filename,
            track_num=track_num,
            artist=albumartist,
        )
        moe_write._write_tags(track)
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
def real_album_factory(real_track_factory) -> Callable[[], Album]:
    """Creates an Album on the filesystem."""

    def _real_album_factory():
        """Creates an album with two tracks."""
        year = random.randint(1, 1000)
        track = real_track_factory(year=year)

        album = track.album_obj
        album.tracks.add(real_track_factory(album_dir=album.path, year=year))

        log_file = album.path / "log.txt"
        log_file.touch()
        album.extras.add(Extra(log_file.name, album))

        return album

    return _real_album_factory


@pytest.fixture
def real_album(real_album_factory) -> Album:
    """Creates a single Album on the filesystem."""
    return real_album_factory()
