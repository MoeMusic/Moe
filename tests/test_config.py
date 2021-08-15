"""Tests configuration."""

from unittest.mock import patch

from moe.config import Config


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

        The config and cli "plugins" will always be registered.
        """
        config = tmp_config(settings='default_plugins = ["list", "write"]')

        plugins = ["config", "list", "write"]
        for plugin_name, _ in config.plugin_manager.list_name_plugin():
            assert plugin_name in plugins

    def test_config_dir_env(self, tmp_path):
        """The configuration directory can be set with an env var."""
        with patch.dict("os.environ", {"MOE_CONFIG_DIR": str(tmp_path)}):
            config = Config()
            assert config.config_dir == tmp_path


class TestPlugins:
    """Test setting up and registering plugins."""

    def test_enabled_plugins(self, tmp_config):
        """Only register enabled + default plugins.

        Note:
            The config plugin will always be registered.
        """
        config = tmp_config(settings='default_plugins = ["cli", "list"]')

        plugins = ["config", "cli", "list"]
        for plugin_name, plugin_module in config.plugin_manager.list_name_plugin():
            assert plugin_name in plugins
            assert plugin_module

        for plugin in plugins:
            assert config.plugin_manager.has_plugin(plugin)
