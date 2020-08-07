#!/usr/bin/env python3

"""Entry point for the CLI."""

import argparse
import sys
from typing import List

import pkg_resources
import pluggy

import moe
from moe.plugins import hello


def main():
    """Runs the CLI."""
    pm = pluggy.PluginManager("moe")
    pm.add_hookspecs(Hooks)

    _parse_args(sys.argv[1:], pm)


class Hooks:
    """CLI hooks."""

    @staticmethod
    @moe.hookspec
    def addcommand(cmd_parsers: argparse.ArgumentParser):
        """Add a sub-command to moe.

        Args:
            cmd_parsers: parent parser for the sub-commands

        Note:
            The sub-command should be added as an argparse parser to cmd_parsers.

        Example:
            >>> my_parser = cmd_parsers.add_parser('<command_name>', help='')
            >>> my_parser.add_argument('bar', type=int)
            >>> my_parser.set_defaults(func=my_function)

        Note:
            To specify a function to run when your command is passed, you need to define
            the `func` key using `set_defaults` as shown above. This function will be
            passed all of the parsed commandline arguments with the `args` key.

        Example:
            >>> my_function(args):
            ...    print("Welcome to my plugin!")
        """
        pass


def _parse_args(args: List[str], pm: pluggy.PluginManager):
    """Parses the commandline arguments.

    Args:
        args: Arguments to parse.
        pm: Global PluginManager

    Returns:
        Parsed arguments
    """
    VERSION = pkg_resources.get_distribution("moe").version

    moe_parser = argparse.ArgumentParser(description="Run moe.")
    moe_parser.add_argument(
        "--version", action="version", version="%(prog)s v{0}".format(VERSION)
    )

    # load all sub-commands
    pm.register(hello)
    cmd_parsers = moe_parser.add_subparsers(help="command to run")
    pm.hook.addcommand(cmd_parsers=cmd_parsers)

    # print help and exit if no arguments given
    if not args:
        moe_parser.print_help(sys.stderr)
        sys.exit(1)

    parsed_args = moe_parser.parse_args(args)
    parsed_args.func(args=args)


if __name__ == "__main__":
    main()
