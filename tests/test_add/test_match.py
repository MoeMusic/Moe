"""Tests the logic regarding matching albums and tracks against each other."""

from unittest.mock import patch

from moe.plugins.add import match


class TestGetMatchingTracks:
    """Test ``get_track_matches()``."""

    def test_full_match(self, mock_album):
        """All tracks have matches."""
        album_a = mock_album
        album_b = album_a

        track_matches = match.get_matching_tracks(album_a, album_b)

        for track_match in track_matches:
            assert None not in track_match

        for a_track in album_a.tracks:
            assert any(a_track == track_match[0] for track_match in track_matches)
        for b_track in album_b.tracks:
            assert any(b_track == track_match[1] for track_match in track_matches)

        assert len(track_matches) == len(album_a.tracks)

    def test_low_threshold(self, mock_album):
        """A threshold above 1 should never return a match.

        Any non-matched tracks should be paired with ``None``.
        """
        album_a = mock_album
        album_b = album_a

        track_matches = match.get_matching_tracks(album_a, album_b, match_threshold=1.1)

        for track_match in track_matches:
            assert None in track_match

        for track in album_a.tracks:
            assert (track, None) in track_matches
            assert (None, track) in track_matches

        assert len(track_matches) == len(album_a.tracks) + len(album_b.tracks)

    def test_high_threshold(self, mock_track_factory):
        """A zero threshold should always return a match."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        assert track1.track_num != track2.track_num

        track_matches = match.get_matching_tracks(
            track1.album_obj, track2.album_obj, match_threshold=0
        )

        for track_match in track_matches:
            assert None not in track_match

        assert len(track_matches) == 1

    def test_a_longer_than_b(self, mock_album_factory, mock_track):
        """Any unmatched tracks should be paired with ``None``."""
        album_a = mock_album_factory()
        album_b = mock_album_factory()
        mock_track.album_obj = album_a

        track_matches = match.get_matching_tracks(album_a, album_b)

        assert (mock_track, None) in track_matches

    def test_b_longer_than_a(self, mock_album_factory, mock_track):
        """Any unmatched tracks should be paired with ``None``."""
        album_a = mock_album_factory()
        album_b = mock_album_factory()
        mock_track.album_obj = album_b

        track_matches = match.get_matching_tracks(album_a, album_b)

        assert (None, mock_track) in track_matches

    def test_multiple_same_match(self, mock_track_factory):
        """Any track should not have more than one match."""
        track1 = mock_track_factory(year=2000, track_num=1)
        track2 = mock_track_factory(track_num=2)
        track1.album_obj = track2.album_obj

        track3 = mock_track_factory(track_num=3)
        track4 = mock_track_factory(track_num=4)
        track3.album_obj = track4.album_obj

        track3.title = "not a match"
        assert track2.title != track3.title
        assert track2.title == track1.title
        assert track2.title == track4.title

        def mock_get_value(track_a, track_b):
            if track_a.title == track_b.title:
                return 1
            return 0

        with patch("moe.plugins.add.match.get_match_value", wraps=mock_get_value):
            track_matches = match.get_matching_tracks(
                track1.album_obj, track3.album_obj
            )

        album1_tracks = [track_match[0] for track_match in track_matches]
        assert album1_tracks.count(track1) == 1
        assert album1_tracks.count(track2) == 1

        album2_tracks = [track_match[1] for track_match in track_matches]
        assert album2_tracks.count(track3) == 1
        assert album2_tracks.count(track4) == 1


class TestGetMatchValue:
    """Test ``get_match_value()``."""

    def test_same_track_num(self, mock_track_factory):
        """Tracks with the same track number should be a perfect match."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        track1.track_num = track2.track_num

        assert match.get_match_value(track1, track2) == 1

    def test_diff_track_num(self, mock_track_factory):
        """Tracks with a different track number should not be match."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        assert track1.track_num != track2.track_num

        assert match.get_match_value(track1, track2) == 0

    def test_diff_disc(self, mock_track_factory):
        """Tracks with the same track number on different discs should not match."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        track1.track_num = track2.track_num
        track2.disc = 2
        assert track1.track_num == track2.track_num
        assert track1.disc != track2.disc

        assert match.get_match_value(track1, track2) == 0
