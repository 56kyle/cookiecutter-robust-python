"""Fixtures used in all tests for cookiecutter-robust-python."""

import subprocess
from pathlib import Path

import pytest
from _pytest.tmpdir import TempPathFactory
from cookiecutter.main import cookiecutter

from tests.constants import REPO_FOLDER


pytest_plugins: list[str] = ["pytester"]


@pytest.fixture(scope="session")
def demos_folder(tmp_path_factory: TempPathFactory) -> Path:
    """Temp Folder used for storing demos while testing."""
    return tmp_path_factory.mktemp("demos")


@pytest.fixture(scope="session")
def robust_python_demo_path(demos_folder: Path) -> Path:
    """Creates a temporary example python project for testing against and returns its Path."""
    cookiecutter(
        str(REPO_FOLDER),
        no_input=True,
        overwrite_if_exists=True,
        output_dir=demos_folder,
        extra_context={"project_name": "robust-python-demo", "add_rust_extension": False},
    )
    path: Path = demos_folder / "robust-python-demo"
    subprocess.run(["nox", "-s", "setup-repo"], cwd=path, capture_output=True)
    return path


@pytest.fixture(scope="session")
def robust_maturin_demo_path(demos_folder: Path) -> Path:
    """Creates a temporary example maturin project for testing against and returns its Path."""
    cookiecutter(
        str(REPO_FOLDER),
        no_input=True,
        overwrite_if_exists=True,
        output_dir=demos_folder,
        extra_context={"project_name": "robust-maturin-demo", "add_rust_extension": True}
    )
    path: Path = demos_folder / "robust-maturin-demo"
    subprocess.run(["nox", "-s", "setup-repo"], cwd=path, capture_output=True)
    return path

