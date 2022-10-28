"""Tests the logic regarding matching albums and tracks against each other."""

from unittest.mock import patch

from moe.util.core import get_match_value, get_matching_tracks
from tests.conftest import album_factory, track_factory


class TestGetMatchingTracks:
    """Test ``get_track_matches()``."""

    def test_full_match(self):
        """All tracks have matches."""
        album_a = album_factory()
        album_b = album_factory(dup_album=album_a)

        track_matches = get_matching_tracks(album_a, album_b)

        for track_match in track_matches:
            assert None not in track_match

        for a_track in album_a.tracks:
            assert any(a_track == track_match[0] for track_match in track_matches)
        for b_track in album_b.tracks:
            assert any(b_track == track_match[1] for track_match in track_matches)

        assert len(track_matches) == len(album_a.tracks)

    def test_low_threshold(self):
        """A threshold above 1 should never return a match.

        Any non-matched tracks should be paired with ``None``.
        """
        album_a = album_factory()
        album_b = album_factory(dup_album=album_a)

        track_matches = get_matching_tracks(album_a, album_b, match_threshold=1.1)

        for track_match in track_matches:
            assert None in track_match

        for track in album_a.tracks:
            assert (track, None) in track_matches
            assert (None, track) in track_matches

        assert len(track_matches) == len(album_a.tracks) + len(album_b.tracks)

    def test_high_threshold(self):
        """A zero threshold should always return a match."""
        track1 = track_factory(track_num=1)
        track2 = track_factory(track_num=2)
        assert track1.track_num != track2.track_num

        track_matches = get_matching_tracks(
            track1.album_obj, track2.album_obj, match_threshold=0
        )

        for track_match in track_matches:
            assert None not in track_match

        assert len(track_matches) == 1

    def test_a_longer_than_b(self):
        """Any unmatched tracks should be paired with ``None``."""
        album_a = album_factory()
        album_b = album_factory()
        track = track_factory(album=album_a)

        track_matches = get_matching_tracks(album_a, album_b)

        assert (track, None) in track_matches

    def test_b_longer_than_a(self):
        """Any unmatched tracks should be paired with ``None``."""
        album_a = album_factory()
        album_b = album_factory()
        track = track_factory(album=album_b)

        track_matches = get_matching_tracks(album_a, album_b)

        assert (None, track) in track_matches

    def test_multiple_same_match(self):
        """Any track should not have more than one match."""
        track1 = track_factory(track_num=1)
        track2 = track_factory(track_num=2)
        track1.album_obj = track2.album_obj

        track3 = track_factory(track_num=3)
        track4 = track_factory(track_num=4)
        track3.album_obj = track4.album_obj

        track3.title = "not a match"
        assert track2.title != track3.title
        assert track2.title == track1.title
        assert track2.title == track4.title

        def mock_get_value(track_a, track_b):
            if track_a.title == track_b.title:
                return 1
            return 0

        with patch("moe.util.core.match.get_match_value", wraps=mock_get_value):
            track_matches = get_matching_tracks(track1.album_obj, track3.album_obj)

        album1_tracks = [track_match[0] for track_match in track_matches]
        assert album1_tracks.count(track1) == 1
        assert album1_tracks.count(track2) == 1

        album2_tracks = [track_match[1] for track_match in track_matches]
        assert album2_tracks.count(track3) == 1
        assert album2_tracks.count(track4) == 1


class TestMatchValue:
    """Test ``get_match_value()``."""

    def test_same_album(self):
        """Albums with the same values for all used fields should be a perfect match."""
        album1 = album_factory()
        album2 = album_factory(dup_album=album1)

        assert get_match_value(album1, album2) > 0.9

    def test_diff_album(self):
        """Albums with different values for each field should not match."""
        album1 = album_factory()
        album2 = album_factory()
        album1.title = "a"
        album2.title = "b"
        album1.disc_total = 2
        assert album1.title != album2.title
        assert album1.disc_total != album2.disc_total

        assert get_match_value(album1, album2) < 1

    def test_same_track(self):
        """Tracks with the same values for all used fields should be a perfect match."""
        track1 = track_factory()
        track2 = track_factory(dup_track=track1)

        assert get_match_value(track1, track2) > 0.9

    def test_diff_track(self):
        """Tracks with different values for each field should not match."""
        track1 = track_factory()
        track2 = track_factory()
        track1.title = "a"
        track2.title = "b"
        track1.disc = 2
        assert track1.title != track2.title
        assert track1.disc != track2.disc
        assert track1.track_num != track2.track_num

        assert get_match_value(track1, track2) < 1
