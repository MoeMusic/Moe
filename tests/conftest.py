"""Shared pytest configuration."""
import datetime
import random
import shutil
import sys
import textwrap
from pathlib import Path
from types import FunctionType
from typing import Callable, Iterator, List, Optional
from unittest.mock import MagicMock, patch

import pytest
import sqlalchemy as sa
import sqlalchemy.exc
import sqlalchemy.orm

from moe.config import Config, ExtraPlugin, MoeSession, session_factory
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.track import Track
from moe.plugins import write as moe_write

RESOURCE_DIR = Path(__file__).parent / "resources"
SUPPORTED_PLATFORMS = {"darwin", "linux", "win32"}


def pytest_runtest_setup(item):
    """Only run tests on their appropriate platform.

    Use the following markers to mark tests for specific platforms:
        @pytest.mark.darwin
        @pytest.mark.linux
        @pytest.mark.win32

    See Also:
       pytest docs: https://docs.pytest.org/en/latest/example/markers.html#marking-platform-specific-tests-with-pytest
    """  # noqa: E501
    platforms = SUPPORTED_PLATFORMS.intersection(
        mark.name for mark in item.iter_markers()
    )
    platform = sys.platform
    if platforms and platform not in platforms:
        pytest.skip(f"cannot run on platform {platform}")


@pytest.fixture
def tmp_library_path(tmp_path_factory):
    """Creates a temporary music library directory for all test tracks and albums."""
    return tmp_path_factory.mktemp("music")


@pytest.fixture
def tmp_config(
    tmp_path_factory, tmp_library_path
) -> Iterator[Callable[[str, bool, bool, List[ExtraPlugin]], Config]]:
    """Instantiates a temporary configuration.

    This fixture must be declared, like a factory. If you want to use specific config
    settings, pass them in your declaration.

    Example::
        settings = f"library_path = '''~/Music'''"
        config = tmp_config(settings)

    Note:
        Any paths should be surrounded with triple single quotes ('''). This tells
        toml to treat the path as a raw string, and prevents it from thinking Windows
        paths are full of escape characters.

    Args:
        settings: Settings string to use. This has the same format as a normal
            ``config.toml`` file.
        init_db: Whether or not to initialize the database.
        tmp_db: Whether or not to use a temporary (in-memory) database. If ``True``,
            the database will be initialized regardless of ``init_db``.
        extra_plugins: Any additional plugins to enable.

    Yields:
        The configuration instance.
    """

    def _tmp_config(
        settings: str = "",
        init_db: bool = False,
        tmp_db: bool = False,
        extra_plugins: Optional[List[ExtraPlugin]] = None,
    ) -> Config:
        config_dir = tmp_path_factory.mktemp("config")
        if "library_path" not in settings:
            settings += f"\nlibrary_path='{tmp_library_path.resolve()}'"

        settings_path = config_dir / "config.toml"
        settings_path.write_text(textwrap.dedent(settings))

        engine: Optional[sa.engine.base.Engine]
        if tmp_db:
            engine = sa.create_engine("sqlite:///:memory:")
            init_db = True
        else:
            engine = None

        return Config(
            config_dir=config_dir,
            settings_filename="config.toml",
            extra_plugins=extra_plugins,
            engine=engine,
            init_db=init_db,
        )

    yield _tmp_config
    session_factory.configure(bind=None)  # reset the database in between tests


@pytest.fixture
def tmp_session(tmp_config) -> Iterator[sqlalchemy.orm.session.Session]:
    """Creates a temporary session.

    If you are also using `tmp_config` in your test, ensure to specify `tmp_db=True`
    when creating the `tmp_config` instance.

    Yields:
        The temporary session.
    """
    try:
        MoeSession().get_bind()
    except sqlalchemy.exc.UnboundExecutionError:
        MoeSession.remove()
        tmp_config("default_plugins = []", tmp_db=True)

    session = MoeSession()
    with session.begin():
        yield session

    MoeSession.remove()


@pytest.fixture(autouse=True)
def clean_session():
    """Ensure we aren't sharing sessions between tests."""
    MoeSession.remove()


@pytest.fixture
def mock_query() -> Iterator[FunctionType]:
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Assumes `query` is imported as `moe.query`.

    Yields:
        Mock query
    """
    with patch("moe.query.query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def mock_track_factory() -> Callable[[], Track]:
    """Factory for mock Tracks that don't exist on the filesystem.

    Note:
        Each track will belong to a different album unless `album` is specified.

    Args:
        album: Optional album to assign the track to.
        **kwargs: Any other fields to assign to the Track.

    Returns:
        Unique Track object with each call.
    """

    def _mock_track(album: Optional[Album] = None, **kwargs):
        if not album:
            album = Album(
                "OutKast", "ATLiens", datetime.date(1996, 8, 27), path=MagicMock()
            )

        return Track(
            album=album,
            path=kwargs.pop("path", MagicMock()),
            track_num=kwargs.pop("track_num", random.randint(1, 10000)),
            title=kwargs.pop("title", "Jazzy Belle"),
            genre=kwargs.pop("genre", "Hip Hop"),
            **kwargs,
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
        year = random.randint(1, 10000)

        album = Album(
            "ATCQ", "Midnight Marauders", datetime.date(year, 11, 9), path=MagicMock()
        )

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

    Each extra will belong to a different album unless `album` is given.

    Args:
        path: Optional path to assign.
        album: Optional album to assign the extra to.

    Returns:
        Unique Extra object.
    """

    def mock_lt(self, other):
        return self.name < other.name

    def _mock_extra(path: Optional[Path] = None, album: Optional[Album] = None):
        if not album:
            album = Album(
                "OutKast",
                "ATLiens",
                datetime.date(random.randint(1, 10000), 1, 1),
                path=MagicMock(),
            )

        if not path:
            path = MagicMock()
            path.__lt__ = mock_lt
            path.name = f"{random.randint(1, 10000)}.txt"

        return Extra(path, album)

    return _mock_extra


@pytest.fixture
def mock_extra(mock_extra_factory) -> Extra:
    """Creates a single mock Extra object."""
    return mock_extra_factory()


@pytest.fixture
def real_track_factory(
    empty_mp3_path, mock_track_factory, tmp_library_path
) -> Callable[[], Track]:
    """Creates a Track on the filesystem.

    Note:
        Each track will belong to a different album unless `album` is specified.

    Args:
        album: Optional album to assign the track to. If given, assumes the album's path
            exists on the filesystem.
        real_path: Optional path of a real music file to use. The file at `real_path`
            will be copied into the temporary music library.
        **kwargs: Any other fields to assign to the track.

    Note:
        If you don't need to interact with the filesystem, it's preferred to use
        `mock_track_factory`.

    Returns:
        Unique Track.
    """

    def _real_track(
        album: Optional[Album] = None,
        real_path: Optional[Path] = None,
        **kwargs,
    ):
        track = mock_track_factory(album, **kwargs)

        if not album:
            track.album_obj.path = (
                tmp_library_path
                / f"{track.albumartist}"
                / f"{track.album} ({track.year})"
            )
            track.album_obj.path.mkdir(exist_ok=True, parents=True)

        filename = f"{track.track_num} - {track.title}.mp3"
        track.path = kwargs.pop("path", track.album_obj.path / filename)
        track.path.parent.mkdir(exist_ok=True, parents=True)

        if real_path:
            shutil.copyfile(real_path, track.path)
        else:
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
    real_extra_factory, real_track_factory, tmp_library_path
) -> Callable[[], Album]:
    """Factory for Albums that exist on the filesytem.

    Args:
        **kwargs: Any fields to assign to the album.

    Returns:
        Album with two tracks and two extras.
    """

    def _real_album_factory(**kwargs):
        year = random.randint(1, 10000)
        artist = kwargs.pop("artist", "Outkast")
        title = kwargs.pop("title", "ATLiens")
        date = kwargs.pop("data", datetime.date(year, 1, 1))
        path = kwargs.pop("path", tmp_library_path / f"{artist}" / f"{title} ({year})")

        album = Album(artist, title, date, path)
        album.path.mkdir(exist_ok=True, parents=True)

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
def real_extra_factory(mock_extra_factory, tmp_library_path) -> Callable[[], Extra]:
    """Creates an Extra on the filesystem.

    Note:
        Each track will belong to a different album unless `album` is specified.

    Args:
        path: Optional path to assign. Will create the file if it does not exist.
        album: Optional album to assign the track to. If given, assumes the album's path
            exists on the filesystem.

    Returns:
        Unique Extra.
    """

    def _real_extra(
        path: Optional[Path] = None,
        album: Optional[Album] = None,
    ):
        extra = mock_extra_factory(path=path, album=album)

        if not album:
            extra.album_obj.path = (
                tmp_library_path / "Jacob's Awesome Band" / "Cool Song (1996)"
            )
            extra.album_obj.path.mkdir(exist_ok=True, parents=True)

        filename = f"{random.randint(1, 10000)}.txt"
        if not path:
            path = extra.album_obj.path / filename
        assert path
        extra.path = path
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
