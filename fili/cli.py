#!/usr/bin/env python3

"""Entry point for the CLI."""

import argparse
import sys

import pkg_resources


def main():
    """Run the cli."""
    VERSION = pkg_resources.get_distribution("fili").version

    fili_parser = argparse.ArgumentParser(description="Run fili.")
    fili_parser.add_argument(
        "--version", action="version", version="%(prog)s v{0}".format(VERSION)
    )
    fili_parser.add_argument("command", help="command to run")

    # print help and exit if no arguments given
    if len(sys.argv) == 1:
        fili_parser.print_help(sys.stderr)
        sys.exit(1)

    fili_parser.parse_args()


if __name__ == "__main__":
    main()
