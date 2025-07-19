"""Script responsible for bumping the version of the {{cookiecutter.project_name}} package."""

import argparse

from util import bump_version


def main() -> None:
    """Parses args and passes through to bump_version."""
    parser: argparse.ArgumentParser = get_parser()
    args: argparse.Namespace = parser.parse_args()
    bump_version(increment=args.increment)


def get_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for prepare-release."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="bump-version", usage="python ./scripts/bump-version.py patch"
    )
    parser.add_argument(
        "increment",
        type=str,
        help="Increment type to use when preparing the release.",
        choices=["MAJOR", "MINOR", "PATCH", "PRERELEASE"],
    )
    return parser


if __name__ == "__main__":
    main()
