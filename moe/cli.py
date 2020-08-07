#!/usr/bin/env python3

"""Entry point for the CLI."""

import argparse
import sys
from typing import List

import pkg_resources
import pluggy

from moe.lib import hooks
from moe.plugins import hello

pm = pluggy.PluginManager("moe")
pm.add_hookspecs(hooks)


def _parse_args(args: List[str] = None):
    """Parses the commandline arguments.

    Args:
        args: Arguments to parse.

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


def main():
    """Runs the CLI."""
    _parse_args(sys.argv[1:])


if __name__ == "__main__":
    main()
