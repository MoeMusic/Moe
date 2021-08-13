"""Core api for importing albums."""

from typing import List

import pluggy
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.lib_item import LibItem
from moe.core.library.track import Track

__all__: List[str] = []


class Hooks:
    """Import core plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def import_candidates(config: Config, session: Session, album: Album) -> Album:
        """Imports candidate albums from implemented sources based on the given album.

        This hook should be used to import metadata from an external source and return
        a new album with the new metadata. The candidate albums will then be processed
        in the :meth:`process_candidates` hook.

        Note:
            This hook runs within the :meth:`pre_add` hook.

        Args:
            config: Moe config.
            session: Currrent db session.
            album: Album being added to the library.

        Returns:
            A new album with imported metadata.
        """  # noqa: DAR202

    @staticmethod
    @moe.hookspec
    def process_candidates(
        config: Config, session: Session, old_album, candidate_albums
    ):
        """Process the imported candidate albums.

        If you wish to save and apply any candidate album metadata, it should be applied
        onto the original album, ``old_album``.

        Args:
            config: Moe config.
            session: Currrent db session.
            old_album: Album being added to the library.
            candidate_albums: New candidate albums with imported metadata.
        """


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `import` core hookspecs to Moe."""
    from moe.plugins.moe_import.import_core import Hooks  # noqa: WPS433, WPS442

    plugin_manager.add_hookspecs(Hooks)


@moe.hookimpl
def pre_add(config: Config, session: Session, item: LibItem):
    """Fixes album metadata via external sources prior to it being added to the lib."""
    if isinstance(item, Album):
        old_album = item
    elif isinstance(item, (Extra, Track)):
        old_album = item.album_obj

    candidate_albums = config.plugin_manager.hook.import_candidates(
        config=config, session=session, album=old_album
    )
    config.plugin_manager.hook.process_candidates(
        config=config,
        session=session,
        old_album=old_album,
        candidate_albums=candidate_albums,
    )
