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


@pytest.fixture
def add_track(tmp_live):
    """Adds a track a `tmp_live` instance."""
    track = library.Track(path=pathlib.Path("testpath"))

    with library.session_scope() as session:
        session.add(track)
