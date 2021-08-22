"""Tests the CLI."""

from unittest.mock import Mock

import pytest

import moe
import moe.cli
from moe.config import ExtraPlugin, MoeSession
from moe.library.track import Track


def test_no_args():
    """Test exit if 0 subcommands given."""
    with pytest.raises(SystemExit) as error:
        moe.cli._parse_args([], Mock())

    assert error.value.code != 0


def test_commit_on_systemexit(real_track, tmp_config):
    """If SystemExit intentionally raised, still commit the session."""
    cli_args = ["add", "bad file", str(real_track.path)]
    config = tmp_config(settings='default_plugins = ["add", "cli"]', tmp_db=True)

    with pytest.raises(SystemExit) as error:
        moe.cli.main(cli_args, config)

    assert error.value.code != 0

    session = MoeSession()
    with session.begin():
        session.query(Track).one()


def test_default_config(tmp_config, real_track):
    """Ensure we can initialize a configuration with its default values."""
    cli_args = ["list", "*"]
    config = tmp_config(init_db=True)

    session = MoeSession()
    with session.begin():
        session.add(real_track)

    moe.cli.main(cli_args, config)


class CLIPlugin:
    """Plugin that implements the CLI hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def add_command(cmd_parsers):
        """Add a `cli` command to Moe."""

        def say_hello(config, args):
            print("hello")  # noqa: WPS421

        cli_parser = cmd_parsers.add_parser("cli")
        cli_parser.add_argument("cli")
        cli_parser.set_defaults(func=say_hello)


class TestHookSpecs:
    """Test the cli hook specifications."""

    def test_add_command(self, capsys, tmp_config):
        """Ensure plugins can properly implement the `add_command` hook."""
        cli_args = ["cli", "1 2 3 4"]
        config = tmp_config(
            settings='default_plugins = ["cli"]',
            extra_plugins=[ExtraPlugin(CLIPlugin, "cli_plugin")],
        )
        moe.cli.main(cli_args, config)

        assert capsys.readouterr().out == "hello\n"
