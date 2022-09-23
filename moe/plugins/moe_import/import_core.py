"""Core api for importing albums."""

import logging

import pluggy

import moe
from moe import config
from moe.library import Album, Extra, LibItem, Track

__all__ = ["import_album"]

log = logging.getLogger("moe.import")


class Hooks:
    """Import core plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def import_candidates(album: Album) -> Album:  # type: ignore
        """Imports candidate albums from implemented sources based on the given album.

        This hook should be used to import metadata from an external source and return
        a new album with the new metadata. The candidate albums will then be processed
        in the :meth:`process_candidates` hook.

        Note:
            This hook runs within the :meth:`pre_add` hook.

        Args:
            album: Album being added to the library.

        Returns:
            A new album with imported metadata.
        """  # noqa: DAR202

    @staticmethod
    @moe.hookspec
    def process_candidates(old_album: Album, candidates: list[Album]):
        """Process the imported candidate albums.

        If you wish to save and apply any candidate album metadata, it should be applied
        onto the original album, ``old_album``.

        Ensure any potential conflicts with existing albums in the database are
        resolved.

        Args:
            old_album: Album being added to the library.
            candidates: New candidate albums with imported metadata.
        """


@moe.hookimpl
def add_hooks(pm: pluggy.manager.PluginManager):
    """Registers `import` core hookspecs to Moe."""
    from moe.plugins.moe_import.import_core import Hooks

    pm.add_hookspecs(Hooks)


@moe.hookimpl
def pre_add(item: LibItem):
    """Fixes album metadata via external sources prior to it being added to the lib."""
    if isinstance(item, Album):
        album = item
    elif isinstance(item, (Extra, Track)):
        album = item.album_obj
    else:
        raise NotImplementedError

    import_album(album)


def import_album(album: Album):
    """Imports album metadata for an album."""
    log.debug(f"Importing album metadata. [{album=!r}]")

    candidates = config.CONFIG.pm.hook.import_candidates(album=album)
    config.CONFIG.pm.hook.process_candidates(
        old_album=album,
        candidates=candidates,
    )

    log.debug(f"Imported album metadata. [{album=!r}]")
