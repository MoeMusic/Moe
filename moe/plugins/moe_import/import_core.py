"""Core api for importing albums."""

from typing import List

import pluggy

import moe
from moe.config import Config
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.lib_item import LibItem
from moe.library.track import Track

__all__ = ["import_album"]


class Hooks:
    """Import core plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def import_candidates(config: Config, album: Album) -> Album:  # type: ignore
        """Imports candidate albums from implemented sources based on the given album.

        This hook should be used to import metadata from an external source and return
        a new album with the new metadata. The candidate albums will then be processed
        in the :meth:`process_candidates` hook.

        Note:
            This hook runs within the :meth:`pre_add` hook.

        Args:
            config: Moe config.
            album: Album being added to the library.

        Returns:
            A new album with imported metadata.
        """  # noqa: DAR202

    @staticmethod
    @moe.hookspec
    def process_candidates(config: Config, old_album: Album, candidates: List[Album]):
        """Process the imported candidate albums.

        If you wish to save and apply any candidate album metadata, it should be applied
        onto the original album, ``old_album``.

        Ensure any potential conflicts with existing albums in the database are
        resolved.

        Args:
            config: Moe config.
            old_album: Album being added to the library.
            candidates: New candidate albums with imported metadata.
        """


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `import` core hookspecs to Moe."""
    from moe.plugins.moe_import.import_core import Hooks

    plugin_manager.add_hookspecs(Hooks)


@moe.hookimpl
def pre_add(config: Config, item: LibItem):
    """Fixes album metadata via external sources prior to it being added to the lib."""
    if isinstance(item, Album):
        album = item
    elif isinstance(item, (Extra, Track)):
        album = item.album_obj
    else:
        raise NotImplementedError

    import_album(config, album)


def import_album(config: Config, album: Album):
    """Imports album metadata for an album."""
    candidates = config.plugin_manager.hook.import_candidates(
        config=config, album=album
    )
    config.plugin_manager.hook.process_candidates(
        config=config,
        old_album=album,
        candidates=candidates,
    )
