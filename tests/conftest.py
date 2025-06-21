"""Fixtures used in all tests for cookiecutter-robust-python."""

import subprocess
from pathlib import Path
from typing import Any

import pytest
import toml
import yaml
from _pytest.fixtures import FixtureRequest
from _pytest.tmpdir import TempPathFactory
from cookiecutter.main import cookiecutter

from tests.constants import REPO_FOLDER


pytest_plugins: list[str] = ["pytester"]


@pytest.fixture(scope="session")
def demos_folder(tmp_path_factory: TempPathFactory) -> Path:
    """Temp Folder used for storing demos while testing."""
    return tmp_path_factory.mktemp("demos")


@pytest.fixture(scope="session")
def robust_yaml(request: FixtureRequest, robust_file: str) -> dict[str, Any]:
    return getattr(request, "param", yaml.safe_load(robust_file))


@pytest.fixture(scope="session")
def robust_toml(request: FixtureRequest, robust_file: str) -> dict[str, Any]:
    return getattr(request, "param", toml.load(robust_file))


@pytest.fixture(scope="session")
def robust_file(request: FixtureRequest, robust_file__path: Path) -> str:
    text: str = robust_file__path.read_text()
    return getattr(request, "param", text)


@pytest.fixture(scope="session")
def robust_file__path(request: FixtureRequest, robust_demo: Path, robust_file__path__relative: str) -> Path:
    return getattr(request, "param", robust_demo / robust_file__path__relative)


@pytest.fixture(scope="session")
def robust_file__path__relative(request: FixtureRequest) -> str:
    return getattr(request, "param", "./pyproject.toml")


@pytest.fixture(scope="session")
def robust_demo(
    request: FixtureRequest,
    demos_folder: Path,
    robust_demo__path: Path,
    robust_demo__extra_context: dict[str, Any],
    robust_demo__is_setup: bool
) -> Path:
    cookiecutter(
        str(REPO_FOLDER),
        no_input=True,
        overwrite_if_exists=True,
        output_dir=demos_folder,
        extra_context=robust_demo__extra_context,
    )
    if robust_demo__is_setup:
        subprocess.run(["nox", "-s", "setup-git"], cwd=robust_demo__path, capture_output=True)
        subprocess.run(["nox", "-s", "setup-venv"], cwd=robust_demo__path, capture_output=True)
    return getattr(request, "param", robust_demo__path)


@pytest.fixture(scope="session")
def robust_demo__path(request: FixtureRequest, demos_folder: Path, robust_demo__name: str) -> Path:
    return getattr(request, "param", demos_folder / robust_demo__name)


@pytest.fixture(scope="session")
def robust_demo__name(request: FixtureRequest) -> str:
    return getattr(request, "param", "robust-python-demo-with-setup")


@pytest.fixture(scope="session")
def robust_demo__extra_context(
    request: FixtureRequest,
    robust_demo__name: str,
    robust_demo__add_rust_extension: bool
) -> dict[str, Any]:
    return getattr(request, "param", {
        "project_name": robust_demo__name,
        "add_rust_extension": robust_demo__add_rust_extension
    })


@pytest.fixture(scope="session")
def robust_demo__add_rust_extension(request: FixtureRequest) -> bool:
    return getattr(request, "param", False)


@pytest.fixture(scope="session")
def robust_demo__is_setup(request: FixtureRequest) -> bool:
    return getattr(request, "param", True)
