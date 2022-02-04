"""Tests configuration."""

from unittest.mock import patch

import dynaconf

import moe
from moe.config import Config, ExtraPlugin
from moe.library.track import Track


class TestInit:
    """Test configuration initialization."""

    def test_config_dir_dne(self, tmp_path):
        """Should create the config directory if it doesn't exist."""
        config = Config(tmp_path / "doesn't exist", init_db=False)

        assert config.config_dir.is_dir()

    def test_config_file_dne(self, tmp_path):
        """Should create an empty config file if it doesn't exist."""
        Config(config_dir=tmp_path, settings_filename="config.toml", init_db=False)

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
            config = Config(init_db=False)
            assert config.config_dir == tmp_path


class TestPlugins:
    """Test setting up and registering plugins."""

    def test_config_plugins(self, tmp_config):
        """All plugins specified in the configuration are registered.

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

    def test_extra_plugins(self, tmp_config):
        """Any given additional plugins are also registered."""
        config = tmp_config(extra_plugins=[ExtraPlugin(TestPlugins, "config_plugin")])

        assert config.plugin_manager.has_plugin("config_plugin")


class ConfigPlugin:
    """Plugin that implements the config hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def edit_new_items(config, items):
        """Edit the incoming items."""
        for item in items:
            if isinstance(item, Track):
                item.title = "config"

    @staticmethod
    @moe.hookimpl
    def process_new_items(config, items):
        """Process the incoming items."""
        for item in items:
            if isinstance(item, Track):
                item.track_num = 3

    @staticmethod
    @moe.hookimpl
    def add_config_validator(settings):
        """Add the `config_plugin` configuration option."""
        settings.validators.register(
            dynaconf.Validator("CONFIG_PLUGIN", must_exist=True, default="hello!")
        )

    @staticmethod
    @moe.hookimpl
    def plugin_registration(config):
        """Alter the `config_dir` at plugin registration."""
        config.plugin_manager.unregister(ConfigPlugin)
        config.plugin_manager.register(ConfigPlugin, "config2")


class TestHooks:
    """Test the config hook specifications."""

    def test_add_config_validator(self, tmp_config):
        """Ensure plugins can implement the `add_config_validator` hook."""
        config = tmp_config(extra_plugins=[ExtraPlugin(ConfigPlugin, "config_plugin")])

        assert config.settings.config_plugin == "hello!"

    def test_edit_new_items(self, mock_track, tmp_config, tmp_session):
        """Ensure plugins can implement the `edit_new_items` hook."""
        tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(ConfigPlugin, "config_plugin")],
            tmp_db=True,
        )

        tmp_session.add(mock_track)
        tmp_session.flush()

        assert mock_track.title == "config"

    def test_process_new_items(self, mock_track, tmp_config, tmp_session):
        """Ensure plugins can implement the `add_hooks` hook."""
        tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(ConfigPlugin, "config_plugin")],
            tmp_db=True,
        )

        tmp_session.add(mock_track)
        tmp_session.flush()

        assert mock_track.track_num == 3

    def test_plugin_registration(self, tmp_config):
        """Ensure plugins can implement the `plugin_registration` hook."""
        config = tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(ConfigPlugin, "config_plugin")],
        )

        assert config.plugin_manager.has_plugin("config2")
