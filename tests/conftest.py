"""Shared pytest configuration."""

from typing import Callable, Iterator
from unittest.mock import MagicMock

import pytest
import sqlalchemy

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

    config = Config(config_dir=MagicMock())
    config.init_db(engine=engine)

    with library.session_scope() as session:
        yield session


@pytest.fixture
def tmp_config(tmp_path) -> Config:
    """Instantiates a temporary configuration.

    This is for use with integration tests.

    Returns:
        The configuration instance.
    """
    config = Config(config_dir=tmp_path)

    config_file = config.config_dir / "config.yaml"
    config_file.touch()

    return config


@pytest.fixture
def mock_track_factory() -> Callable[[], library.Track]:
    """Factory for mock Tracks.

    In particular, the path is mocked so the Track doesn't need to exist.

    Returns:
        Unique Track object with each call.
    """

    def _mock_track():  # noqa: WPS430
        return library.Track(path=MagicMock(), read_tags=False)

    return _mock_track


@pytest.fixture
def mock_track(mock_track_factory) -> library.Track:
    """Creates a single mock Track object.

    Uses `mock_track_factory`.

    Returns:
        Track object.
    """
    return mock_track_factory()
