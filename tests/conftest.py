"""Shared pytest configuration."""

import random
from typing import Callable, Iterator
from unittest.mock import MagicMock

import pytest
import sqlalchemy
from sqlalchemy.orm.session import Session

from moe.core.config import Config
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
    config._init_db(engine=engine)

    with session_scope() as session:
        yield session


@pytest.fixture
def tmp_config(tmp_path) -> Config:
    """Instantiates a temporary configuration.

    This is for use with integration tests.

    Returns:
        The configuration instance.
    """
    return Config(config_dir=tmp_path)


@pytest.fixture
def mock_track_factory() -> Callable[[], Track]:
    """Factory for mock Tracks.

    In particular, the path is mocked so the Track doesn't need to exist.

    Note:
        Each track will share the same album attributes, and thus will
        belong to the same album if a mock_track already exists in the database.
        If adding multiple tracks of the same album in one session, use
        `session.merge(track)` vice `session.add(track)`

    Returns:
        Unique Track object with each call.
    """

    def _mock_track():  # noqa: WPS430
        return Track(
            path=MagicMock(),
            title="Halftime",
            album="Illmatic",
            albumartist="Nas",
            track_num=random.randint(1, 1000),
            year=1994,
        )

    return _mock_track


@pytest.fixture
def mock_track(mock_track_factory) -> Track:
    """Creates a single mock Track object."""
    return mock_track_factory()
