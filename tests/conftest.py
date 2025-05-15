"""Fixtures used in all tests for cookiecutter-robust-python."""
import json
import os
from pathlib import Path
from typing import Any, Generator

import platformdirs
import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.tmpdir import TempPathFactory
from cookiecutter.main import cookiecutter


pytest_plugins: list[str] = ["pytester"]


REPO_FOLDER: Path = Path(__file__).parent.parent
COOKIECUTTER_FOLDER: Path = REPO_FOLDER / "{{cookiecutter.project_name}}"
HOOKS_FOLDER: Path = REPO_FOLDER / "hooks"
SCRIPTS_FOLDER: Path = REPO_FOLDER / "scripts"

COOKIECUTTER_JSON_PATH: Path = COOKIECUTTER_FOLDER / "cookiecutter.json"
COOKIECUTTER_JSON: dict[str, Any] = json.loads(COOKIECUTTER_JSON_PATH.read_text())


@pytest.fixture(scope="session")
def robust_python_demo_path(tmp_path_factory: TempPathFactory) -> Path:
    """Creates a temporary example python project for testing against and returns its Path."""
    demos_path: Path = tmp_path_factory.mktemp("demos")
    cookiecutter(
        str(REPO_FOLDER),
        no_input=True,
        overwrite_if_exists=True,
        output_dir=demos_path,
        extra_context={
            "project_name": "robust-python-demo",
            "add_rust_extension": False
        }
    )
    return demos_path / "robust-python-demo"


@pytest.fixture(scope="session")
def robust_maturin_demo_path(tmp_path_factory: TempPathFactory) -> Path:
    """Creates a temporary example maturin project for testing against and returns its Path."""
    demos_path: Path = tmp_path_factory.mktemp("demos")
    cookiecutter(
        str(REPO_FOLDER),
        no_input=True,
        overwrite_if_exists=True,
        output_dir=demos_path,
        extra_context={
            "project_name": "robust-maturin-demo",
            "add_rust_extension": True
        }
    )
    return demos_path / "robust-maturin-demo"


@pytest.fixture(scope="function")
def inside_robust_python_demo(robust_python_demo_path: Path) -> Generator[Path, None, None]:
    """Changes the current working directory to the robust-python-demo project."""
    original_path: Path = Path.cwd()
    os.chdir(robust_python_demo_path)
    yield robust_python_demo_path
    os.chdir(original_path)


