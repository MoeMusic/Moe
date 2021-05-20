"""Test configuration."""

from moe.core.config import _Config


class TestInit:
    """Test configuration initialization."""

    def test_config_dir_dne(self, tmp_path):
        """Should create the config directory if it doesn't exist."""
        config = _Config(tmp_path / "doesn't exist")

        assert config.config_dir.is_dir()


class TestReadConfig:
    """Test reading the configuration file."""

    def test_config_file_dne(self, tmp_path):
        """Should create an empty config file if it doesn't exist."""
        config = _Config(config_dir=tmp_path)
        config._read_config()

        assert (config.config_dir / "config.toml").is_file()
