"""Tests the import core plugin."""

import itertools
from unittest.mock import patch

import moe
from moe import config, moe_import
from moe.config import ExtraPlugin
from moe.library import Album
from moe.moe_import import CandidateAlbum
from tests.conftest import album_factory, extra_factory, track_factory


class ImportPlugin:
    """Test plugin that implements the import hookspecs."""

    @staticmethod
    @moe.hookimpl
    def get_candidates(album: Album):
        """Changes the album title."""
        album.title = "candidate title"

        return [
            CandidateAlbum(album, match_value=1, plugin_source="hook", source_id="1")
        ]

    @staticmethod
    @moe.hookimpl
    def process_candidates(new_album, candidates):
        """Apply the new title onto the old album."""
        new_album.title = candidates[0].album.title


class TestHookSpecs:
    """Test the various plugin hook specifications."""

    def test_get_candidates(self, tmp_config):
        """Plugins can import candidate albums."""
        album = album_factory()
        tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(ImportPlugin, "import_plugin")],
        )

        candidates = config.CONFIG.pm.hook.get_candidates(album=album)
        candidates = list(itertools.chain.from_iterable(candidates))

        assert candidates
        assert candidates[0].album.title == "candidate title"

    def test_process_candidates(self, tmp_config):
        """Plugins can process candidate albums."""
        album = album_factory()
        new_album = album_factory(title="new title")

        tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(ImportPlugin, "import_plugin")],
        )

        config.CONFIG.pm.hook.process_candidates(
            new_album=album,
            candidates=[
                CandidateAlbum(
                    album=new_album, match_value=1, plugin_source="tests", source_id="1"
                )
            ],
        )

        assert album.title == "new title"


class TestPreAdd:
    """Test the `pre_add` hook implementation."""

    def test_pre_add_album(self, tmp_config):
        """Albums are imported in the `pre_add` hook."""
        album = album_factory()
        config = tmp_config("default_plugins = ['add', 'import']")

        with patch(
            "moe.moe_import.import_core.import_album", autospec=True
        ) as mock_import:
            config.pm.hook.pre_add(item=album)

        mock_import.assert_called_once_with(album)

    def test_pre_add_track(self, tmp_config):
        """A track's album is imported in the `pre_add` hook."""
        track = track_factory()
        tmp_config("default_plugins = ['add', 'import']")

        with patch(
            "moe.moe_import.import_core.import_album", autospec=True
        ) as mock_import:
            config.CONFIG.pm.hook.pre_add(item=track)

        mock_import.assert_called_once_with(track.album)

    def test_pre_add_extra(self, tmp_config):
        """Don't try to import an Extra."""
        extra = extra_factory()
        tmp_config("default_plugins = ['add', 'import']")

        with patch(
            "moe.moe_import.import_core.import_album", autospec=True
        ) as mock_import:
            config.CONFIG.pm.hook.pre_add(item=extra)

        mock_import.assert_not_called()


class TestImportAlbum:
    """Test ``import_album``."""

    def test_hooks(self, tmp_config):
        """Importing consists of calling get and process candidates hooks."""
        album = album_factory()
        tmp_config(
            "default_plugins = ['import']",
            extra_plugins=[ExtraPlugin(ImportPlugin, "import_plugin")],
        )

        moe_import.import_album(album)

        assert album.title == "candidate title"


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_registration_as_import(self, tmp_config):
        """Enable the import core plugin if specified in the config."""
        tmp_config(settings='default_plugins = ["import"]')

        assert config.CONFIG.pm.has_plugin("import_core")
