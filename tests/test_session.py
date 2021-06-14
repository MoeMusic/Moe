"""Tests the sqlalchemy session generator."""

from unittest.mock import patch

import pytest

from moe import cli
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
