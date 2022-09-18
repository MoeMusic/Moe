"""Tests the CLI."""

from unittest.mock import patch

import pytest

import moe
import moe.cli
from moe import config
from moe.library.track import Track
from tests.conftest import track_factory


def test_no_args(tmp_config):
    """Test exit if 0 subcommands given."""
    tmp_config()
    with pytest.raises(SystemExit) as error:
        moe.cli._parse_args([])

    assert error.value.code != 0


def test_commit_on_systemexit(tmp_config):
    """If SystemExit intentionally raised, still commit the session."""
    tmp_config(settings='default_plugins = ["add", "cli"]', tmp_db=True)
    track = track_factory(exists=True)
    cli_args = ["add", "bad file", str(track.path)]

    with pytest.raises(SystemExit) as error:
        moe.cli.main(cli_args)

    assert error.value.code != 0

    session = config.MoeSession()
    with session.begin():
        session.query(Track).one()


def test_default_config(tmp_config):
    """Ensure we can initialize a configuration with its default values."""
    cli_args = ["list", "*"]
    tmp_config(init_db=True)
    track = track_factory(exists=True)

    session = config.MoeSession()
    with session.begin():
        session.add(track)

    moe.cli.main(cli_args)


def test_config_validation_error():
    """Raise SystemExit if the config fails to pass its validation."""
    config.CONFIG = None
    with patch.object(
        moe.cli, "Config", autospec=True, side_effect=config.ConfigValidationError
    ):
        with pytest.raises(SystemExit) as error:
            moe.cli.main(["-h"])

    assert error.value.code != 0


class CLIPlugin:
    """Plugin that implements the CLI hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def add_command(cmd_parsers):
        """Add a `cli` command to Moe."""

        def say_hello(args):
            print("hello")

        cli_parser = cmd_parsers.add_parser("cli")
        cli_parser.add_argument("cli")
        cli_parser.set_defaults(func=say_hello)


class TestHookSpecs:
    """Test the cli hook specifications."""

    def test_add_command(self, capsys, tmp_config):
        """Ensure plugins can properly implement the `add_command` hook."""
        cli_args = ["cli", "1 2 3 4"]
        tmp_config(
            settings='default_plugins = ["cli"]',
            extra_plugins=[config.ExtraPlugin(CLIPlugin, "cli_plugin")],
        )
        moe.cli.main(cli_args)

        assert capsys.readouterr().out == "hello\n"
