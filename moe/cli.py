#!/usr/bin/env python3

"""Entry point for the CLI.

This module deals with parsing the arguments of ``moe`` and related functionality.
For general shared CLI functionality, see the ``moe.util.cli`` package.
"""

import argparse
import logging
import sys

import pkg_resources
import pluggy
from rich.console import Console

import moe
from moe import config
from moe.config import Config, ConfigValidationError, MoeSession

__all__ = ["console"]

log = logging.getLogger("moe.cli")

console = Console()


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

            Then, you can call ``query.query(args.query, query_type=args.query_type)``
            to get a list of items matching the query from the library.

        See Also:
            * `The python documentation for adding sub-parsers.
              <https://docs.python.org/3/library/argparse.html#sub-commands>`_
            * The :meth:`~moe.query.query` function.
        """


@moe.hookimpl
def add_hooks(pm: pluggy.manager.PluginManager):
    """Registers `CLI` hookspecs to Moe."""
    from moe.cli import Hooks

    pm.add_hookspecs(Hooks)


def main(args: list[str] = sys.argv[1:]):
    """Runs the CLI."""
    log.debug(f"Commandline arguments received. [{args=!r}]")

    if not config.CONFIG:
        try:
            Config()
        except ConfigValidationError as err:
            log.error(err)
            raise SystemExit(1) from err
    _parse_args(args)


if __name__ == "__main__":
    main()


def _parse_args(args: list[str]):
    """Parses the commandline arguments.

    Args:
        args: Arguments to parse. Should not include 'moe'.

    Raises:
        SystemExit: No sub-commands given.
            Does not include root commands such as `--version` or `--help`.
    """
    moe_parser = _create_arg_parser()

    # load all sub-commands
    cmd_parsers = moe_parser.add_subparsers(help="command to run", dest="command")
    config.CONFIG.pm.hook.add_command(cmd_parsers=cmd_parsers)

    parsed_args = moe_parser.parse_args(args)

    # no sub-command given
    if not parsed_args.command:
        moe_parser.print_help(sys.stderr)
        raise SystemExit(1)

    _set_log_lvl(parsed_args)

    # call the sub-command's handler within a single session
    cli_session = MoeSession()
    with cli_session.begin():
        try:
            parsed_args.func(args=parsed_args)
        except SystemExit:
            cli_session.commit()
            raise


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


def _set_log_lvl(args):
    """Sets the root logger level based on cli arguments."""
    moe_log = logging.getLogger("moe")

    if args.verbose == 1:
        moe_log.setLevel(logging.INFO)
    elif args.verbose == 2:
        moe_log.setLevel(logging.DEBUG)
    elif args.quiet == 1:
        moe_log.setLevel(logging.ERROR)
    elif args.quiet == 2:
        moe_log.setLevel(logging.CRITICAL)
