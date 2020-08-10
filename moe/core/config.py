"""User configuration of moe.

To avoid namespace confusion when using a variable named config,
typical usage of this module should just import the Config class directly.

    >>> from moe.core.config import Config
    >>> config = Config()
"""

import pathlib
from typing import List

import sqlalchemy

from moe.core import library

DEFAULT_PLUGINS = [
    "add",
]
"""Plugins that are enabled by default.

This list should only contain plugins that are a net positive in the vast majority
of use cases.
"""


class Config:
    """Reads and/or defines all the necessary configuration options for moe.

    Also initializes the database and will be passed to various hooks
    throughout a single run of moe.

    Attributes:
        config_dir (pathlib.Path): Configuration directory.
        db_path (pathlib.Path): Path of the database file.
        plugins (List[str]): Enabled plugins.
    """

    def __init__(
        self,
        config_dir: pathlib.Path = pathlib.Path().home() / ".config" / "moe",
        db_dir: pathlib.Path = None,
        db_filename: str = "library.db",
        engine: sqlalchemy.engine.base.Engine = None,
        default_plugins: List[str] = DEFAULT_PLUGINS,
    ):
        """Read configuration.

        Args:
            config_dir: Path of the configuration directory.
            db_dir: Path of the database directory. Defaults to config_dir.
            db_filename: Name of the database file.
            engine: sqlalchemy database engine to use. Defaults to sqlite
                located at db_dir / db_filename.
            default_plugins: Default plugins to enable. These will be enabled
                in addition to any plugins specified by the config file.
        """
        self.config_dir = config_dir
        db_dir = db_dir if db_dir else config_dir
        self.db_path = db_dir / db_filename
        self.plugins = default_plugins

        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
        if not db_dir.exists():
            db_dir.mkdir(parents=True)

        # initialize db
        if not engine:
            engine = sqlalchemy.create_engine("sqlite:///" + str(self.db_path))
        library.Session.configure(bind=engine)
        library.Base.metadata.create_all(engine)  # create tables if they don't exist
