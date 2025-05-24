"""Module containing constants used throughout all tests."""

import json
from pathlib import Path
from typing import Any


REPO_FOLDER: Path = Path(__file__).parent.parent
COOKIECUTTER_FOLDER: Path = REPO_FOLDER / "{{cookiecutter.project_name}}"
HOOKS_FOLDER: Path = REPO_FOLDER / "hooks"
SCRIPTS_FOLDER: Path = REPO_FOLDER / "scripts"

COOKIECUTTER_JSON_PATH: Path = REPO_FOLDER / "cookiecutter.json"
COOKIECUTTER_JSON: dict[str, Any] = json.loads(COOKIECUTTER_JSON_PATH.read_text())

MIN_PYTHON_SLUG: int = int(COOKIECUTTER_JSON["min_python_version"].lstrip("3."))
MAX_PYTHON_SLUG: int = int(COOKIECUTTER_JSON["max_python_version"].lstrip("3."))
PYTHON_VERSIONS: list[str] = [f"3.{VERSION_SLUG}" for VERSION_SLUG in range(MIN_PYTHON_SLUG, MAX_PYTHON_SLUG + 1)]
DEFAULT_PYTHON_VERSION: str = PYTHON_VERSIONS[1]


TYPE_CHECK_NOX_SESSIONS: list[str] = [f"typecheck-{python_version}" for python_version in PYTHON_VERSIONS]
TESTS_NOX_SESSIONS: list[str] = [f"tests-{python_version}" for python_version in PYTHON_VERSIONS]
CHECK_NOX_SESSIONS: list[str] = [f"check-{python_version}" for python_version in PYTHON_VERSIONS]
FULL_CHECK_NOX_SESSIONS: list[str] = [f"full-check-{python_version}" for python_version in PYTHON_VERSIONS]


GLOBAL_NOX_SESSIONS: list[str] = [
    "pre-commit",
    "format-python",
    "lint-python",
    *TYPE_CHECK_NOX_SESSIONS,
    "docs-build",
    "build-python",
    "build-container",
    "publish-python",
    "release",
    "tox",
    *CHECK_NOX_SESSIONS,
    *FULL_CHECK_NOX_SESSIONS,
    "coverage",
]

RUST_NOX_SESSIONS: list[str] = ["format-rust", "lint-rust", "tests-rust", "publish-rust"]
