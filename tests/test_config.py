"""Tests configuration."""

from unittest.mock import patch

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


class TestRegisterPluginDir:
    """Test registering plugins from a directory."""

    def test_files(self, tmp_config, tmp_path):
        """We can register plugin files within a directory."""
        plugins = ["add", "move"]
        tmp_settings = f"default_plugins = {plugins}"
        config = tmp_config(tmp_settings)
        (tmp_path / "add.py").touch()
        (tmp_path / "move.py").touch()

        # start with no plugins registered
        for _, plugin in config.plugin_manager.list_name_plugin():
            config.plugin_manager.unregister(plugin)

        config._register_plugin_dir(tmp_path)
        registered_plugins = {
            plugin[0] for plugin in config.plugin_manager.list_name_plugin()
        }
        assert set(plugins) == registered_plugins

    def test_dirs(self, tmp_config, tmp_path):
        """We can register plugin package directories within a directory.

        Each file within the appropriate plugin directory should be added.
        """
        plugins = ["add", "move"]
        tmp_settings = f"default_plugins = {plugins}"
        config = tmp_config(tmp_settings)

        add_path = tmp_path / "add"
        add_path.mkdir()
        (add_path / "my_add.py").touch()
        (add_path / "my_add2.py").touch()
        (tmp_path / "move.py").touch()

        # start with no plugins registered
        for _, plugin in config.plugin_manager.list_name_plugin():
            config.plugin_manager.unregister(plugin)

        config._register_plugin_dir(tmp_path)

        registered_plugins = [
            plugin[0] for plugin in config.plugin_manager.list_name_plugin()
        ]

        assert set(registered_plugins) == {"move", "my_add", "my_add2"}

    def test_nested_dirs(self, tmp_config, tmp_path):
        """We can register plugin package directories containing nested directories.

        Each file within the appropriate plugin directory should be added.
        """
        plugins = ["add", "move"]
        tmp_settings = f"default_plugins = {plugins}"
        config = tmp_config(tmp_settings)

        add_path = tmp_path / "add" / "nested" / "direc" / "tories"
        add_path.mkdir(parents=True)
        (add_path / "my_add.py").touch()
        (add_path / "my_add2.py").touch()
        (tmp_path / "move.py").touch()

        # start with no plugins registered
        for _, plugin in config.plugin_manager.list_name_plugin():
            config.plugin_manager.unregister(plugin)

        config._register_plugin_dir(tmp_path)

        registered_plugins = [
            plugin[0] for plugin in config.plugin_manager.list_name_plugin()
        ]

        assert set(registered_plugins) == {"move", "my_add", "my_add2"}

    def test_wrong_plugin_name(self, tmp_config, tmp_path):
        """Don't add any files or directories that don't match our enabled plugins."""
        plugins = ["not_add", "not_move"]
        tmp_settings = f"default_plugins = {plugins}"
        config = tmp_config(tmp_settings)

        add_path = tmp_path / "add"
        add_path.mkdir()
        (add_path / "add.py").touch()
        (add_path / "my_add2.py").touch()
        (tmp_path / "move.py").touch()

        # start with no plugins registered
        for _, plugin in config.plugin_manager.list_name_plugin():
            config.plugin_manager.unregister(plugin)

        config._register_plugin_dir(tmp_path)

        registered_plugins = [
            plugin[0] for plugin in config.plugin_manager.list_name_plugin()
        ]

        assert not registered_plugins
