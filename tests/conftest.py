"""Shared pytest configuration."""

from typing import Iterator
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
    Config(config_dir=MagicMock(), engine=engine)

    with library.session_scope() as session:
        yield session
