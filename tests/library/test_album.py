"""Test an Album object."""


class TestToDict:
    """Test dict representation of an album."""

    def test_single_track(self, mock_track):
        """If only one track, just return the track's dict."""
        assert mock_track._album_obj.to_dict() == mock_track.to_dict()

    def test_second_track_attribute_dne(self, mock_track_factory):
        """If varying existence of fields between tracks, set field to Various.

        For example, if track 1 has a year, but track 2 doesn't. The album should
        display `year: Various`.
        """
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        track1.title = "don't show this"
        track2.title = ""
        track1._album_obj = track2._album_obj

        assert track1._album_obj.to_dict()["title"] == "Various"

    def test_second_track_attribute_different(self, mock_track_factory):
        """If varying field values between tracks, set field to Various."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        track1.title = "don't show this"
        track2.title = "different"
        track1._album_obj = track2._album_obj

        assert track1._album_obj.to_dict()["title"] == "Various"
