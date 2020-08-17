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
import sqlite3

import sqlalchemy

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
        plugins (List[str]): Enabled plugins.
        engine (sqlalchemy.engine.base.Engine): Database engine in use.
    """

    _default_config_dir = pathlib.Path().home() / ".config" / "moe"

    def __init__(
        self,
        config_dir: pathlib.Path = _default_config_dir,
        db_dir: pathlib.Path = None,
        db_filename: str = "library.db",
        engine: sqlalchemy.engine.base.Engine = None,
    ):
        """Reads the configuration and initializes the database.

        Args:
            config_dir: Path of the configuration directory.
            db_dir: Path of the database directory. Defaults to config_dir.
            db_filename: Name of the database file.
            engine: sqlalchemy database engine to use.
                Defaults to sqlite located at db_dir / db_filename.
        """
        self.config_dir = config_dir
        db_dir = db_dir if db_dir else config_dir
        db_path = db_dir / db_filename
        self.plugins = DEFAULT_PLUGINS

        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
        if not db_dir.exists():
            db_dir.mkdir(parents=True)

        if not engine:
            engine = sqlalchemy.create_engine("sqlite:///" + str(db_path))
        self._db_init(engine)

    def _db_init(self, engine: sqlalchemy.engine.base.Engine):
        """Initializes the database.

        Moe uses sqlite by default. Current (known) limitations with using other dbs:
            1. Track and album fields aren't defined with character limits.
            2. Support for the `regexp` operator used for regex queries.

        Args:
            engine: Database engine to create.
        """
        self.engine = engine

        library.Session.configure(bind=engine)
        library.Base.metadata.create_all(engine)  # create tables if they don't exist

        # create regular expression function for sqlite queries
        @sqlalchemy.event.listens_for(engine, "begin")
        def sqlite_engine_connect(conn):  # noqa: WPS430
            try:
                conn.connection.create_function(
                    "regexp", 2, _regexp, deterministic=True
                )
            except sqlite3.NotSupportedError:
                # determinstic flag is only supported by SQLite>=3.8.3
                conn.connection.create_function("regexp", 2, _regexp)

        def _regexp(pattern: str, col_value: str) -> bool:  # noqa: WPS430
            """Use the python re module for sqlite regular expression functionality.

            Args:
                pattern: Regular expression pattern.
                col_value: Column value to match against.

            Returns:
                Whether or not the match was successful.
            """
            return re.search(pattern, col_value) is not None
