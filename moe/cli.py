#!/usr/bin/env python3

"""Entry point for the CLI."""

import argparse
import logging
import sys
from typing import List

import pkg_resources
import pluggy

import moe
from moe.core.config import Config
from moe.core.library.session import session_scope

__all__ = ["Hooks"]

log = logging.getLogger(__name__)


class Hooks:
    """CLI hooks."""

    @staticmethod
    @moe.hookspec
    def add_command(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
        """Add a sub-command to Moe's CLI.

        Args:
            cmd_parsers: Contains all the sub-command parsers.

        Note:
            The sub-command should be added as an argparse parser to cmd_parsers.

        Example:
            Inside your hook implementation::

                my_parser = cmd_parsers.add_parser('<command_name>', help='')
                my_parser.add_argument('bar', type=int)
                my_parser.set_defaults(func=my_function)

        Note:
            To specify a function to run when your command is passed, you need to
            define the ``func`` key using ``set_defaults`` as shown above.
            The function will be called like::

                func(
                    config: moe.Config,  # user config
                    session: sqlalchemy.orm.session.Session,  # database session
                    args: argparse.Namespace,  # parsed commandline arguments
                )
        """

    @staticmethod
    @moe.hookspec
    def post_args(config: Config, session):
        """Process any cleanup tasks after the CLI arguments have been executed.

        Args:
            config: Moe config.
            session: Currrent db session.

        Note:
            A common use-case may be to process any items that are about to be committed
            to the database. ``session.new.union(session.dirty)`` will return a set of
            any changed or new objects (not just LibItems) to be added to the db.

        Important:
            Normal usage of this hook will not involve altering the state/fields of the
            items that are about to be added to the database.
        """


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
    config.init_db()  # noqa: WPS437
    with session_scope() as session:
        parsed_args.func(config, session, args=parsed_args)
        config.plugin_manager.hook.post_args(config=config, session=session)


def _create_arg_parser() -> argparse.ArgumentParser:
    """Creates the root argument parser."""
    version = pkg_resources.get_distribution("mrmoe").version

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


if __name__ == "__main__":
    main()
