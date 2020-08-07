"""Toy plugin example."""

import moe


@moe.hookimpl
def addcommand(cmd_parsers):
    """Adds a new `hello` command to moe."""
    hello_parser = cmd_parsers.add_parser("hello", help="say hello")
    hello_parser.set_defaults(func=hello)


def hello(args):
    """Say hello."""
    print("Hello!")
