"""Test the ``moe.util.cli.fmt_changes`` module."""

import datetime
import random

from moe.util.cli import fmt_album_changes


class TestFmtAlbumChanges:
    """Test formatting of album changes.

    These test cases aren't specifically testing what is output, as that
    is more of an implementation detail and harder to test than it's worth. Rather,
    these test cases are used to help see what is being printed for various scenarios
    (add ``assert 0`` to the end of any test case to see it's output to stdout).
    """

    def test_full_diff_album(self, album_factory):
        """Print prompt for fully different albums."""
        old_album = album_factory()
        new_album = album_factory()
        old_album.tracks[0].title = "really really long old title"
        new_album.title = "new title"
        new_album.artist = "new artist"
        new_album.date = datetime.date(1999, 12, 31)

        for track in new_album.tracks:
            track.title = "new title"

        assert old_album is not new_album

        print(fmt_album_changes(old_album, new_album))

    def test_unmatched_tracks(self, album_factory):
        """Print prompt for albums with non-matching tracks."""
        old_album = album_factory()
        new_album = album_factory()

        for track in old_album.tracks:
            track.track_num = random.randint(1, 1000)

        assert old_album is not new_album

        print(fmt_album_changes(old_album, new_album))

    def test_multi_disc_album(self, album_factory, track_factory):
        """Prompt supports multi_disc albums."""
        mock_album = album_factory()
        new_album = album_factory()
        mock_album.disc_total = 2
        mock_album.tracks[1].disc = 2
        mock_album.tracks[1].track_num = 1
        track_factory(track_num=2, album=mock_album)

        print(fmt_album_changes(mock_album, new_album))
