"""Tests configuration."""

from moe.core.config import Config


class TestInit:
    """Test configuration initialization."""

    def test_config_dir_dne(self, tmp_path):
        """Should create the config directory if it doesn't exist."""
        config = Config(tmp_path / "doesn't exist")

        assert config.config_dir.is_dir()

    def test_config_file_dne(self, tmp_path):
        """Should create an empty config file if it doesn't exist."""
        Config(config_dir=tmp_path, settings_filename="config.toml")

        assert (tmp_path / "config.toml").is_file()

    def test_default_plugins(self, tmp_config):
        """Only register enabled + default plugins.

        The config "plugin" will always be registered.
        """
        config = tmp_config(settings='default_plugins = ["ls"]')

        plugins = ["moe.core.config", "moe.plugins.ls"]
        for plugin_name, _ in config.pluginmanager.list_name_plugin():
            assert plugin_name in plugins
