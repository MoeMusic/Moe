"""Test configuration."""

from typing import Iterator
from unittest.mock import Mock, patch

import pytest

from moe.core.config import Config


@pytest.fixture
def mock_config(tmp_path) -> Iterator[Config]:
    """Instantiates a mock configuration.

    Yields:
        The configuration instance.
    """
    with patch.object(Config, "_db_init"):
        yield Config(config_dir=tmp_path, engine=Mock())


class TestInit:
    """Test configuration initialization."""

    def test_dirs_dne(self, tmp_path):
        """Should create the config and database directories if they don't exist."""
        fake_path = tmp_path / "this_definitely_doesnt_exist"

        with patch.object(Config, "_db_init"):
            Config(config_dir=fake_path)

        assert fake_path.exists()

    def test_config_file_dne(self, mock_config):
        """Should create the config file if it doesn't exist."""
        assert mock_config.config_path.exists()


class TestReadConfig:
    """Test reading the actual configuration file."""

    def test_load_file(self, mock_config):
        """Ensure we can load a configuration file."""
        with mock_config.config_path.open("w+") as config_file:
            config_file.write("test yaml")

        mock_config._read_config()
