#!/usr/bin/env python3

"""Entry point for the CLI."""

import argparse
import logging
import sys
from dataclasses import dataclass
from typing import Callable, List

import pkg_resources
import pluggy

import moe
from moe.config import Config, MoeSession
from moe.library.album import Album

__all__ = ["PromptChoice", "query_parser"]

log = logging.getLogger("moe.cli")


class Hooks:
    """General CLI hook specifications."""

    @staticmethod
    @moe.hookspec
    def add_command(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
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


@dataclass
class PromptChoice:
    """A single, user-selectable choice for a CLI prompt.

    Attributes:
        title: Title of the prompt choice that is displayed to the user.
        shortcut_key: Single character the user will use to select the choice.

            Important:
                Ensure the key is not currently in use by another PromptChoice.
        func: Function to call upon this prompt choice being selected. The function
            should return the album to be added to the library (or ``None`` if no album
            should be added) and will be supplied the following keyword arguments:

            * ``config``: Moe config.
            * ``old_album``: Old album with no changes applied.
            * ``new_album``: New album consisting of all the new changes.
    """

    func_type = Callable[[Config, Album, Album], None]

    title: str
    shortcut_key: str
    func: func_type


# Argument parser for a query. This should be passed as a parent parser for a command.
query_parser = argparse.ArgumentParser(
    add_help=False, formatter_class=argparse.RawTextHelpFormatter
)
query_parser.add_argument("query", help="query the library for matching tracks")

query_type_group = query_parser.add_mutually_exclusive_group()
query_type_group.add_argument(
    "-a", "--album", action="store_true", help="query for matching albums"
)
query_type_group.add_argument(
    "-e", "--extra", action="store_true", help="query for matching extras"
)


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `CLI` hookspecs to Moe."""
    from moe.cli import Hooks  # noqa: WPS433, WPS442

    plugin_manager.add_hookspecs(Hooks)


def main(args: List[str] = sys.argv[1:], config: Config = None):
    """Runs the CLI."""
    if not config:
        config = Config()
    _parse_args(args, config)


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
        "--version", action="version", version=f"%(prog)s v{version}"  # noqa: WPS323
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


if __name__ == "__main__":
    main()
