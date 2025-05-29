"""Script responsible for first time setup of the project's git repo.

Since this a first time setup script, we intentionally only use builtin Python dependencies.
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
    setup_git(path=args.path, github_user=args.github_user, repo_name=args.repo_name)


def setup_git(path: Path, github_user: str, repo_name: str) -> None:
    """Set up the provided cookiecutter-robust-python project's git repo."""
    commands: list[list[str]] = [
        ["git", "init"],
        ["git", "branch", "-M", "main"],
        ["git", "remote", "add", "origin", f"https://github.com/{github_user}/{repo_name}.git"],
        ["git", "remote", "set-url", "origin", f"https://github.com/{github_user}/{repo_name}.git"],
        ["git", "fetch", "origin"],
        ["git", "push", "-u", "origin", "main"],
        ["git", "checkout", "-b", "develop", "main"],
        ["git", "push", "-u", "origin", "develop"],
        ["git", "add", "."],
        ["git", "commit", "-m", "feat: initial commit"],
        ["git", "push", "origin", "develop"]
    ]
    check_dependencies(path=path, dependencies=["git"])

    for command in commands:
        subprocess.run(command, cwd=path, stdout=subprocess.STDOUT, stderr=subprocess.STDOUT)


def get_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for setup-git."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="setup-git",
        usage="python ./scripts/setup-git.py . -u 56kyle -n robust-python-demo",
        description="Set up the provided cookiecutter-robust-python project's git repo.",
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


if __name__ == '__main__':
    main()
