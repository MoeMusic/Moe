"""Import prompt."""

import logging
import operator
from typing import List, Optional, cast

import pluggy
import questionary

import moe.cli
from moe.config import Config
from moe.library.album import Album
from moe.library.track import Track
from moe.plugins import add as moe_add

log = logging.getLogger("moe.add")

__all__ = ["AbortImport", "import_prompt"]


class AbortImport(Exception):
    """Used to abort the import process."""


class Hooks:
    """Import plugin cli hook specifications."""

    @staticmethod
    @moe.hookspec
    def add_import_prompt_choice(prompt_choices: List[moe.cli.PromptChoice]):
        """Add a user input choice to the prompt.

        Args:
            prompt_choices: List of prompt choices. To add a prompt choice, simply
                append it to this list.

        Example:
            Inside your hook implementation::

                prompt_choices.append(
                    PromptChoice(
                        title="Abort", shortcut_key="x", func=_abort_changes
                    )
                )
        """


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `import` cli hookspecs to Moe."""
    from moe.plugins.moe_import.import_cli import Hooks  # noqa: WPS433, WPS442

    plugin_manager.add_hookspecs(Hooks)


@moe.hookimpl
def process_candidates(config: Config, old_album: Album, candidates):
    """Use the import prompt to select and process the imported candidate albums."""
    if candidates:
        import_prompt(config, old_album, candidates[0])


@moe.hookimpl
def add_import_prompt_choice(prompt_choices: List[moe.cli.PromptChoice]):
    """Adds the ``apply`` and ``abort`` prompt choices to the user prompt."""
    prompt_choices.append(
        moe.cli.PromptChoice(
            title="Apply changes", shortcut_key="a", func=_apply_changes
        )
    )
    prompt_choices.append(
        moe.cli.PromptChoice(title="Abort", shortcut_key="x", func=_abort_changes)
    )


def import_prompt(
    config: Config,
    old_album: Album,
    new_album: Album,
):
    """Runs the interactive prompt for the given album changes.

    Args:
        config: Moe config.
        old_album: Original album to be added.
        new_album: New album with all metadata changes. Will be compared against
            ``old_album``.

    Returns:
        The album to be added to the library.
    """
    if old_album == new_album:
        return old_album

    existing_album = new_album.get_existing()
    old_album.merge(existing_album, overwrite_album_info=False)

    print(_fmt_album_changes(old_album, new_album))  # noqa: WPS421

    prompt_choices: List[moe.cli.PromptChoice] = []
    config.plugin_manager.hook.add_import_prompt_choice(prompt_choices=prompt_choices)
    prompt_choices.sort(key=operator.attrgetter("shortcut_key"))

    user_input = _get_input(prompt_choices)

    for prompt_choice in prompt_choices:
        if prompt_choice.shortcut_key == user_input:
            prompt_choice.func(  # type: ignore
                config=config,
                old_album=old_album,
                new_album=new_album,
            )


def _get_input(
    prompt_choices: List[moe.cli.PromptChoice],
) -> moe.cli.PromptChoice.func_type:
    """Prompts the user for input using the given prompt choices."""
    questionary_choices: List[questionary.Choice] = []
    for prompt_choice in prompt_choices:
        questionary_choices.append(
            questionary.Choice(
                title=prompt_choice.title,
                shortcut_key=prompt_choice.shortcut_key,
                value=prompt_choice.shortcut_key,
            )
        )

    return questionary.rawselect(
        "What do you want to do?", choices=questionary_choices
    ).ask()


def _fmt_album_changes(old_album: Album, new_album: Album) -> str:
    """Formats the changes of the album between the old and new album."""
    album_info_str = ""
    album_title = f"Album: {old_album.title}"
    if old_album.title != new_album.title:
        album_title += f" -> {new_album.title}"
    album_info_str += album_title

    album_artist = f"Album Artist: {old_album.artist}"
    if old_album.artist != new_album.artist:
        album_artist = album_artist + f" -> {new_album.artist}"
    album_info_str += "\n" + album_artist

    album_year = f"Year: {old_album.year}"
    if old_album.year != new_album.year:
        album_year = album_year + f" -> {new_album.year}"
    album_info_str += "\n" + album_year
    if new_album.mb_album_id:
        mb_album_id = f"Musicbrainz ID: {new_album.mb_album_id}"
        album_info_str += "\n" + mb_album_id

    tracklist_str = _fmt_tracklist(old_album, new_album)

    extra_str = ""
    extra_str += "\nExtras:\n"
    extra_str += "\n".join([extra.filename for extra in old_album.extras])

    album_str = album_info_str + "\n" + tracklist_str
    if old_album.extras:
        album_str += "\n" + extra_str

    return album_str


def _fmt_tracklist(old_album: Album, new_album: Album) -> str:
    """Formats the changes of the tracklist between two albums."""
    tracklist_str = ""

    matches = moe_add.get_matching_tracks(old_album, new_album)
    matches.sort(
        key=lambda match: match[1].track_num + match[1].disc * len(matches)
        if match[1] is not None
        else 0
    )  # sort by new track's track number and disc
    unmatched_tracks: List[Track] = []
    for old_track, new_track in matches:
        if not new_track:
            unmatched_tracks.append(cast(Track, old_track))
            continue

        tracklist_str += "\n" + _fmt_track_change(old_track, new_track)

    if unmatched_tracks:
        tracklist_str += "\n\nUnmatched Tracks:\n"
        tracklist_str += "\n".join([str(track) for track in unmatched_tracks])

    return tracklist_str


def _fmt_track_change(old_track: Optional[Track], new_track: Track) -> str:
    """Formats the changes between two tracks."""
    track_change = ""
    new_disc = ""
    old_disc = ""
    if new_track.disc_total > 1:
        new_disc = f"{new_track.disc}."
        if old_track:
            old_disc = f"{old_track.disc}."
    if old_track:
        old_track_title = f"{old_disc}{old_track.track_num}: {old_track.title}"
    else:
        old_track_title = "(missing)"
    track_change += old_track_title

    new_track_title = f"{new_disc}{new_track.track_num}: {new_track.title}"

    if old_track_title != new_track_title:
        track_change += f" -> {new_track_title}"

    return track_change


def _apply_changes(
    config: Config,
    old_album: Album,
    new_album: Album,
):
    """Applies the album changes."""
    new_album.path = old_album.path
    for old_track, new_track in moe_add.get_matching_tracks(old_album, new_album):
        if not old_track:
            new_track.album_obj = None  # type: ignore # (causes mypy error)
        elif new_track:
            new_track.path = old_track.path

    for extra in old_album.extras:
        extra.album_obj = new_album

    new_album.merge(old_album)


def _abort_changes(
    config: Config,
    old_album: Album,
    new_album: Album,
):
    """Aborts the album changes."""
    raise AbortImport()
