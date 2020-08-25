"""Test configuration."""

import pytest

from moe.core.config import Config


class TestInit:
    """Test configuration initialization."""

    def test_config_dir_dne(self, tmp_path):
        """Should create the config directory if it doesn't exist."""
        assert Config(config_dir=tmp_path / "does not exist").config_dir.exists()


class TestReadConfig:
    """Test reading the actual configuration file."""

    def test_load_file(self, tmp_path):
        """Ensure we can load a configuration file."""
        config = Config()
        config_path = tmp_path / "config.yaml"

        with config_path.open("w") as config_file:
            config_file.write("test yaml")

        config.read_config(config_path.read_text())

    def test_config_file_dne(self, tmp_path):
        """Error if the configuration file doesn't exist."""
        config = Config(config_dir=tmp_path)

        with pytest.raises(SystemExit) as error:
            config.read_config()

        assert error.value.code != 0
