"""Shared pytest configuration."""
import random
import shutil
import textwrap
from typing import Callable, Generator, Iterator
from unittest.mock import MagicMock, patch

import pytest
import sqlalchemy
from sqlalchemy.orm.session import Session

from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.core.library.track import Track


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
def tmp_config(tmp_path) -> Callable[[], Config]:
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
        if settings:
            settings_path = tmp_path / "config.toml"
            settings_path.write_text(textwrap.dedent(settings))

        return Config(config_dir=tmp_path, settings_filename="config.toml")

    return _tmp_config


@pytest.fixture
def mock_track_factory() -> Generator[Callable[[], Track], None, None]:
    """Factory for mock Tracks that don't exist on the filesystem.

    Note:
        Each track will share the same album attributes, and thus will
        belong to the same album if a mock_track already exists in the database.
        If adding multiple tracks of the same album in one session, use
        `session.merge(track)` vice `session.add(track)`

    Yields:
        Unique Track object with each call.
    """

    def _mock_track():
        return Track(
            path=MagicMock(),  # doesn't need to exist on the filesystem
            title="Halftime",
            album="Illmatic",
            albumartist="Nas",
            track_num=random.randint(1, 1000),
            year=1994,
        )

    # don't try to write tags
    with patch("moe.core.library.session.Track.write_tags"):
        yield _mock_track


@pytest.fixture
def mock_track(mock_track_factory) -> Track:
    """Creates a single mock Track object."""
    return mock_track_factory()


@pytest.fixture
def real_track_factory(tmp_path) -> Callable[[], Track]:
    """Creates a Track on the filesystem.

    The track is copied to a temp location, so feel free to make any changes. Each
    track will belong to a single album.

    Args:
        year: Optional year to include. Changing this will change which album the
            the track belongs to.

    Note:
        If you don't need to interact with the filesystem, it's preferred to use
        `mock_track_factory`.

    Returns:
        Unique Track.
    """

    def _real_track(year: int = 1994):
        track_num = random.randint(1, 1000)
        track_path = tmp_path / f"{track_num}"
        shutil.copyfile("tests/resources/empty.mp3", track_path)

        track = Track(
            album="Illmatic",
            albumartist="Nas",
            artist="Nas",
            genre=["East Coast Hip Hop", "Hip Hop"],
            title="N.Y. State of Mind",
            path=track_path,
            track_num=track_num,
            year=year,
        )
        track.write_tags()
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
        track = real_track_factory(year)

        album = track._album_obj
        album.tracks.add(real_track_factory(year))

        return album

    return _real_album_factory


@pytest.fixture
def real_album(real_album_factory) -> Album:
    """Creates a single Album on the filesystem."""
    return real_album_factory()
