"""User configuration of moe.

To avoid namespace confusion when using a variable named config, typical usage of this
module should just import the Config class directly::

    from moe.core.config import Config
    config = Config()

This class shouldn't be accessed normally by a plugin, it should instead be passed a
Config object through a hook.
"""

import importlib
import importlib.util  # noqa: WPS458
import logging
import os
import re
import sys
from pathlib import Path
from typing import cast

import dynaconf
import pluggy
import sqlalchemy

import alembic.command
import alembic.config
import moe
from moe.core.library.session import Session

__all__ = ["Config", "Hooks"]

log = logging.getLogger("moe.config")

DEFAULT_PLUGINS = (
    "add",
    "edit",
    "info",
    "list",
    "move",
    "musicbrainz",
    "remove",
    "write",
)


class Hooks:
    """Config hooks."""

    @staticmethod
    @moe.hookspec
    def add_config_validator(settings: dynaconf.base.LazySettings):
        """Add a settings validator for the configuration file.

        Args:
            settings: Moe's settings.

        Example:
            Inside your hook implementation::

                settings.validators.register(
                    Validator("MOVE.LIBRARY_PATH", must_exist=True)
                )

        See https://www.dynaconf.com/validation/#validation for more info.
        """

    @staticmethod
    @moe.hookspec
    def add_hooks(plugin_manager: pluggy.manager.PluginManager):
        """Add hookspecs to be registered to Moe.

        Args:
            plugin_manager: PluginManager that registers the hookspec.

        Example:
            Inside your hook implementation::

                from moe.plugins.add import Hooks  # noqa: WPS433, WPS442
                plugin_manager.add_hookspecs(Hooks)
        """


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    settings.validators.register(
        dynaconf.Validator("DEFAULT_PLUGINS", default=list(DEFAULT_PLUGINS))
    )


class Config:
    """Initializes moe configuration settings and database.

    Note:
        `init_db()` is not included in `__init__()` for testing purposes.

    Attributes:
        config_dir (Path): Filesystem path of the configuration directory.
        config_file (Path): Filesystem path of the configuration settings file.
        engine (sqlalchemy.engine.base.Engine): Database engine in use.
        plugin_manager (pluggy.manager.PluginManager): Manages plugin logic.
        plugins (List[str]): Enabled plugins.
        settings (dynaconf.base.LazySettings): User configuration settings.

    Example:
        In your plugin, to access the library_path setting (assuming a Config object
        named config)::

            config.settings.library_path

        See the dynaconf documentation for more info on reading settings variables.
        https://www.dynaconf.com/#reading-settings-variables
    """

    def __init__(
        self,
        config_dir: Path = Path.home() / ".config" / "moe",
        settings_filename: str = "config.toml",
    ):
        """Initializes the plugin manager and configuration directory.

        Args:
            config_dir: Filesystem path of the configuration directory where the
                settings and database files will reside. The environment variable
                ``MOE_CONFIG_DIR`` has precedence in setting this.
            settings_filename: Name of the configuration settings file.
        """
        try:
            self.config_dir = Path(os.environ["MOE_CONFIG_DIR"])
        except KeyError:
            self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.config_file = self.config_dir / settings_filename
        self._read_config()

    def init_db(
        self, engine: sqlalchemy.engine.base.Engine = None, create_tables: bool = True
    ):
        """Initializes the database.

        Moe uses sqlite by default.

        Args:
            engine: sqlalchemy database engine to use.
                Defaults to sqlite located at db_path.
            create_tables: Whether or not to create and update the db tables.
                If doing db migrations manually, e.g. in alembic, this shuold be False.
        """
        db_path = self.config_dir / "library.db"

        if engine:
            self.engine = engine
        else:
            self.engine = sqlalchemy.create_engine("sqlite:///" + str(db_path))

        Session.configure(bind=self.engine)

        # create and update database tables
        if create_tables:
            config_path = Path(__file__)
            alembic_cfg = alembic.config.Config(
                config_path.parents[2] / "alembic" / "alembic.ini"
            )
            alembic_cfg.attributes["configure_logger"] = False
            with self.engine.begin() as connection:
                alembic_cfg.attributes["connection"] = connection
                alembic.command.upgrade(alembic_cfg, "head")

        # create regular expression function for sqlite queries
        @sqlalchemy.event.listens_for(self.engine, "begin")  # noqa: WPS430
        def sqlite_engine_connect(conn):  # noqa: WPS430
            if (sys.version_info.major, sys.version_info.minor) < (3, 8):
                conn.connection.create_function("regexp", 2, _regexp)
            else:
                conn.connection.create_function(
                    "regexp", 2, _regexp, deterministic=True
                )

        def _regexp(pattern: str, col_value) -> bool:  # noqa: WPS430
            """Use the python re module for sqlite regular expression functionality.

            Args:
                pattern: Regular expression pattern.
                col_value: Column value to match against. The match will be against
                    the str of the value.

            Returns:
                Whether or not the match was successful.
            """
            return re.search(pattern, str(col_value), re.IGNORECASE) is not None

    def _read_config(self):
        """Reads the user configuration settings.

        Searches for a configuration file at `config_dir / "config.toml"`.

        Raises:
            SystemExit: No config file found.
        """
        self.config_file.touch(exist_ok=True)

        self.settings = dynaconf.Dynaconf(
            envvar_prefix="MOE",  # export envvars with `export MOE_FOO=bar`
            settings_file=str(self.config_file.resolve()),
        )

        self._setup_plugins()

        self.plugin_manager.hook.add_config_validator(settings=self.settings)
        self.settings.validators.validate()

    def _setup_plugins(self):
        """Setup plugin_manager and hook logic."""
        self.plugin_manager = pluggy.PluginManager("moe")

        # need to validate `config` specific settings separately so we have access to
        # the 'default_plugins' setting
        self.plugin_manager.register(moe.core.config, name="config")
        self.plugin_manager.add_hookspecs(Hooks)
        self.plugin_manager.hook.add_config_validator(settings=self.settings)
        self.settings.validators.validate()

        # cli is always registered
        self.plugin_manager.register(importlib.import_module("moe.cli"), name="cli")

        # register plugin hookimpls for all enabled plugins
        self.plugins = self.settings.default_plugins
        internal_plugin_path = Path(__file__).resolve().parents[1] / "plugins"
        self._register_plugin_dir(internal_plugin_path)

        # register plugin hookspecs for all plugins
        self.plugin_manager.hook.add_hooks(plugin_manager=self.plugin_manager)

    def _register_plugin_dir(self, plugin_dir: Path):
        """Registers plugins in a given directory.

        Assumes each plugin is a single file named ``{plugin_name}.py``, or is a
        package directory named ``{plugin_name}/``. If the plugin is a package, it will
        register each file in the dir as a new plugin.

        Only registers plugins that are enabled in the configuration.

        Args:
            plugin_dir: Path to search for plugin modules or packages.
        """
        for plugin_path in plugin_dir.iterdir():
            if plugin_path.stem in self.plugins:
                self._register_plugin_path(plugin_path)

    def _register_plugin_path(self, plugin_path: Path):
        """Registers a plugin file or directory."""
        if (
            plugin_path.is_file()
            and not plugin_path.name.startswith("_")
            and plugin_path.suffix == ".py"
        ):
            plugin_spec = importlib.util.spec_from_file_location(
                plugin_path.stem, plugin_path
            )
            if plugin_spec:
                plugin_module = importlib.util.module_from_spec(plugin_spec)
                cast(importlib.abc.Loader, plugin_spec.loader).exec_module(
                    plugin_module
                )

                self.plugin_manager.register(plugin_module)
        elif plugin_path.is_dir():
            # register every file in a plugin's directory
            for path in plugin_path.iterdir():
                self._register_plugin_path(path)
