"""Shared pytest configuration."""

import pathlib
from typing import Iterator, Tuple
from unittest.mock import MagicMock

import pluggy
import pytest
import sqlalchemy

from moe import cli
from moe.core import library
from moe.core.config import Config


@pytest.fixture
def tmp_session() -> Iterator[sqlalchemy.orm.session.Session]:
    """Creates temporary Session instance for database interaction.

    The database is a temporary sqlite instance created in memory.

    Yields:
        session: temp Session instance
    """
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    Config(config_dir=MagicMock(), engine=engine)

    with library.session_scope() as session:
        yield session


@pytest.fixture
def tmp_live(tmp_path) -> Tuple[Config, pluggy.PluginManager]:
    """Instantiates an actual configuration and pluginmanager under a tmp path.

    Returns:
        A tuple containing the config and pluginmanager
    """
    config = Config(config_dir=tmp_path)
    pm = cli._get_plugin_manager(config)

    return config, pm


@pytest.fixture(scope="session")
def make_track():
    """Factory for a temporary Track object.

    Call with arguments specified in _make_track.

    Example:
        `track = make_track(1)`
    """

    def _make_track(track_id: int):
        track = library.Track(pathlib.Path("track_" + str(track_id)))
        track.id = track_id

        return track

    return _make_track
