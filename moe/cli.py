#!/usr/bin/env python3

"""Entry point for the CLI."""

import argparse
import logging
import operator
import sys
from dataclasses import dataclass
from typing import Callable, List, Optional, cast

import pkg_resources
import pluggy
import questionary

import moe
from moe.config import Config, MoeSession
from moe.library.album import Album
from moe.library.track import Track
from moe.plugins import add as moe_add

__all__ = ["PromptChoice", "choice_prompt", "fmt_album_changes", "query_parser"]

log = logging.getLogger("moe.cli")


class Hooks:
    """General CLI hook specifications."""

    @staticmethod
    @moe.hookspec
    def add_command(cmd_parsers: argparse._SubParsersAction):
        """Add a sub-command to Moe's CLI.

        Args:
            cmd_parsers: Contains all the sub-command parsers. The new sub-command
                should be added as an argparse parser to `cmd_parsers`.

        Example:
            Inside your hook implementation::

                my_parser = cmd_parsers.add_parser('<command_name>', help='')
                my_parser.add_argument('bar', type=int)
                my_parser.set_defaults(func=my_function)

        Important:
            To specify a function to run when your command is passed, you need to
            define the ``func`` key using ``set_defaults`` as shown above.
            The function will be called like::

                func(
                    config: moe.Config,  # user config
                    args: argparse.Namespace,  # parsed commandline arguments
                )

        Note:
            If your command utilizes a `query`, you can specify ``query_parser`` as
            a parent parser::

                edit_parser = cmd_parsers.add_parser(
                    "list",
                    description="Lists music in the library.",
                    parents=[moe.cli.query_parser],
                )

        See Also:
            `The python documentation for adding sub-parsers.
            <https://docs.python.org/3/library/argparse.html#sub-commands>`_
        """


# Argument parser for a query. This should be passed as a parent parser for a command.
query_parser = argparse.ArgumentParser(
    add_help=False, formatter_class=argparse.RawTextHelpFormatter
)
query_parser.add_argument("query", help="query the library for matching tracks")

query_type_group = query_parser.add_mutually_exclusive_group()
query_type_group.add_argument(
    "-a",
    "--album",
    action="store_const",
    const="album",
    dest="query_type",
    help="query for matching albums",
)
query_type_group.add_argument(
    "-e",
    "--extra",
    action="store_const",
    const="extra",
    dest="query_type",
    help="query for matching extras",
)
query_parser.set_defaults(query_type="track")


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `CLI` hookspecs to Moe."""
    from moe.cli import Hooks

    plugin_manager.add_hookspecs(Hooks)


def main(args: List[str] = sys.argv[1:], config: Optional[Config] = None):
    """Runs the CLI."""
    if not config:
        config = Config()
    _parse_args(args, config)


if __name__ == "__main__":
    main()


def _parse_args(args: List[str], config: Config):
    """Parses the commandline arguments.

    Args:
        args: Arguments to parse. Should not include 'moe'.
        config: User configuration for moe.

    Raises:
        SystemExit: No sub-commands given.
            Does not include root commands such as `--version` or `--help`.
    """
    moe_parser = _create_arg_parser()

    # load all sub-commands
    cmd_parsers = moe_parser.add_subparsers(help="command to run", dest="command")
    config.plugin_manager.hook.add_command(cmd_parsers=cmd_parsers)

    parsed_args = moe_parser.parse_args(args)

    # no sub-command given
    if not parsed_args.command:
        moe_parser.print_help(sys.stderr)
        raise SystemExit(1)

    _set_root_log_lvl(parsed_args)

    # call the sub-command's handler within a single session
    cli_session = MoeSession()
    with cli_session.begin():
        try:
            parsed_args.func(config, args=parsed_args)
        except SystemExit as err:
            cli_session.commit()
            raise err


def _create_arg_parser() -> argparse.ArgumentParser:
    """Creates the root argument parser."""
    version = pkg_resources.get_distribution("moe").version

    moe_parser = argparse.ArgumentParser()
    moe_parser.add_argument(
        "--version", action="version", version=f"%(prog)s v{version}"
    )
    moe_parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        help="increase logging verbosity; use -vv to enable debug logging",
    )
    moe_parser.add_argument(
        "--quiet",
        "-q",
        action="count",
        help="decrease logging verbosity; use -qq to limit logging to critical errors",
    )

    return moe_parser


def _set_root_log_lvl(args):
    """Sets the root logger level based on cli arguments.

    Args:
        args: parsed arguments to process
    """
    if args.verbose == 1:
        logging.basicConfig(level="INFO")
    elif args.verbose == 2:
        logging.basicConfig(level="DEBUG")
    elif args.quiet == 1:
        logging.basicConfig(level="ERROR")
    elif args.quiet == 2:
        logging.basicConfig(level="CRITICAL")
    else:
        logging.basicConfig(level="WARNING")

    # always set external loggers to warning
    for key in logging.Logger.manager.loggerDict:
        if "moe" not in key:
            logging.getLogger(key).setLevel(logging.WARNING)


########################################################################################
# General shared UI functionality
########################################################################################


@dataclass
class PromptChoice:
    """A single, user-selectable choice for a CLI prompt.

    Attributes:
        title: Title of the prompt choice that is displayed to the user.
        shortcut_key: Single character the user will use to select the choice.

            Important:
                Ensure each shortcut key is not in use by another PromptChoice.
        func: The function that should get called if a choice is selected.
            The definition for how to call ``func`` should be specified by the plugin.
    """

    title: str
    shortcut_key: str
    func: Callable


def choice_prompt(
    prompt_choices: List[PromptChoice], question: str = "What do you want to do?"
) -> PromptChoice:
    """Generates a user choice prompt.

    Args:
        prompt_choices: Prompt choices to be used.
        question: Question prompted to the user.

    Returns:
        The chosen prompt choice.

    Raises:
        SystemExit: Invalid user input.
    """
    prompt_choices.sort(key=operator.attrgetter("shortcut_key"))

    questionary_choices: List[questionary.Choice] = []
    for prompt_choice in prompt_choices:
        questionary_choices.append(
            questionary.Choice(
                title=prompt_choice.title,
                shortcut_key=prompt_choice.shortcut_key,
                value=prompt_choice.shortcut_key,
            )
        )

    user_input = questionary.rawselect(question, choices=questionary_choices).ask()

    for prompt_choice in prompt_choices:
        if prompt_choice.shortcut_key == user_input:
            return prompt_choice

    log.error("Invalid option selected.")
    raise SystemExit(1)


def fmt_album_changes(old_album: Album, new_album: Album) -> str:
    """Formats the changes between between two albums."""
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
    """Formats the changes of the tracklists between two albums."""
    tracklist_str = ""

    matches = moe_add.get_matching_tracks(old_album, new_album)
    matches.sort(
        key=lambda match: (
            getattr(match[1], "disc", 0),
            getattr(match[1], "track_num", 0),
        )
    )  # sort by new track's disc then track number
    unmatched_tracks: List[Track] = []
    for old_track, new_track in matches:
        if not new_track:
            unmatched_tracks.append(cast(Track, old_track))
            continue

        tracklist_str += "\n" + _fmt_track_changes(old_track, new_track)

    if unmatched_tracks:
        tracklist_str += "\n\nUnmatched Tracks:\n"
        tracklist_str += "\n".join([str(track) for track in unmatched_tracks])

    return tracklist_str


def _fmt_track_changes(old_track: Optional[Track], new_track: Track) -> str:
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
