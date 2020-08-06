#!/usr/bin/env python3

"""Entry point for the CLI."""

import argparse
import sys
from typing import List

import pkg_resources


def _parse_args(args: List[str] = None) -> argparse.Namespace:
    """Parses the commandline arguments.

    Args:
        args: Arguments to parse.

    Returns:
        Parsed arguments
    """
    VERSION = pkg_resources.get_distribution("fili").version

    fili_parser = argparse.ArgumentParser(description="Run fili.")
    fili_parser.add_argument(
        "--version", action="version", version="%(prog)s v{0}".format(VERSION)
    )
    fili_parser.add_argument("command", help="command to run")

    # print help and exit if no arguments given
    if not args:
        fili_parser.print_help(sys.stderr)
        sys.exit(1)

    return fili_parser.parse_args(args)


def main():
    """Runs the CLI."""
    _parse_args(sys.argv[1:])


if __name__ == "__main__":
    main()
