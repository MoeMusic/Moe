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

import pathlib
import re

import sqlalchemy
import yaml

from moe.core import library

DEFAULT_PLUGINS = (
    "add",
    "info",
    "ls",
    "rm",
)


class Config:
    """Reads and/or defines all the necessary configuration options for moe.

    Also initializes the database and will be passed to various hooks
    throughout a single run of moe.

    Attributes:
        config_dir (pathlib.Path): Configuration directory.
        config_path (pathlib.Path): Configuration file.
        plugins (List[str]): Enabled plugins.
        engine (sqlalchemy.engine.base.Engine): Database engine in use.
    """

    _default_config_dir = pathlib.Path().home() / ".config" / "moe"

    def __init__(
        self,
        config_dir: pathlib.Path = _default_config_dir,
        config_path: pathlib.Path = None,
        db_path: pathlib.Path = None,
        engine: sqlalchemy.engine.base.Engine = None,
    ):
        """Reads the configuration and initializes the database.

        Args:
            config_dir: Path of the configuration directory.
            config_path: Path of the config file.
                Defaults to config_dir / "config.yaml".
            db_path: Path of the database file.
                Defaults to config_dir / "library.db".
            engine: sqlalchemy database engine to use.
                Defaults to sqlite located at db_dir / db_filename.
        """
        self.config_dir = config_dir
        self.config_path = config_path if config_path else config_dir / "config.yaml"
        db_path = db_path if db_path else config_dir / "library.db"
        self.plugins = DEFAULT_PLUGINS

        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
        if not self.config_path.exists():
            self.config_path.touch()

        self._read_config(self.config_path.read_text())

        if engine:
            self.engine = engine
        else:
            self.engine = sqlalchemy.create_engine("sqlite:///" + str(db_path))
        self._db_init()

    def _read_config(self, config_stream=None):
        """Read the user configuration file.

        Args:
            config_stream: Configuration stream to read. Can be anything
                read by `yaml.load()`.
                Defaults to reading the configuration file at `self.config_path`.
        """
        config_stream = config_stream if config_stream else self.config_path.read_text()
        self.yaml = yaml.safe_load(config_stream)

    def _db_init(self):
        """Initializes the database.

        Moe uses sqlite by default. Current (known) limitations with using other dbs:
            1. Track and album fields aren't defined with character limits.
            2. Support for the `regexp` operator used for regex queries.
        """
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
