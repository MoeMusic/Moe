"""Shared pytest configuration."""
import datetime
import random
import shutil
import sys
import textwrap
from pathlib import Path
from typing import Any, Callable, Iterator, Optional
from unittest.mock import MagicMock

import pytest
import sqlalchemy as sa
import sqlalchemy.exc
import sqlalchemy.orm

from moe import config
from moe.config import Config, ExtraPlugin, MoeSession, session_factory
from moe.library import Album, Extra, Track
from moe.plugins import write as moe_write

__all__ = ["album_factory", "extra_factory", "track_factory"]

RESOURCE_DIR = Path(__file__).parent / "resources"
EMPTY_MP3_FILE = RESOURCE_DIR / "empty.mp3"
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


@pytest.fixture(autouse=True, scope="session")
def _tmp_library_path(tmp_path_factory):
    """Creates a temporary music library directory for all test tracks and albums."""
    global LIBRARY_PATH
    LIBRARY_PATH = tmp_path_factory.mktemp("music")


@pytest.fixture
def tmp_config(
    tmp_path_factory,
) -> Iterator[Callable[[str, bool, bool, list[ExtraPlugin]], Config]]:
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
        config_dir: Optionally specifiy a config directory to use.

    Yields:
        The configuration instance.
    """

    def _tmp_config(
        settings: str = "",
        init_db: bool = False,
        tmp_db: bool = False,
        extra_plugins: Optional[list[ExtraPlugin]] = None,
        config_dir: Optional[Path] = None,
    ) -> Config:
        config_dir = config_dir or tmp_path_factory.mktemp("config")
        assert config_dir

        if "library_path" not in settings:
            settings += f"\nlibrary_path = '{LIBRARY_PATH.resolve()}'"

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
def _clean_moe():
    """Ensure we aren't sharing sessions or configs between tests."""
    MoeSession.remove()
    config.CONFIG = MagicMock()


def track_factory(
    album: Optional[Album] = None,
    exists: bool = False,
    dup_track: Optional[Track] = None,
    custom_fields: Optional[dict[str, Any]] = None,
    **kwargs,
):
    """Creates a track.

    Args:
        album: Optional album to assign the track to.
        exists: Whether the track should exist on the filesystem. Note, this option
            requires the write plugin.
        dup_track: If given, the new track created will be a duplicate of `dup_track`.
        custom_fields: Dict of custom_fields to values to assign to the track.
        **kwargs: Any other fields to assign to the Track.

    Returns:
        Unique Track.
    """
    album = album or album_factory(num_tracks=0, num_extras=0, exists=exists)

    track_num = kwargs.pop("track_num", random.randint(1, 10000))
    title = kwargs.pop("title", "Jazzy Belle")
    disc = kwargs.pop("disc", 1)

    if album.disc_total > 1:
        disc_dir = f"Disc {disc:02}"
    else:
        disc_dir = ""
    path = kwargs.pop(
        "path", album.path / disc_dir / f"{disc}.{track_num} - {title}.mp3"
    )

    track = Track(
        album=album,
        path=path,
        title=title,
        track_num=track_num,
        disc=disc,
        **kwargs,
    )

    if custom_fields:
        for field, value in custom_fields.items():
            track.custom_fields.add(field)
            setattr(track, field, value)

    if dup_track:
        for field in dup_track.fields:
            value = getattr(dup_track, field)
            if field == "genre":
                print(value)
            try:
                setattr(track, field, value)
            except AttributeError:
                pass
        return track

    if exists:
        track.path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(EMPTY_MP3_FILE, track.path)
        moe_write.write_tags(track)

    return track


def extra_factory(
    album: Optional[Album] = None,
    path: Optional[Path] = None,
    exists: bool = False,
    dup_extra: Optional[Extra] = None,
    custom_fields: Optional[dict[str, Any]] = None,
    **kwargs,
) -> Extra:
    """Creates an extra for testing.

    Args:
        album: Album to assign the extra to.
        path: Path to assign to the extra. Will create a random path if not given.
        exists: Whether the extra should actually exist on the filesystem.
        dup_extra: If given, the new extra created will be a duplicate of `dup_extra`.
        custom_fields: Dict of custom_fields to values to assign to the extra.
        **kwargs: Any other fields to assign to the extra.

    Returns:
        Created extra.
    """
    album = album or album_factory(num_tracks=0, num_extras=0, exists=exists)
    path = path or album.path / f"{random.randint(1,1000)}.txt"

    extra = Extra(album=album, path=path, **kwargs)

    if custom_fields:
        for field, value in custom_fields.items():
            extra.custom_fields.add(field)
            setattr(extra, field, value)

    if dup_extra:
        for field in dup_extra.fields:
            value = getattr(dup_extra, field)
            try:
                setattr(extra, field, value)
            except AttributeError:
                pass
        return extra

    if exists:
        extra.path.touch()

    return extra


def album_factory(
    num_tracks: int = 2,
    num_extras: int = 2,
    num_discs: int = 1,
    exists: bool = False,
    dup_album: Optional[Album] = None,
    custom_fields: Optional[dict[str, Any]] = None,
    **kwargs,
) -> Album:
    """Creates an album.

    Args:
        num_tracks: Number of tracks to add to the album.
        num_extras: Number of extras to add to the album.
        num_discs: Number of discs on the album. Will have disc sub dirs.
        exists: Whether the album should exist on the filesystem. Note, this option
            requires the write plugin.
        dup_album: If given, the new album created will be a duplicate of `dup_album`.
        custom_fields: Dict of custom_fields to values to assign to the album.
        **kwargs: Any other fields to assign to the album.

    Returns:
        Created album.
    """
    artist = kwargs.pop("artist", "Outkast")
    title = kwargs.pop("title", "ATLiens")
    date = kwargs.pop(
        "date", datetime.date(random.randint(datetime.MINYEAR, datetime.MAXYEAR), 1, 1)
    )
    path = kwargs.pop("path", LIBRARY_PATH / f"{artist}" / f"{title} ({date.year})")

    album = Album(
        path=path,
        artist=artist,
        title=title,
        date=date,
        disc_total=num_discs,
        **kwargs,
    )
    if custom_fields:
        for field, value in custom_fields.items():
            album.custom_fields.add(field)
            setattr(album, field, value)

    if dup_album:
        for field in dup_album.fields:
            if field not in ["tracks", "extras"]:
                value = getattr(dup_album, field)
                try:
                    setattr(album, field, value)
                except AttributeError:
                    pass

        dup_tracks = dup_album.tracks.copy()
        for track in dup_tracks:
            album.tracks.append(
                track_factory(
                    album=None,
                    exists=exists,
                    dup_track=track,
                )
            )

        dup_extras = dup_album.extras.copy()
        for extra in dup_extras:
            album.extras.append(
                extra_factory(
                    album=None,
                    exists=exists,
                    dup_extra=extra,
                )
            )

        return album

    if exists:
        album.path.mkdir(exist_ok=True, parents=True)

    if num_tracks < num_discs and num_tracks != 0:
        num_tracks = num_discs
    tracks_per_disc = int(num_tracks / num_discs)
    for disc in range(1, num_discs + 1):
        for track_num in range(1, tracks_per_disc + 1):
            track_factory(
                album=album,
                exists=exists,
                track_num=track_num,
                disc=disc,
            )

    for _ in range(1, num_extras):
        extra_factory(album=album, exists=exists)

    return album
