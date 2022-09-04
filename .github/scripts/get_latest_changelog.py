#!/usr/bin/env python3

"""Outputs the changelog for the latest version."""

import argparse
import pathlib
import re


def main() -> None:
    """Runs the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("version")

    args = parser.parse_args()
    version = args.version

    changelog_path = pathlib.Path("CHANGELOG.rst")

    changes = ""
    correct_version = False
    with changelog_path.open("r") as f:
        for line in f:
            if re.match(rf"{version}", line) or re.match(r"=", line):
                correct_version = True
                continue
            elif re.match(r"v\d+\.\d+\.\d+", line):
                # encountered next version
                break

            if correct_version:
                changes += line

    print(changes.strip())


if __name__ == "__main__":
    main()
