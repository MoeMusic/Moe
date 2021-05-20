"""User configuration of moe.

To avoid namespace confusion when using a variable named config, typical usage of this
module should just import the Config class directly::

    from moe.core.config import Config
    config = Config()

This class shouldn't be accessed normally by a plugin, it should instead be passed a
Config object through a hook.

Attributes:
    DEFAULT_PLUGINS: Plugins that are enabled by default.
        This list should only contain plugins that are a net positive in the vast
        majority of use cases.
"""

import importlib
import logging
import pathlib
import re

import pluggy
import sqlalchemy
from dynaconf import Dynaconf

from moe.core.library.session import Base, Session

log = logging.getLogger(__name__)

DEFAULT_PLUGINS = (
    "add",
    "info",
    "ls",
    "rm",
)


class Config:
    """Initializes moe configuration settings and database.

    Database initialization will not happen on `__init__()`. You must call `init_db()`
    explicitly.

    Attributes:
        config_dir (pathlib.Path): Configuration directory.
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

    def __init__(self, config_dir: pathlib.Path = _default_config_dir):
        """Initializes the plugin manager and configuration settings.

        Args:
            config_dir: Filesystem path of the configuration directory. By default,
                this is where the settings and database files will reside.
        """
        self.plugins = DEFAULT_PLUGINS

        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.read_config()

        self.pluginmanager = pluggy.PluginManager("moe")
        for plugin in self.plugins:
            self.pluginmanager.register(
                importlib.import_module(f"moe.plugins.{plugin}")
            )

    def read_config(self):
        """Reads the user configuration settings.

        Searches for a configuration file at `config_dir / "config.toml"`.

        Raises:
            SystemExit: No config file found.
        """
        config_file = self.config_dir / "config.toml"
        config_file.touch(exist_ok=True)

        # use dynaconf to handle config files
        self.settings = Dynaconf(
            envvar_prefix="MOE",  # export envvars with `export MOE_FOO=bar`
            settings_file=str(config_file.resolve()),
        )

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
        Base.metadata.create_all(self.engine)  # creates tables

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
