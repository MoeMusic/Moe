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
    pm = _get_plugin_manager(config)

    _parse_args(sys.argv[1:], pm, config)


def _get_plugin_manager(config: Config) -> pluggy.PluginManager:
    """Gets the plugin manager.

    This manages and registers all the specified plugins and hooks.

    Args:
        config: User configuration for moe.

    Returns:
        global plugin manager
    """
    pm = pluggy.PluginManager("moe")
    pm.add_hookspecs(Hooks)

    for plugin in config.plugins:
        pm.register(importlib.import_module(f"moe.plugins.{plugin}"))

    return pm


def _parse_args(args: List[str], pm: pluggy.PluginManager, config: Config):
    """Parses the commandline arguments.

    Args:
        args: Arguments to parse. Should not include 'moe'.
        pm: Global plugin manager
        config: User configuration for moe.
    """
    version = pkg_resources.get_distribution("moe").version

    moe_parser = argparse.ArgumentParser(description="Run moe.")
    moe_parser.add_argument(
        "--version", action="version", version=f"%(prog)s v{version}",  # noqa: WPS323
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

    # load all sub-commands
    cmd_parsers = moe_parser.add_subparsers(help="command to run", dest="command")
    pm.hook.addcommand(cmd_parsers=cmd_parsers)

    parsed_args = moe_parser.parse_args(args)

    # no sub-command given
    if not parsed_args.command:
        moe_parser.print_help(sys.stderr)
        sys.exit(1)

    _set_root_log_lvl(parsed_args)

    # call the sub-command's handler within a single session
    with library.session_scope() as session:
        parsed_args.func(config=config, session=session, args=parsed_args)


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
