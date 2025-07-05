"""Script responsible for preparing a release of the {{cookiecutter.project_name}} package."""

import argparse
import re
import shutil
import subprocess
from pathlib import Path
from re import Match
from typing import Literal
from typing import Optional
from typing import Pattern
from typing import TypeAlias


from util import check_dependencies
from util import remove_readonly
from util import REPO_FOLDER


Increment: TypeAlias = Literal["major", "minor", "patch", "prerelease"]
CZ_PATTERN: Pattern[str] = re.compile(r"bump: version (?P<current_version>.*?) → (?P<new_version>.*?)")


def main() -> None:
    """Parses args and passes through to prepare_release."""
    parser: argparse.ArgumentParser = get_parser()
    args: argparse.Namespace = parser.parse_args()
    prepare_release(path=args.path, python_version=args.python_version)


def get_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for prepare-release."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="prepare-release", usage="python ./scripts/prepare-release.py patch"
    )
    parser.add_argument(
        "increment",
        type=str,
        help="Increment type to use when preparing the release.",
        choices=["major", "minor", "patch", "prerelease"],
    )
    return parser


def prepare_release(increment: Optional[str] = None) -> None:
    """Prepares a release of the {{cookiecutter.project_name}} package.

    Sets up a release branch from the branch develop, bumps the version, and creates a release commit. Does not tag the
    release or push any changes.
    """
    dry_run_cmd: list[str] = ["uvx", "cz", "bump", "--dry-run", "--yes"]
    bump_cmd: list[str] = ["uvx", "cz", "bump", "--yes", "--files-only", "--changelog"]
    if increment is not None:
        dry_run_cmd.extend(["--increment", increment])
        bump_cmd.extend(["--increment", increment])

    result: subprocess.CompletedProcess = subprocess.run(dry_run_cmd, cwd=REPO_FOLDER, capture_output=True)
    match: Match = re.match(CZ_PATTERN, result.stdout)
    current_version: str = match.group("current_version")
    new_version: str = match.group("new_version")

    commands: list[list[str]] = [
        ["git", "status", "--porcelain"],
        ["git", "branch", "-b", f"release/{new_version}", "develop"],
        ["git", "checkout", f"release/{new_version}"],
        bump_cmd,
        ["git", "add", "."],
        ["git", "commit", "-m", f"bump: version {current_version} → {new_version}"]
    ]

    check_dependencies(path=REPO_FOLDER, dependencies=["git", "cz"])

    for command in commands:
        subprocess.run(command, cwd=REPO_FOLDER, capture_output=True, check=True)


if __name__ == "__main__":
    main()


