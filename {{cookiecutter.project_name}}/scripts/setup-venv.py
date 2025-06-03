"""Script responsible for first time setup of the project's venv.

Since this a first time setup script, we intentionally only use builtin Python dependencies.
"""
import argparse
import shutil
import subprocess
from pathlib import Path

from util import check_dependencies
from util import existing_dir
from util import remove_readonly


def main() -> None:
    """Parses args and passes through to setup_venv."""
    parser: argparse.ArgumentParser = get_parser()
    args: argparse.Namespace = parser.parse_args()
    setup_venv(path=args.path, python_version=args.python_version)


def get_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for setup-venv."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="setup-venv",
        usage="python ./scripts/setup-venv.py . -p '3.9'"
    )
    parser.add_argument(
        "path",
        type=existing_dir,
        metavar="PATH",
        help="Path to the repo's root directory (must already exist).",
    )
    parser.add_argument(
        "-p",
        "--python",
        dest="python_version",
        help="The Python version that will serve as the main working version used by the IDE."
    )
    return parser


def setup_venv(path: Path, python_version: str) -> None:
    """Set up the provided cookiecutter-robust-python project's venv."""
    commands: list[list[str]] = [
        ["uv", "lock"],
        ["uv", "venv", ".venv"],
        ["uv", "python", "install", python_version],
        ["uv", "python", "pin", python_version],
        ["uv", "sync", "--all-groups"]
    ]
    check_dependencies(path=path, dependencies=["uv"])

    venv_path: Path = path / ".venv"
    if venv_path.exists():
        shutil.rmtree(venv_path, onerror=remove_readonly)

    for command in commands:
        subprocess.run(command, cwd=path, capture_output=True)


if __name__ == '__main__':
    main()
