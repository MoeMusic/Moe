"""Tests the CLI."""

import copy
import datetime
import random
from unittest.mock import Mock, patch

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
            print("hello")

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


class TestChoicePrompt:
    """Test `choice_prompt`."""

    def test_prompt_choice_return(self, mock_track):
        """The proper PromptChoice is returned when selected."""
        mock_choice1 = moe.cli.PromptChoice("title a", "a", lambda a: None)
        mock_choice2 = moe.cli.PromptChoice("title b", "b", lambda b: None)
        mock_q = Mock()
        mock_q.ask.return_value = "a"

        assert mock_track.title != "a"

        with patch("moe.cli.questionary.rawselect", return_value=mock_q):
            prompt_choice = moe.cli.choice_prompt([mock_choice1, mock_choice2])
            prompt_choice.func(mock_track)

            assert prompt_choice == mock_choice1

    def test_invalid_input(self):
        """Raise SystemExit if an improper user choice is made."""
        mock_choice = moe.cli.PromptChoice("title b", "b", lambda b: None)
        mock_q = Mock()
        mock_q.ask.return_value = "a"

        with patch("moe.cli.questionary.rawselect", return_value=mock_q):
            with pytest.raises(SystemExit) as error:
                moe.cli.choice_prompt([mock_choice])

        assert error.value.code != 0


class TestFmtAlbumChanges:
    """Test formatting of album changes.

    These test cases aren't specifically testing what is output, as that
    is more of an implementation detail and harder to test than it's worth. Rather,
    these test cases are used to help see what is being printed for various scenarios
    (add ``assert 0`` to the end of any test case to see it's output to stdout).
    """

    def test_full_diff_album(self, mock_album):
        """Print prompt for fully different albums."""
        old_album = mock_album
        new_album = copy.deepcopy(mock_album)
        old_album.tracks[0].title = "really really long old title"
        new_album.title = "new title"
        new_album.artist = "new artist"
        new_album.date = datetime.date(1999, 12, 31)
        new_album.mb_album_id = "1234"

        for track in new_album.tracks:
            track.title = "new title"

        assert old_album is not new_album

        print(moe.cli.fmt_album_changes(old_album, new_album))

    def test_unmatched_tracks(self, mock_album):
        """Print prompt for albums with non-matching tracks."""
        old_album = mock_album
        new_album = copy.deepcopy(mock_album)

        for track in old_album.tracks:
            track.track_num = random.randint(1, 1000)

        assert old_album is not new_album

        print(moe.cli.fmt_album_changes(old_album, new_album))

    def test_multi_disc_album(self, mock_album, mock_track_factory):
        """Prompt supports multi_disc albums."""
        mock_album.disc_total = 2
        mock_album.tracks[1].disc = 2
        mock_album.tracks[1].track_num = 1
        mock_track_factory(track_num=2, album=mock_album)
        new_album = copy.deepcopy(mock_album)

        print(moe.cli.fmt_album_changes(mock_album, new_album))
