#!/usr/bin/env python3

"""Entry point for the CLI."""

import argparse
import logging
import sys
from typing import List

import pkg_resources

import moe
from moe.core.config import Config
from moe.core.library.session import session_scope

log = logging.getLogger(__name__)


class Hooks:
    """CLI hooks."""

    @staticmethod
    @moe.hookspec
    def addcommand(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
        """Adds a sub-command to moe.

        Args:
            cmd_parsers: contains all the sub-command parsers

        Note:
            The sub-command should be added as an argparse parser to cmd_parsers.

        Example:
            Inside of your hook implementation, write::

                my_parser = cmd_parsers.add_parser('<command_name>', help='')
                my_parser.add_argument('bar', type=int)
                my_parser.set_defaults(func=my_function)

        Note:
            To specify a function to run when your command is passed, you need to
            define the `func` key using `set_defaults` as shown above.
            The function will be called like::

                func(
                    config: moe.Config,  # user config
                    session: sqlalchemy.orm.session.Session,  # database session
                    args: argparse.Namespace,  # parsed commandline arguments
                )
        """


def main():
    """Runs the CLI."""
    config = Config()

    config.pluginmanager.add_hookspecs(Hooks)

    _parse_args(sys.argv[1:], config)


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
    config.pluginmanager.hook.addcommand(cmd_parsers=cmd_parsers)

    parsed_args = moe_parser.parse_args(args)

    # no sub-command given
    if not parsed_args.command:
        moe_parser.print_help(sys.stderr)
        raise SystemExit(1)

    _set_root_log_lvl(parsed_args)

    config.read_config()
    config.init_db()

    # call the sub-command's handler within a single session
    with session_scope() as session:
        parsed_args.func(config=config, session=session, args=parsed_args)


def _create_arg_parser() -> argparse.ArgumentParser:
    """Creates the root argument parser."""
    version = pkg_resources.get_distribution("moe").version

    moe_parser = argparse.ArgumentParser(description="Run moe.")
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


if __name__ == "__main__":
    main()
