"""User configuration of moe.

To avoid namespace confusion when using a variable named config, typical usage of this
module should just import the Config class directly::

    from moe.core.config import Config
    config = Config()

This class shouldn't be accessed normally by a plugin, it should instead be passed a
Config object through a hook.
"""

import importlib
import logging
import pathlib
import re

import dynaconf
import pluggy
import sqlalchemy

import alembic.command
import alembic.config
import moe
from moe.core.library.session import Session

log = logging.getLogger(__name__)

DEFAULT_PLUGINS = (
    "add",
    "info",
    "ls",
    "move",
    "rm",
)


class Hooks:
    """Config hooks."""

    @staticmethod
    @moe.hookspec
    def add_hooks(pluginmanager: pluggy.manager.PluginManager):
        """Add hookspecs to be registered.

        Args:
            pluginmanager: pluggy pluginmanager that will register the hookspec.

        Example:
            Inside of your hook implementation, write::
                from moe.plugins.add import Hooks  # noqa: WPS433, WPS442
                pluginmanager.add_hookspecs(Hooks)
        """

    @staticmethod
    @moe.hookspec
    def add_config_validator(settings: dynaconf.base.LazySettings):
        """Add a settings validator for the configuration file.

        Args:
            settings: moe's settings object.

        Example:
            Inside of your hook implementation, write::

                settings.validators.register(
                    Validator("MOVE.LIBRARY_PATH", must_exist=True)
                )

        See https://www.dynaconf.com/validation/#validation for more info.
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
        config_dir (pathlib.Path): Filesystem path of the configuration directory.
        config_file (pathlib.Path): Filesystem path of the configuration settings file.
        engine (sqlalchemy.engine.base.Engine): Database engine in use.
        pluginmanager (pluggy.manager.PluginManager): Manages plugin logic.
        plugins (List[str]): Enabled plugins.
        settings (dynaconf.base.LazySettings): User configuration settings.

    Example:
        In your plugin, to access the library_path setting (assuming a Config object
        named config)::

            config.settings.library_path

        See the dynaconf documentation for more info on reading settings variables.
        https://www.dynaconf.com/#reading-settings-variables
    """

    _default_config_dir = pathlib.Path().home() / ".config" / "moe"

    def __init__(
        self,
        config_dir: pathlib.Path = _default_config_dir,
        settings_filename: str = "config.toml",
    ):
        """Initializes the plugin manager and configuration directory.

        Args:
            config_dir: Filesystem path of the configuration directory. By default,
                this is where the settings and database files will reside.
            settings_filename: Name of the configuration settings file.
        """
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.config_file = self.config_dir / settings_filename
        self._read_config()

    def init_db(self, engine: sqlalchemy.engine.base.Engine = None):
        """Initializes the database.

        Moe uses sqlite by default.

        Args:
            engine: sqlalchemy database engine to use.
                Defaults to sqlite located at db_path.
        """
        db_path = self.config_dir / "library.db"

        if engine:
            self.engine = engine
        else:
            self.engine = sqlalchemy.create_engine("sqlite:///" + str(db_path))

        Session.configure(bind=self.engine)

        # create and update database tables
        alembic_cfg = alembic.config.Config("alembic.ini")
        alembic_cfg.attributes["configure_logger"] = False
        with self.engine.begin() as connection:
            alembic_cfg.attributes["connection"] = connection
            alembic.command.upgrade(alembic_cfg, "head")

        # create regular expression function for sqlite queries
        @sqlalchemy.event.listens_for(self.engine, "begin")
        def sqlite_engine_connect(conn):  # noqa: WPS430
            conn.connection.create_function("regexp", 2, _regexp, deterministic=True)

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

        self.pluginmanager.hook.add_config_validator(settings=self.settings)
        self.settings.validators.validate()

    def _setup_plugins(self):
        """Setup pluginmanager and hook logic."""
        self.pluginmanager = pluggy.PluginManager("moe")

        # need to validate `config` specific settings separately
        # this is so we have access to the 'default_plugins' setting
        self.pluginmanager.register(moe.core.config)
        self.pluginmanager.add_hookspecs(Hooks)
        self.pluginmanager.hook.add_config_validator(settings=self.settings)
        self.settings.validators.validate()

        # register plugin hookimpls for all enabled plugins
        self.plugins = self.settings.default_plugins
        for plugin in self.plugins:
            self.pluginmanager.register(
                importlib.import_module(f"moe.plugins.{plugin}")
            )

        # register plugin hookspecs for all plugins
        self.pluginmanager.hook.add_hooks(pluginmanager=self.pluginmanager)
