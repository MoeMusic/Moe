"""Tests the sqlalchemy session generator."""

import pytest

import moe
from moe.library.session import session_scope
from moe.library.track import Track


class TestSessionScope:
    """Test the contextual generator."""

    @pytest.mark.integration
    def test_commit_on_systemexit(self, real_track, tmp_config):
        """If SystemExit intentionally raised, still commit the session."""
        cli_args = ["add", "bad file", str(real_track.path)]
        config = tmp_config(settings='default_plugins = ["add", "cli"]')

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, config)

        assert error.value.code != 0

        with session_scope() as session:
            session.query(Track).one()
