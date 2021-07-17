#!/usr/bin/env python3

"""Entry point for the CLI."""

import argparse
import functools
import logging
import sys
from typing import Any, List, Optional

import pkg_resources
import pluggy
import sqlalchemy
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.lib_item import LibItem
from moe.core.library.session import session_scope

__all__ = ["Hooks"]

log = logging.getLogger("moe.cli")


class Hooks:
    """CLI hooks specifications."""

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
                    session: sqlalchemy.orm.session.Session,  # database session
                    args: argparse.Namespace,  # parsed commandline arguments
                )

        Note:
            If your command utilizes a `query`, you can specify ``query_parser`` as
            a parent parser::

                edit_parser = cmd_parsers.add_parser(
                    "list",
                    description="Lists music in the library.",
                    parents=[query.query_parser],
                )

        See Also:
            `The python documentation for adding sub-parsers.
            <https://docs.python.org/3/library/argparse.html#sub-commands>`_
        """

    @staticmethod
    @moe.hookspec
    def edit_new_items(config: Config, session: Session, items: List[LibItem]):
        """Edit any new or changed items prior to them being added to the library.

        Args:
            config: Moe config.
            session: Currrent db session.
            items: Any new or changed items in the current session. The items and
                their changes have not yet been committed to the library.

        See Also:
            The :meth:`process_new_items` hook if you wish to process any items after
            any final edits have been made and they have been successfully added to
            the library.
        """

    @staticmethod
    @moe.hookspec
    def process_new_items(config: Config, session: Session, items: List[LibItem]):
        """Process any new or changed items after they have been added to the library.

        Args:
            config: Moe config.
            session: Currrent db session.
            items: Any new or changed items that have been successfully added to the
                library during the current session.

        See Also:
            The :meth:`edit_new_items` hook if you wish to edit the items.
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
    config.init_db()
    with session_scope() as session:
        sqlalchemy.event.listen(
            session, "before_flush", functools.partial(_edit_new_items, config=config)
        )
        sqlalchemy.event.listen(
            session, "after_flush", functools.partial(_process_new_items, config=config)
        )

        parsed_args.func(config, session, args=parsed_args)


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


def _edit_new_items(
    session: Session,
    flush_context: sqlalchemy.orm.UOWTransaction,
    instances: Optional[Any],
    config: Config,
):
    """Runs the ``edit_new_items`` hook specification.

    This uses the sqlalchemy ORM event ``before_flush`` in the background to determine
    the time of execution and to provide any new or changed items to the hook
    implementations.

    Args:
        session: Current db session.
        flush_context: sqlalchemy obj which handles the details of the flush.
        instances: List of objects passed to the ``flush()`` method.
        config: Moe config.
    """
    config.plugin_manager.hook.edit_new_items(
        config=config, session=session, items=session.new.union(session.dirty)
    )


def _process_new_items(
    session: Session,
    flush_context: sqlalchemy.orm.UOWTransaction,
    config: Config,
):
    """Runs the ``process_new_items`` hook specification.

    This uses the sqlalchemy ORM event ``after_flush`` in the background to determine
    the time of execution and to provide any new or changed items to the hook
    implementations.

    Args:
        session: Current db session.
        flush_context: sqlalchemy obj which handles the details of the flush.
        config: Moe config.
    """
    config.plugin_manager.hook.process_new_items(
        config=config, session=session, items=session.new.union(session.dirty)
    )


if __name__ == "__main__":
    main()
