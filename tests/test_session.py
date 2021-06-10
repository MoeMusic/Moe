"""Tests the sqlalchemy session generator."""

from unittest.mock import patch

import pytest

from moe import cli
from moe.core.library.session import session_scope
from moe.core.library.track import Album, Track


@pytest.mark.integration
class TestSessionScope:
    """Test the contextual generator."""

    def test_commit_on_systemexit(self, tmp_config):
        """If SystemExit intentionally raised, still commit the session."""
        cli_args = ["moe", "add", "bad_file", "tests/resources/album/"]
        config = tmp_config(settings='default_plugins = ["add"]')

        with patch("sys.argv", cli_args):
            with patch("moe.cli.Config", return_value=config):
                with pytest.raises(SystemExit) as error:
                    cli.main()

        assert error.value.code != 0

        with session_scope() as session:
            album = session.query(Album).one()

            tracks = session.query(Track)
            for track in tracks:
                assert track in album.tracks

            assert len(album.tracks) > 1
