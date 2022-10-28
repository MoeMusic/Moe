"""Core api for importing albums."""

import itertools
import logging
import operator
from dataclasses import dataclass, field

import pluggy

import moe
from moe import config
from moe.library import Album, LibItem, MetaAlbum, Track

__all__ = ["CandidateAlbum", "import_album"]

log = logging.getLogger("moe.import")


@dataclass
class CandidateAlbum:
    """A single candidate for the import process.

    Attributes:
        album (Album): The candidate album.
        match_value (float): 0 to 1 scale of how well the candidate album matches with
            the album being imported.
        source_str (str): A string identifying the release and it's source
            e.g. 'Musicbrainz: 1234'. This will be displayed as the last line in the
            candidate prompt.
        sub_header_info (list[str]): List of any additional info to include in the
            candidate sub-header. The following fields are already included:
            ['media', 'country', 'label']
        match_value_pct (str): ``match_value`` as a percentage.
    """

    album: MetaAlbum
    match_value: float
    source_str: str
    sub_header_info: list[str] = field(default_factory=list)

    @property
    def match_value_pct(self) -> str:
        """Formats `match_value` as a percentage."""
        return f"{round(self.match_value * 100, 1)}%"

    def __str__(self):
        """String representation of a CandidateAlbum."""
        return f"[{self.match_value_pct}] {self.album.artist} - {self.album.title}"


class Hooks:
    """Import core plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def get_candidates(album: Album) -> list[CandidateAlbum]:  # type: ignore
        """Return candidate albums from implemented sources based on the given album.

        This hook should be used to import metadata from an external source and return
        any candidate albums to import from. The candidate albums will then be processed
        in the :meth:`process_candidates` hook.

        Note:
            This hook runs within the :meth:`pre_add` hook.

        Args:
            album: Album being added to the library.

        Returns:
            New candidate album.
        """  # noqa: DAR202

    @staticmethod
    @moe.hookspec
    def process_candidates(new_album: Album, candidates: list[CandidateAlbum]):
        """Process the imported candidate albums.

        If you wish to save and apply any candidate album metadata, it should be applied
        onto the original album, ``new_album``.

        Ensure any potential conflicts with existing albums in the database are
        resolved.

        Args:
            new_album: Album being added to the library.
            candidates: New candidate albums with imported metadata sorted by how well
                 they match ``new_album``.
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
    elif isinstance(item, Track):
        album = item.album_obj
    else:
        return

    import_album(album)


def import_album(album: Album):
    """Imports album metadata for an album."""
    log.debug(f"Importing album metadata. [{album=!r}]")

    candidates = config.CONFIG.pm.hook.get_candidates(album=album)
    candidates = list(itertools.chain.from_iterable(candidates))
    candidates.sort(key=operator.attrgetter("match_value"), reverse=True)

    config.CONFIG.pm.hook.process_candidates(
        new_album=album,
        candidates=candidates,
    )

    log.debug(f"Imported album metadata. [{album=!r}]")
