#!/usr/bin/env python3

"""Creates a release pull request.

Also generates the changelog for the new release.

See Also:
    https://github.com/pytest-dev/pytest/blob/main/scripts/prepare-release-pr.py
    (pytest's script I stole a lot from)
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import shutil
import subprocess
from textwrap import indent
from typing import TYPE_CHECKING

import github3

if TYPE_CHECKING:
    from github3.repos import Repository

SLUG = "MoeMusic/Moe"
PR_BODY = """
This pull request was created automatically by a manual trigger.

Once this pull request is merged into main, it will be released on github and PyPI.
"""

# Ordered in order to display
COMMIT_TYPE_TO_HEADER = {
    "breaking": "Breaking Changes",
    "feat": "New Features",
    "fix": "Bug Fixes",
    "perf": "Performance Enhancements",
    "build": "Build Changes",
    "deprecate": "Deprecations",
    "ci": None,
    "docs": None,
    "refactor": None,
    "style": None,
    "test": None,
}


class Commit:
    """Represents a single commit."""

    commit_hash: str
    commit_type: str
    scope: str
    breaking: bool
    summary: str
    body: str

    COMMIT_TITLE_RE = re.compile(
        r"""
        (?P<type>\w+)
        \(?(?P<scope>\w+)?\)?
        (?P<break>!?)
        :\s?(?P<summary>.+)
        """,
        re.VERBOSE,
    )
    COMMIT_RE = re.compile(
        r"""
        hash=(?P<hash>\w{40});\s
        title=(?P<title>.+);\s
        body=(?P<body>.*);
        """,
        re.VERBOSE | re.DOTALL,
    )  # based on "git_log_format defined below"

    def __init__(self, commit_log: str) -> None:
        """Parse a `git log` ouput for a single commit."""
        # default values
        self.scope = ""
        self.breaking = False

        match = re.match(self.COMMIT_RE, commit_log)
        if not match:
            err_msg = f"Could not parse commit log: '{commit_log}'"
            raise ValueError(err_msg)

        self.commit_hash = match["hash"]
        title = match["title"]
        self.body = match["body"].strip()

        match = re.match(self.COMMIT_TITLE_RE, title)
        if match:
            self.commit_type = match.group("type")
            self.scope = match.group("scope")
            self.summary = match.group("summary")
            if match.group("break"):
                self.breaking = True
                self.commit_type = "breaking"

    def __str__(self) -> str:
        """Formats the commit for a changelog."""
        changelog_entry = "* "

        if self.scope:
            changelog_entry += self.scope.capitalize() + ": "

        changelog_entry += self.summary.capitalize()
        commit_github_url = f"https://github.com/{SLUG}/commit/{self.commit_hash}"
        changelog_entry += f" (`{self.commit_hash[:7]} <{commit_github_url}>`_)"

        return changelog_entry.strip()


def main() -> None:
    """Runs the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("token")

    git_path = shutil.which("git")
    if not git_path:
        err_msg = "Could not find 'git' executable in PATH."
        raise RuntimeError(err_msg)

    args = parser.parse_args()
    prepare_release_pr(args.token, git_path)


def prepare_release_pr(token: str, git_path: str) -> None:
    """Prepares the release pull request."""
    subprocess.run([git_path, "config", "user.name", "Moe bot"], check=True)  # noqa: S603 git is a trusted executable
    subprocess.run([git_path, "config", "user.email", "<>"], check=True)  # noqa: S603 git is a trusted executable

    cz_path = shutil.which("cz")
    if not cz_path:
        err_msg = "Could not find 'cz' executable in PATH."
        raise RuntimeError(err_msg)

    old_version = subprocess.run(  # noqa: S603 trusted inputs
        [cz_path, "version", "--project"], text=True, capture_output=True, check=True
    ).stdout
    old_version = f"v{old_version.strip()}"
    subprocess.run([cz_path, "bump", "--files-only"], check=True)  # noqa: S603 trusted inputs
    new_version = subprocess.run(  # noqa: S603 trusted inputs
        [cz_path, "version", "--project"], text=True, capture_output=True, check=True
    ).stdout
    new_version = f"v{new_version.strip()}"

    generate_changelog(old_version, new_version, git_path)
    release_branch = f"release_{new_version}"
    subprocess.run([git_path, "checkout", "-b", f"{release_branch}"], check=True)  # noqa: S603 git is a trusted executable

    subprocess.run(  # noqa: S603 git is a trusted executable
        [git_path, "commit", "-a", "-m", f"release: {new_version}"], check=True
    )
    oauth_url = f"https://{token}:x-oauth-basic@github.com/{SLUG}.git"
    subprocess.run(  # noqa: S603 git is a trusted executable
        [git_path, "push", oauth_url, f"HEAD:{release_branch}", "--force"], check=True
    )

    repo = login(token)
    if not repo:
        err_msg = f"Failed to get repository '{SLUG}'."
        raise RuntimeError(err_msg)

    repo.create_pull(
        f"Prepare release {new_version}",
        base="main",
        head=f"{release_branch}",
        body=PR_BODY,
    )


def generate_changelog(old_version: str, new_version: str, git_path: str) -> None:
    """Generates a changelog for a new release."""
    changelog_path = pathlib.Path("CHANGELOG.rst")

    release_title = f"{new_version} ({dt.datetime.now(dt.timezone.utc).date()})"
    changelog_title = f"\n{release_title}\n"
    changelog_title += "=" * len(release_title) + "\n"

    field_delim = ";"
    commit_delim = ";|;"
    git_log_format = (
        f"hash=%H{field_delim} title=%s{field_delim} body=%b{field_delim}{commit_delim}"
    )
    git_log = str(
        subprocess.run(  # noqa: S603 git is a trusted executable
            [
                git_path,
                "log",
                f"--pretty=format:{git_log_format}",
                f"{old_version}..HEAD",
            ],
            check=True,
            text=True,
            capture_output=True,
        ).stdout
    )
    commits = [
        Commit(commit_log.strip())
        for commit_log in git_log.split(commit_delim)
        if commit_log
    ]

    changelog_body = ""
    for commit_type, header in COMMIT_TYPE_TO_HEADER.items():
        if not header or not any(
            commit.commit_type == commit_type for commit in commits
        ):
            continue

        changelog_body += header + "\n"
        changelog_body += "-" * len(header) + "\n"

        for commit in commits:
            if commit_type == commit.commit_type:
                changelog_body += str(commit) + "\n"
                if commit.breaking:
                    changelog_body += "\n" + indent(commit.body, "  ") + "\n"

        changelog_body += "\n"

    changelog = changelog_title + "\n" + changelog_body
    changelog += (
        "`Full diff "
        f"<https://github.com/{SLUG}/compare/{old_version}...{new_version}>`__\n"
    )

    # write changelog
    with changelog_path.open("r+") as f:
        contents = f.readlines()

        for index, line in enumerate(contents):
            if re.match(rf"^{old_version}", line):
                contents.insert(index - 1, changelog)
                break

        f.seek(0)
        f.writelines(contents)


def login(token: str) -> Repository | None:
    """Logins to github and returns the working repository."""
    github = github3.login(token=token)
    if not github:
        err_msg = "Failed to login to GitHub. Check the provided token."
        raise RuntimeError(err_msg)

    owner, repo = SLUG.split("/")

    return github.repository(owner, repo)


if __name__ == "__main__":
    main()
