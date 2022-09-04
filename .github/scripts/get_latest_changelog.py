#!/usr/bin/env python3

"""Outputs the changelog for the latest version."""

import argparse
import pathlib
import re

import pypandoc


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

    print(convert_rst_to_md(changes).strip())


def convert_rst_to_md(text: str) -> str:
    """Converts restructuredText to markdown."""
    return pypandoc.convert_text(
        text, "md", format="rst", extra_args=["--wrap=preserve"]
    )


if __name__ == "__main__":
    main()
