"""Script responsible for getting the release notes of the {{cookiecutter.project_name}} package."""

import argparse
from pathlib import Path

from util import get_latest_release_notes


RELEASE_NOTES_PATH: Path = Path("body.md")


def main() -> None:
    """Parses args and passes through to bump_version."""
    parser: argparse.ArgumentParser = get_parser()
    args: argparse.Namespace = parser.parse_args()
    release_notes: str = get_latest_release_notes()
    path: Path = RELEASE_NOTES_PATH if args.path is None else args.path
    path.write_text(release_notes)


def get_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for prepare-release."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="get-release-notes", usage="python ./scripts/get-release-notes.py"
    )
    parser.add_argument(
        "path",
        type=Path,
        metavar="PATH",
        help="Path the changelog will be written to.",
    )
    return parser


if __name__ == "__main__":
    main()
