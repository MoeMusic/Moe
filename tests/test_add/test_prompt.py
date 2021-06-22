"""Tests the add plugin interactive prompt."""

import copy
import random
from unittest.mock import MagicMock, Mock, patch

from moe.core.library.album import Album
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
        mock_session = MagicMock()
        mock_session.get.return_value = None
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        with patch("builtins.input", side_effect="a"):
            add_album = prompt.run_prompt(config, MagicMock(), mock_album, new_album)

        assert add_album.title == new_album.title

    def test_default_whitespace(self, mock_album, tmp_config):
        """If whitespace input, apply the changes to the old album."""
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        with patch("builtins.input", side_effect=" "):
            add_album = prompt.run_prompt(config, MagicMock(), mock_album, new_album)

        assert add_album.title == new_album.title

    def test_default_empty(self, mock_album, tmp_config):
        """If no input, apply the changes to the old album."""
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        with patch("builtins.input", lambda _: ""):
            add_album = prompt.run_prompt(config, MagicMock(), mock_album, new_album)

        assert add_album.title == new_album.title

    def test_abort_changes(self, mock_album, tmp_config):
        """If selected, abort the changes to the old album."""
        mock_session = MagicMock()
        mock_session.get.return_value = None
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        with patch("builtins.input", side_effect="b"):
            add_album = prompt.run_prompt(config, MagicMock(), mock_album, new_album)

        assert not add_album

    def test_partial_album_exists_merge(
        self, mock_album, mock_track_factory, tmp_config, tmp_session
    ):
        """Merge existing tracks with those being added."""
        config = tmp_config("default_plugins = ['add']")
        existing_album = copy.deepcopy(mock_album)
        new_album = copy.deepcopy(mock_album)
        existing_album.tracks.pop(0)
        mock_album.tracks.pop(1)
        tmp_session.add(existing_album)
        tmp_session.commit()

        with patch("builtins.input", side_effect="a"):
            add_album = prompt.run_prompt(config, tmp_session, mock_album, new_album)

        add_album.merge_existing(tmp_session)

        album = tmp_session.query(Album).one()
        assert len(album.tracks) == 2


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
