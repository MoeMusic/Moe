"""Shared pytest configuration."""

from typing import Iterator, Tuple
from unittest.mock import MagicMock

import pytest
import sqlalchemy

from moe.core import library
from moe.core.config import Config


@pytest.fixture
def temp_config_session() -> Iterator[Tuple[Config, sqlalchemy.orm.session.Session]]:
    """Creates temporary Config and Session instances.

    This should be used for database interaction.

    Yields:
        config, session (Tuple): temp Config and Session instances
    """
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    config = Config(config_dir=MagicMock(), engine=engine)

    with library.session_scope() as session:
        yield config, session
