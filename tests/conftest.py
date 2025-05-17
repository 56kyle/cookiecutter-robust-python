"""Fixtures used in all tests for cookiecutter-robust-python."""

import os
import subprocess

from pathlib import Path
from typing import Generator

import pytest
from _pytest.tmpdir import TempPathFactory
from cookiecutter.main import cookiecutter

from tests.constants import REPO_FOLDER


pytest_plugins: list[str] = ["pytester"]


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
    path: Path = demos_path / "robust-python-demo"
    subprocess.run(["uv", "lock"], cwd=path)
    return path


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
    path: Path = demos_path / "robust-maturin-demo"
    subprocess.run(["uv", "sync"], cwd=path)
    return path


@pytest.fixture(scope="function")
def inside_robust_python_demo(robust_python_demo_path: Path) -> Generator[Path, None, None]:
    """Changes the current working directory to the robust-python-demo project."""
    original_path: Path = Path.cwd()
    os.chdir(robust_python_demo_path)
    yield robust_python_demo_path
    os.chdir(original_path)


@pytest.fixture(scope="function")
def inside_robust_maturin_demo(robust_maturin_demo_path: Path) -> Generator[Path, None, None]:
    original_path: Path = Path.cwd()
    os.chdir(robust_maturin_demo_path)
    yield robust_maturin_demo_path
    os.chdir(original_path)
