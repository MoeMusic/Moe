"""Writes tags to track files."""

import logging

import mediafile
import pluggy

import moe
from moe import config
from moe.library import LibItem, Track

__all__ = ["write_tags"]

log = logging.getLogger("moe.write")


class Hooks:
    """Write plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def write_custom_tags(track: Track):
        """Allow plugins to write tags to a Track.

        How you write tags to the track is up to each individual plugin. Internally,
        Moe uses the `mediafile <https://github.com/beetbox/mediafile>`_ library to
        write tags.

        Args:
            track: Track to write tags to.

        Example:
            .. code:: python

                audio_file = mediafile.MediaFile(track.path)
                audio_file.album = track.album
                audio_file.save()

        See Also:
            * :ref:`Album and track fields <fields:Fields>`
            * `Mediafile docs <https://mediafile.readthedocs.io/en/latest/>`_
            * The :meth:`~moe.library.track.Hooks.read_custom_tags` hook for reading
              tags.
        """


@moe.hookimpl
def add_hooks(pm: pluggy.manager.PluginManager):
    """Registers `write` hookspecs to Moe."""
    from moe.plugins.write import Hooks

    pm.add_hookspecs(Hooks)


@moe.hookimpl
def process_new_items(items: list[LibItem]):
    """Writes tags to any new tracks in the library."""
    for item in items:
        if isinstance(item, Track):
            write_tags(item)


@moe.hookimpl
def process_changed_items(items: list[LibItem]):
    """Writes tags to any altered tracks in the library."""
    for item in items:
        if isinstance(item, Track):
            write_tags(item)


@moe.hookimpl(tryfirst=True)
def write_custom_tags(track: Track):
    """Writes all internally tracked tags to the track."""
    audio_file = mediafile.MediaFile(track.path)

    audio_file.album = track.album
    audio_file.albumartist = track.albumartist
    audio_file.artist = track.artist
    audio_file.artists = track.artists
    audio_file.country = track.album_obj.country
    audio_file.date = track.album_obj.date
    audio_file.disc = track.disc
    audio_file.disctotal = track.album_obj.disc_total
    audio_file.genres = track.genres
    audio_file.label = track.album_obj.label
    audio_file.media = track.album_obj.media
    audio_file.original_date = track.album_obj.original_date
    audio_file.title = track.title
    audio_file.track = track.track_num

    audio_file.save()


def write_tags(track: Track):
    """Write tags to a track's file."""
    log.debug(f"Writing tags to track. [{track=!r}]")

    config.CONFIG.pm.hook.write_custom_tags(track=track)

    log.info(f"Wrote tags to track. [{track=!r}]")
