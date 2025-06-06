"""Script responsible for first time setup of the project's git repo's remote connection.

Since this is a first time setup script, we intentionally only use builtin Python dependencies.
"""

import argparse
import subprocess
from pathlib import Path

from util import check_dependencies
from util import existing_dir


def main() -> None:
    """Parses command line input and passes it through to setup_git."""
    parser: argparse.ArgumentParser = get_parser()
    args: argparse.Namespace = parser.parse_args()
    setup_remote(path=args.path, github_user=args.github_user, repo_name=args.repo_name)


def setup_remote(path: Path, github_user: str, repo_name: str) -> None:
    """Set up the provided cookiecutter-robust-python project's git repo."""
    commands: list[list[str]] = [
        ["git", "fetch", "origin"],
        ["git", "remote", "add", "origin", f"https://github.com/{github_user}/{repo_name}.git"],
        ["git", "remote", "set-url", "origin", f"https://github.com/{github_user}/{repo_name}.git"],
        ["git", "pull"],
        ["git", "checkout", "main"],
        ["git", "push", "-u", "origin", "main"],
        ["git", "checkout", "develop"],
        ["git", "push", "-u", "origin", "develop"],
    ]
    check_dependencies(path=path, dependencies=["git"])

    for command in commands:
        subprocess.run(command, cwd=path, stderr=subprocess.STDOUT)


def get_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for setup-git."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="setup-git",
        usage="python ./scripts/setup-remote.py . -u 56kyle -n robust-python-demo",
        description="Set up the provided cookiecutter-robust-python project's remote repo connection.",
    )
    parser.add_argument(
        "path",
        type=existing_dir,
        metavar="PATH",
        help="Path to the repo's root directory (must already exist).",
    )
    parser.add_argument("-u", "--user", dest="github_user", help="GitHub user name.")
    parser.add_argument("-n", "--name", dest="repo_name", help="Name of the repo.")
    return parser
