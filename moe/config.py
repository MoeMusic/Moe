"""User configuration of moe."""

import pathlib

import sqlalchemy

from moe.lib import library


class Config:
    """Reads and/or defines all the necessary configuration options for moe.

    Also initializes the database and will be passed to various hooks
    throughout a single run of moe.
    """

    def __init__(self, config_path: pathlib.Path = None, db_path: pathlib.Path = None):
        """Read configuration.

        Args:
            config_path: path to configuration file
            db_path: path to database file
        """
        self.path = config_path if config_path else pathlib.Path().home() / ".config"
        self.db_path = db_path if db_path else self.path / "library.db"

        # initialize db
        engine = sqlalchemy.create_engine("sqlite:///" + str(self.db_path))
        library.Session.configure(bind=engine)
        library.Base.metadata.create_all(engine)  # create tables if they don't exist
