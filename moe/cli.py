#!/usr/bin/env python3

"""Entry point for the CLI."""

import argparse
import importlib
import logging
import sys
from typing import List

import pkg_resources
import pluggy

import moe
from moe.core import library
from moe.core.config import Config

log = logging.getLogger(__name__)


class Hooks:
    """CLI hooks."""

    @staticmethod
    @moe.hookspec
    def addcommand(cmd_parsers: argparse._SubParsersAction):
        """Adds a sub-command to moe.

        Args:
            cmd_parsers: contains all the sub-command parsers

        Note:
            The sub-command should be added as an argparse parser to cmd_parsers.

        Example:
            >>> my_parser = cmd_parsers.add_parser('<command_name>', help='')
            >>> my_parser.add_argument('bar', type=int)
            >>> my_parser.set_defaults(func=my_function)

        Note:
            To specify a function to run when your command is passed, you need to
            define the `func` key using `set_defaults` as shown above.
            The function call will be called like
            ```
            func(
                config: moe.Config,  # user config
                session: sqlalchemy.orm.session.Session,  # database session
                args: argparse.Namespace,  # parsed commandline arguments
            )
            ```

        Example:
            >>> my_function(config, session, args):
            ...    print("Welcome to my plugin!")
        """
        pass


def main():
    """Runs the CLI."""
    config = Config()
    pm = _get_plugin_manager(config)

    _parse_args(sys.argv[1:], pm, config)


def _get_plugin_manager(config: Config) -> pluggy.PluginManager:
    """Gets the plugin manager.

    This manages and registers all the specified plugins and hooks.

    Args:
        config: User configuration for moe.
    """
    pm = pluggy.PluginManager("moe")
    pm.add_hookspecs(Hooks)

    for plugin in config.plugins:
        pm.register(importlib.import_module("moe.plugins." + plugin))

    return pm


def _parse_args(args: List[str], pm: pluggy.PluginManager, config: Config):
    """Parses the commandline arguments.

    Args:
        args: Arguments to parse.
        pm: Global plugin manager
        config: User configuration for moe.

    Returns:
        Parsed arguments
    """
    VERSION = pkg_resources.get_distribution("moe").version

    moe_parser = argparse.ArgumentParser(description="Run moe.")
    moe_parser.add_argument(
        "--version", action="version", version="%(prog)s v{0}".format(VERSION)
    )
    moe_parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        help="Increase logging verbosity. Use -vv to enable debug logging.",
    )
    moe_parser.add_argument(
        "--quiet",
        "-q",
        action="count",
        help="Decrease logging verbosity."
        " Use -qq to limit logging to critical errors.",
    )

    # load all sub-commands
    cmd_parsers = moe_parser.add_subparsers(help="command to run")
    pm.hook.addcommand(cmd_parsers=cmd_parsers)

    if not args:
        moe_parser.print_help(sys.stderr)
        sys.exit(1)

    parsed_args = moe_parser.parse_args(args)

    if parsed_args.verbose == 1:
        logging.basicConfig(level="INFO")
    elif parsed_args.verbose == 2:
        logging.basicConfig(level="DEBUG")
    elif parsed_args.quiet == 1:
        logging.basicConfig(level="ERROR")
    elif parsed_args.quiet == 2:
        logging.basicConfig(level="CRITICAL")
    else:
        logging.basicConfig(level="WARNING")

    # call the sub-command's handler within a single session
    with library.session_scope() as session:
        try:
            parsed_args.func(config=config, session=session, args=parsed_args)
        except AttributeError:
            moe_parser.print_help(sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
