"""Script responsible for getting the release notes of the {{cookiecutter.project_name}} package."""
from pathlib import Path

from util import get_latest_release_notes


RELEASE_NOTES_PATH: Path = Path("body.md")


def main() -> None:
    """Parses args and passes through to bump_version."""
    get_latest_release_notes()


if __name__ == "__main__":
    main()
