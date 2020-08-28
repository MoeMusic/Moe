"""User configuration of moe.

To avoid namespace confusion when using a variable named config,
typical usage of this module should just import the Config class directly.

    >>> from moe.core.config import Config
    >>> config = Config()

Attributes:
    DEFAULT_PLUGINS: Plugins that are enabled by default.

    This list should only contain plugins that are a net positive in the vast majority
    of use cases.
"""

import logging
import pathlib
import re

import sqlalchemy
import yaml

from moe.core import library

log = logging.getLogger(__name__)

DEFAULT_PLUGINS = (
    "add",
    "info",
    "ls",
    "rm",
)


class Config:
    """Reads and/or defines all the necessary configuration options for moe.

    The database and config file will not be read on init. `read_config` and
    `init_db` must be explicitly called.

    TODO: determine type of config object once we have a sample config
    Attributes:
        config: User configuration in use.
        config_dir (pathlib.Path): Configuration directory.
        engine (sqlalchemy.engine.base.Engine): Database engine in use.
        plugins (List[str]): Enabled plugins.
    """

    _default_config_dir = pathlib.Path().home() / ".config" / "moe"

    def __init__(self, config_dir: pathlib.Path = _default_config_dir):
        """Reads the configuration and initializes the database.

        Args:
            config_dir: Path of the configuration directory.
        """
        self.config_dir = config_dir
        self.plugins = DEFAULT_PLUGINS

        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)

    def read_config(self, config_stream=None):
        """Reads a given yaml configuration.

        Args:
            config_stream: Configuration stream to read.
                Can be anything read by `yaml.load()`.
                Defaults to reading a config file at `config_dir / "config.yaml"`.

        Raises:
            SystemExit: Couldn't read the default configuration file.
        """
        if not config_stream:
            config_file = self.config_dir / "config.yaml"

            try:
                config_stream = config_file.read_text()
            except FileNotFoundError:
                log.error(f"Configuration file '{config_file}' does not exist.")
                raise SystemExit(1)

        self.config = yaml.safe_load(config_stream)

    def init_db(
        self,
        db_path: pathlib.Path = None,
        engine: sqlalchemy.engine.base.Engine = None,
    ):
        """Initializes the database.

        Moe uses sqlite by default. Current (known) limitations with using other dbs:
            1. Track and album fields aren't defined with character limits.
            2. Support for the `regexp` operator used for regex queries.

        Args:
            db_path: Path of the database file.
                Defaults to config_dir / "library.db".
            engine: sqlalchemy database engine to use.
                Defaults to sqlite located at db_dir / db_path.
        """
        db_path = db_path if db_path else self.config_dir / "library.db"

        if engine:
            self.engine = engine
        else:
            self.engine = sqlalchemy.create_engine("sqlite:///" + str(db_path))

        library.Session.configure(bind=self.engine)
        library.Base.metadata.create_all(self.engine)  # creates tables

        # create regular expression function for sqlite queries
        @sqlalchemy.event.listens_for(self.engine, "begin")
        def sqlite_engine_connect(conn):  # noqa: WPS430
            conn.connection.create_function("regexp", 2, _regexp, deterministic=True)

        def _regexp(pattern: str, col_value: str) -> bool:  # noqa: WPS430
            """Use the python re module for sqlite regular expression functionality.

            Args:
                pattern: Regular expression pattern.
                col_value: Column value to match against.

            Returns:
                Whether or not the match was successful.
            """
            return re.search(pattern, col_value) is not None
