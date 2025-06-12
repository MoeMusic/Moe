"""Tests configuration."""

import logging
import shutil
from pathlib import Path
from unittest.mock import patch

import dynaconf
import pytest

import moe
from moe import config
from moe.config import CORE_PLUGINS, Config, ConfigValidationError, ExtraPlugin


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

        The config, track, album, and extra "plugins" will always be registered.
        """
        config = tmp_config(settings='default_plugins = ["list", "write"]')

        plugins = list(CORE_PLUGINS) + ["list", "write"]
        for plugin_name, _ in config.pm.list_name_plugin():
            assert plugin_name in plugins

    def test_config_dir_env(self, tmp_path):
        """The configuration directory can be set with an env var."""
        with patch.dict("os.environ", {"MOE_CONFIG_DIR": str(tmp_path)}):
            Config(init_db=False)
            assert config.CONFIG.config_dir == tmp_path

    def test_bad_validation(self, tmp_config):
        """Raise a ConfigValidationError if the configuration is invalid."""
        with pytest.raises(ConfigValidationError):
            tmp_config(extra_plugins=[ExtraPlugin(ConfigPlugin, "config_plugin")])


class TestPlugins:
    """Test setting up and registering plugins."""

    def test_config_plugins(self, tmp_config):
        """All plugins specified in the configuration are registered.

        Note:
            The config, track, album, and extra "plugins" will always be registered.
        """
        tmp_config(
            settings="""default_plugins = ["cli", "list"]
        disable_plugins = ["list"]"""
        )

        plugins = list(CORE_PLUGINS) + ["cli"]
        for plugin_name, plugin_module in config.CONFIG.pm.list_name_plugin():
            assert plugin_name in plugins
            assert plugin_module

        for plugin in plugins:
            assert config.CONFIG.pm.has_plugin(plugin)

    def test_enable_plugins(self, tmp_config):
        """We can explictly enable plugins."""
        tmp_config(
            settings="""default_plugins = ["cli"]
        enable_plugins = ["list"]"""
        )

        assert config.CONFIG.pm.has_plugin("list")

    def test_extra_plugins(self, tmp_config):
        """Any given additional plugins are also registered."""
        tmp_config(extra_plugins=[ExtraPlugin(TestPlugins, "config_plugin")])

        assert config.CONFIG.pm.has_plugin("config_plugin")

    def test_register_local_user_plugins(self, tmp_config, tmp_path_factory):
        """We can register plugins in the user plugin directory."""
        config_dir = tmp_path_factory.mktemp("config")
        plugin_dir = config_dir / "plugins"
        plugin_dir.mkdir()

        list_path = Path(__file__).resolve().parent.parent / "moe/list.py"
        shutil.copyfile(list_path, plugin_dir / "my_list.py")

        tmp_config(settings="enable_plugins = ['my_list']", config_dir=config_dir)

        assert config.CONFIG.pm.has_plugin("my_list")

    def test_warn_uninstalled_plugin(self, tmp_config, caplog):
        """Warn the user if an enabled plugin cannot be loaded."""
        with caplog.at_level(logging.WARNING):
            tmp_config(
                settings="""enable_plugins = ["non_existent"]
            """
            )
            assert (
                "Plugin 'non_existent' is enabled in the configuration but could not be"
                " loaded. Is it installed?" in caplog.text
            )

        assert not config.CONFIG.pm.has_plugin("non_existent")


class ConfigPlugin:
    """Plugin that implements the config hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def add_config_validator(settings):
        """Add the `config_plugin` configuration option."""
        settings.validators.register(
            dynaconf.Validator("CONFIG_PLUGIN", must_exist=True)
        )

    @staticmethod
    @moe.hookimpl
    def plugin_registration():
        """Alter the `config_dir` at plugin registration."""
        config.CONFIG.pm.unregister(ConfigPlugin)
        config.CONFIG.pm.register(ConfigPlugin, "config2")


class TestHooks:
    """Test the config hook specifications."""

    def test_add_config_validator(self, tmp_config):
        """Ensure plugins can implement the `add_config_validator` hook."""
        config = tmp_config(
            settings="CONFIG_PLUGIN = 'hello!'",
            extra_plugins=[ExtraPlugin(ConfigPlugin, "config_plugin")],
        )

        assert config.settings.config_plugin == "hello!"

    def test_plugin_registration(self, tmp_config):
        """Ensure plugins can implement the `plugin_registration` hook."""
        config = tmp_config(
            """default_plugins = []
            CONFIG_PLUGIN = true
            """,
            extra_plugins=[ExtraPlugin(ConfigPlugin, "config_plugin")],
        )

        assert config.pm.has_plugin("config2")


class TestConfigOptions:
    """Test the various global configuration options."""

    def test_default_plugins(self, tmp_config):
        """Not required."""
        config = tmp_config()
        assert config.settings.default_plugins

    def test_library_path(self, tmp_config):
        """Not required."""
        config = tmp_config()
        assert config.settings.library_path

    @pytest.mark.win32
    def test_library_path_backslash(self, tmp_path, tmp_config):
        """Backslashes in library_path are allowed on Windows should use ''."""
        tmp_windows_path = str(tmp_path.resolve()).replace("/", "\\")
        config = tmp_config(
            settings=f"library_path = '{tmp_windows_path}'",
        )
        assert Path(config.settings.library_path).exists()
