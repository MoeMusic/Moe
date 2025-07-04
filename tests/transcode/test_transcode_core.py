"""Tests the transcode_core module."""

from pathlib import Path

import pytest

from moe import config
from moe.move import fmt_item_path
from moe.plugins.transcode import transcode
from tests.conftest import album_factory, track_factory


@pytest.fixture
def _tmp_transcode_config(tmp_config, tmp_path):
    """A temporary config for the transcode plugin."""
    tmp_config(
        settings=f"""
    default_plugins = ['move', 'write']
    enable_plugins = ['transcode']
    library_path = '{tmp_path.resolve()}'
    """
    )


@pytest.mark.usefixtures("_tmp_transcode_config")
@pytest.mark.ffmpeg
class TestTranscodeTrack:
    """Test transcode() when given a track."""

    def test_track_v0(self):
        """We can transcode a track from flac to mp3 v0."""
        track = track_factory(audio_format="flac", exists=True)
        transcoded_track = transcode(track, "mp3 v0")

        assert transcoded_track.audio_format == "mp3"

    def test_track_v2(self):
        """We can transcode a track from flac to mp3 v2."""
        track = track_factory(audio_format="flac", exists=True)
        transcoded_track = transcode(track, "mp3 v2")

        assert transcoded_track.audio_format == "mp3"

    def test_track_320(self):
        """We can transcode a track from flac to mp3 320."""
        track = track_factory(audio_format="flac", exists=True)
        transcoded_track = transcode(track, "mp3 320")

        assert transcoded_track.audio_format == "mp3"

    def test_track_out_path_default(self):
        """The path of the transcoded track is formatted per the config by default."""
        track = track_factory(audio_format="flac", exists=True)
        transcoded_track = transcode(track, "mp3 320")
        transcode_path = config.CONFIG.settings.transcode.transcode_path

        assert transcoded_track.path == fmt_item_path(transcoded_track, transcode_path)

    def test_track_given_out_path(self, tmp_path):
        """Respect the `out_path` argument if given."""
        track = track_factory(audio_format="flac", exists=True)

        out_path = tmp_path / "out.mp3"
        transcoded_track = transcode(track, "mp3 320", out_path)

        assert transcoded_track.path == out_path

    def test_quote_in_title(self):
        """We should handle the case if there's a single quote in the path."""
        track = track_factory(title="Jacob's Song", audio_format="flac", exists=True)

        transcoded_track = transcode(track, "mp3 v0")

        assert transcoded_track.audio_format == "mp3"

    def test_existing_file_dont_overwrite(self, tmp_path):
        """If ``overwrite`` is False and the file exists, raise FileExistsError."""
        existing_mp3 = tmp_path / "exists.mp3"
        existing_mp3.touch()

        track = track_factory(title="Jacob's Song", audio_format="flac", exists=True)

        with pytest.raises(FileExistsError):
            transcode(track, "mp3 v0", out_path=existing_mp3)

    def test_existing_file_overwrite(self, tmp_path):
        """Overwrite existing files if ``overwrite`` is True."""
        existing_mp3 = tmp_path / "exists.mp3"
        existing_mp3.touch()
        track = track_factory(title="Jacob's Song", audio_format="flac", exists=True)

        transcoded_track = transcode(
            track, "mp3 v0", out_path=existing_mp3, overwrite=True
        )

        assert transcoded_track.audio_format == "mp3"


@pytest.mark.usefixtures("_tmp_transcode_config")
@pytest.mark.ffmpeg
class TestTranscodeAlbum:
    """Test transcode() for an album."""

    def test_album(self):
        """We can transcode an album from flac to mp3 v0."""
        album = album_factory(exists=True, audio_format="flac")

        transcoded_album = transcode(album, "mp3 v0")

        for track in transcoded_album.tracks:
            assert track.audio_format == "mp3"

    def test_album_out_path_default(self):
        """The path of the transcoded album is formatted per the config by default."""
        album = album_factory(audio_format="flac", exists=True)
        transcoded_album = transcode(album, "mp3 320")
        transcode_path = config.CONFIG.settings.transcode.transcode_path

        assert transcoded_album.path == fmt_item_path(transcoded_album, transcode_path)

    def test_album_given_out_path(self, tmp_path):
        """Respect the `out_path` argument if given."""
        album = album_factory(audio_format="flac", exists=True)
        out_path = tmp_path / "out_dir"
        transcoded_album = transcode(album, "mp3 320", out_path)

        assert transcoded_album.path == out_path


@pytest.mark.usefixtures("_tmp_transcode_config")
class TestConfigSettings:
    """Test configuration settings."""

    def test_transcode_path(self):
        """The transcode path is the library path / transcode by default."""
        assert (
            Path(config.CONFIG.settings.transcode.transcode_path)
            == Path(config.CONFIG.settings.library_path) / "transcode"
        )
