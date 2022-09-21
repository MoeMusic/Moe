"""Test the ``moe.util.cli.fmt_changes`` module."""

import datetime

from moe.util.cli import fmt_item_changes
from tests.conftest import album_factory


class TestFmtItemChanges:
    """Test formatting of item changes.

    These test cases aren't specifically testing what is output, as that
    is more of an implementation detail and harder to test than it's worth. Rather,
    these test cases are used to help see what is being printed for various scenarios
    (add ``assert 0`` to the end of any test case to see it's output to stdout).
    """

    def test_full_diff_album(self):
        """Print prompt for fully different albums."""
        old_album = album_factory()
        new_album = album_factory(
            title="new title", artist="new artist", date=datetime.date(1999, 12, 31)
        )
        old_album.tracks[0].title = "really really long old title"

        for track in new_album.tracks:
            track.title = "new title"

        assert old_album is not new_album

        print(fmt_item_changes(old_album, new_album))
