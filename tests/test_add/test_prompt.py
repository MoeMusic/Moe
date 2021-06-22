"""Tests the add plugin interactive prompt."""

import copy
import random
from unittest.mock import Mock, patch

from moe.plugins.add import prompt


class TestRunPrompt:
    """Test running the prompt."""

    def test_same_album(self, capsys, mock_album):
        """Don't do anything if no album changes."""
        new_album = copy.deepcopy(mock_album)
        assert mock_album is not new_album

        prompt.run_prompt(Mock(), Mock(), mock_album, new_album)

        captured_txt = capsys.readouterr()
        assert not captured_txt.out

    def test_apply_changes(self, mock_album, tmp_config):
        """If selected, apply the changes to the old album."""
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        with patch("builtins.input", side_effect="a"):
            add_album = prompt.run_prompt(config, Mock(), mock_album, new_album)

        assert add_album.title == new_album.title

    def test_default_whitespace(self, mock_album, tmp_config):
        """If whitespace input, apply the changes to the old album."""
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        with patch("builtins.input", side_effect=" "):
            add_album = prompt.run_prompt(config, Mock(), mock_album, new_album)

        assert add_album.title == new_album.title

    def test_default_empty(self, mock_album, tmp_config):
        """If no input, apply the changes to the old album."""
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        with patch("builtins.input", lambda _: ""):
            add_album = prompt.run_prompt(config, Mock(), mock_album, new_album)

        assert add_album.title == new_album.title

    def test_abort_changes(self, mock_album, tmp_config):
        """If selected, abort the changes to the old album."""
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        with patch("builtins.input", side_effect="b"):
            add_album = prompt.run_prompt(config, Mock(), mock_album, new_album)

        assert add_album.title != new_album.title

    def test_invalid_input(self, mock_album, tmp_config):
        """Re-ask user input if invalid input given."""
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        with patch("builtins.input", side_effect=["invalid", "a"]):
            add_album = prompt.run_prompt(config, Mock(), mock_album, new_album)

        assert add_album.title == new_album.title

    def test_apply_missing_tracks(self, mock_album, tmp_config):
        """The new album only contains tracks that existed in the old album."""
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        mock_album.tracks.pop(0)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        with patch("builtins.input", side_effect="a"):
            add_album = prompt.run_prompt(config, Mock(), mock_album, new_album)

        assert add_album.title == new_album.title
        assert len(new_album.tracks) == len(mock_album.tracks)


class TestFmtAlbumChanges:
    """Test formatting of album changes.

    Some of these test cases aren't specifically testing what is output, as that
    is more of an implementation detail and harder to test than it's worth. Rather,
    these test cases are used to help see what is being printed for various scenarios
    (add ``assert 0`` to the end of any test case to see it's output to stdout).
    """

    def test_full_diff_album(self, capsys, mock_album):
        """Print prompt for fully different albums."""
        old_album = mock_album
        new_album = copy.deepcopy(mock_album)
        old_album.tracks[0].title = "really really long old title"
        new_album.title = "new title"
        new_album.artist = "new artist"
        new_album.year = "1999"

        for track in new_album.tracks:
            track.title = "new title"

        assert old_album is not new_album

        print(prompt._fmt_album_changes(old_album, new_album))  # noqa: WPS421

    def test_unmatched_tracks(self, capsys, mock_album):
        """Print prompt for albums with non-matching tracks."""
        old_album = mock_album
        new_album = copy.deepcopy(mock_album)

        for track in old_album.tracks:
            track.track_num = random.randint(1, 1000)

        assert old_album is not new_album

        print(prompt._fmt_album_changes(old_album, new_album))  # noqa: WPS421
