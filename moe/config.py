"""User configuration of moe."""

import pathlib

import sqlalchemy

from moe.lib import library


class Config:
    """Reads and/or defines all the necessary configuration options for moe.

    Also initializes the database and will be passed to various hooks
    throughout a single run of moe.

    Attributes:
        config_dir (pathlib.Path): Configuration directory.
        db_path (pathlib.Path): Path of the database file.
    """

    def __init__(
        self,
        config_dir: pathlib.Path = pathlib.Path().home() / ".config" / "moe",
        db_dir: pathlib.Path = None,
        db_filename: str = "library.db",
        engine: sqlalchemy.engine.base.Engine = None,
    ):
        """Read configuration.

        Args:
            config_dir: Path of the configuration directory.
            db_dir: Path of the database directory. Defaults to config_dir.
            db_filename: Name of the database file.
            engine: sqlalchemy database engine to use. Defaults to sqlite
                located at db_dir / db_filename.
        """
        self.config_dir = config_dir
        db_dir = db_dir if db_dir else config_dir
        self.db_path = db_dir / db_filename

        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
        if not db_dir.exists():
            db_dir.mkdir(parents=True)

        # initialize db
        if not engine:
            engine = sqlalchemy.create_engine("sqlite:///" + str(self.db_path))
        library.Session.configure(bind=engine)
        library.Base.metadata.create_all(engine)  # create tables if they don't exist
