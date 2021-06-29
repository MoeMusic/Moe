"""Tests the add plugin interactive prompt."""

import copy
import datetime
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
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        # new albums won't have paths
        new_album.path = None
        for new_track in new_album.tracks:
            new_track.path = None

        with patch("builtins.input", side_effect="a"):
            add_album = prompt.run_prompt(config, MagicMock(), mock_album, new_album)

        assert add_album.title == new_album.title
        assert add_album.path == mock_album.path

        for track in add_album.tracks:
            assert track.path == mock_album.get_track(track.track_num).path

    def test_invalid_input(self, mock_album, tmp_config):
        """Keep asking for user input if invalid."""
        config = tmp_config("default_plugins = ['add']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"

        # new albums won't have paths
        with patch("builtins.input", side_effect=["invalid", "a"]):
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

        add_album.merge(add_album.get_existing(tmp_session))
        tmp_session.merge(add_album)

        album = tmp_session.query(Album).one()
        assert len(album.tracks) == 2

    def test_multi_disc_album(self, mock_album, tmp_config, tmp_session):
        """Prompt supports multi_disc albums."""
        config = tmp_config("default_plugins = ['add']")
        mock_album.disc_total = 2
        mock_album.tracks[1].disc = 2
        mock_album.tracks[1].track_num = 1
        new_album = copy.deepcopy(mock_album)

        with patch("builtins.input", side_effect="a"):
            add_album = prompt.run_prompt(config, MagicMock(), mock_album, new_album)

        add_album.merge(add_album.get_existing(tmp_session))
        tmp_session.merge(add_album)

        album = tmp_session.query(Album).one()
        assert album.disc_total == 2
        assert album.get_track(1, disc=2)


class TestFmtAlbumChanges:
    """Test formatting of album changes.

    Some of these test cases aren't specifically testing what is output, as that
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

        print(prompt._fmt_album_changes(old_album, new_album))  # noqa: WPS421

    def test_unmatched_tracks(self, mock_album):
        """Print prompt for albums with non-matching tracks."""
        old_album = mock_album
        new_album = copy.deepcopy(mock_album)

        for track in old_album.tracks:
            track.track_num = random.randint(1, 1000)

        assert old_album is not new_album

        print(prompt._fmt_album_changes(old_album, new_album))  # noqa: WPS421

    def test_multi_disc_album(self, mock_album):
        """Prompt supports multi_disc albums."""
        mock_album.disc_total = 2
        mock_album.tracks[1].disc = 2
        mock_album.tracks[1].track_num = 1
        new_album = copy.deepcopy(mock_album)

        print(prompt._fmt_album_changes(mock_album, new_album))  # noqa: WPS421
