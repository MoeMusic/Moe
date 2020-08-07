"""Core hook specifications.

Any plugin-defined hooks should be in the plugin's module.
"""

import argparse

import moe


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
