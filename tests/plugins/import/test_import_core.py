"""Tests the import core plugin."""

import copy
from typing import List
from unittest.mock import patch

import moe
from moe.config import Config, ExtraPlugin
from moe.library.album import Album
from moe.plugins import moe_import


class ImportPlugin:
    """Test plugin that implements the import hookspecs."""

    @staticmethod
    @moe.hookimpl
    def import_candidates(config: Config, album: Album) -> Album:
        """Changes the album title."""
        new_album = copy.deepcopy(album)
        new_album.title = "candidate title"

        return new_album

    @staticmethod
    @moe.hookimpl
    def process_candidates(config: Config, old_album: Album, candidates: List[Album]):
        """Apply the new title onto the old album."""
        old_album.title = candidates[0].title


class TestHookSpecs:
    """Test the various plugin hook specifications."""

    def test_import_candidates(self, mock_album, tmp_config):
        """Plugins can import candidate albums."""
        config = tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(ImportPlugin, "import_plugin")],
        )

        candidates = config.plugin_manager.hook.import_candidates(
            config=config, album=mock_album
        )

        assert candidates
        assert candidates[0].title == "candidate title"

    def test_process_candidates(self, mock_album, tmp_config):
        """Plugins can process candidate albums."""
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"

        config = tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(ImportPlugin, "import_plugin")],
        )

        config.plugin_manager.hook.process_candidates(
            config=config, old_album=mock_album, candidates=[new_album]
        )

        assert mock_album.title == "new title"


class TestPreAdd:
    """Test the `pre_add` hook implementation."""

    def test_pre_add_album(self, mock_album, tmp_config):
        """Albums are imported in the `pre_add` hook."""
        config = tmp_config("default_plugins = ['add', 'import']")

        with patch(
            "moe.plugins.moe_import.import_core.import_album", autospec=True
        ) as mock_import:
            config.plugin_manager.hook.pre_add(config=config, item=mock_album)

        mock_import.assert_called_once_with(config, mock_album)

    def test_pre_add_track(self, mock_track, tmp_config):
        """A track's album is imported in the `pre_add` hook."""
        config = tmp_config("default_plugins = ['add', 'import']")

        with patch(
            "moe.plugins.moe_import.import_core.import_album", autospec=True
        ) as mock_import:
            config.plugin_manager.hook.pre_add(config=config, item=mock_track)

        mock_import.assert_called_once_with(config, mock_track.album_obj)

    def test_pre_add_extra(self, mock_extra, tmp_config):
        """An extra's album is imported in the `pre_add` hook."""
        config = tmp_config("default_plugins = ['add', 'import']")

        with patch(
            "moe.plugins.moe_import.import_core.import_album", autospec=True
        ) as mock_import:
            config.plugin_manager.hook.pre_add(config=config, item=mock_extra)

        mock_import.assert_called_once_with(config, mock_extra.album_obj)


class TestImportAlbum:
    """Test ``import_album``."""

    def test_hooks(self, mock_album, tmp_config):
        """Importing consists of calling import and process candidates hooks."""
        config = tmp_config(
            "default_plugins = ['import']",
            extra_plugins=[ExtraPlugin(ImportPlugin, "import_plugin")],
        )

        moe_import.import_album(config, mock_album)

        assert mock_album.title == "candidate title"


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_registration_as_import(self, tmp_config):
        """Enable the import core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["import"]')

        assert config.plugin_manager.has_plugin("import_core")
