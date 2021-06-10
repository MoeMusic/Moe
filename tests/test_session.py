"""Tests the sqlalchemy session generator."""

from unittest.mock import MagicMock, patch

import pytest
import sqlalchemy

from moe import cli
from moe.core.config import Config
from moe.core.library.session import session_scope
from moe.core.library.track import Track


class TestSessionScope:
    """Test the contextual generator."""

    @pytest.mark.integration
    def test_commit_on_systemexit(self, real_track, tmp_config):
        """If SystemExit intentionally raised, still commit the session."""
        cli_args = ["moe", "add", "bad_file", str(real_track.path)]
        config = tmp_config(settings='default_plugins = ["add"]')

        with patch("sys.argv", cli_args):
            with patch("moe.cli.Config", return_value=config):
                with pytest.raises(SystemExit) as error:
                    cli.main()

        assert error.value.code != 0

        with session_scope() as session:
            session.query(Track).one()

    def test_write_tags(self, real_track):
        """If a Track changes, write its new fields to file before committing."""
        real_track.album = "Bigger, Better, Faster, More!"

        engine = sqlalchemy.create_engine("sqlite:///:memory:")

        config = Config(config_dir=MagicMock())
        config.init_db(engine=engine)

        real_track_path = real_track.path
        with session_scope() as session:
            session.add(real_track)

        new_track = Track.from_tags(path=real_track_path)
        assert new_track.album == "Bigger, Better, Faster, More!"
