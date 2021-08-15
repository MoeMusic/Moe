"""Tests the CLI."""

from unittest.mock import Mock

import pytest

import moe
import moe.cli
from moe.config import MoeSession
from moe.library.track import Track


def test_no_args():
    """Test exit if 0 subcommands given."""
    with pytest.raises(SystemExit) as error:
        moe.cli._parse_args([], Mock())

    assert error.value.code != 0


@pytest.mark.integration
def test_commit_on_systemexit(real_track, tmp_config):
    """If SystemExit intentionally raised, still commit the session."""
    cli_args = ["add", "bad file", str(real_track.path)]
    config = tmp_config(settings='default_plugins = ["add", "cli"]', init_db=True)

    with pytest.raises(SystemExit) as error:
        moe.cli.main(cli_args, config)

    assert error.value.code != 0

    session = MoeSession()
    with session.begin():
        session.query(Track).one()
