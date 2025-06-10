"""Fixtures used in all tests for cookiecutter-robust-python."""

import subprocess
from pathlib import Path
from typing import Any

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.tmpdir import TempPathFactory
from cookiecutter.main import cookiecutter

from tests.constants import REPO_FOLDER


pytest_plugins: list[str] = ["pytester"]


@pytest.fixture(scope="session")
def demos_folder(tmp_path_factory: TempPathFactory) -> Path:
    """Temp Folder used for storing demos while testing."""
    return tmp_path_factory.mktemp("demos")


@pytest.mark.parametrize(argnames=["robust_demo__name"], argvalues=["robust-python-demo-no-setup"], indirect=True)
@pytest.mark.parametrize(argnames=["robust_demo__add_rust_extension"], argvalues=[False], indirect=True)
@pytest.fixture(scope="session")
def robust_python_demo_no_setup(request: FixtureRequest, robust_demo: Path) -> Path:
    return getattr(request, "param", robust_demo)


@pytest.mark.parametrize(argnames=["robust_demo__name"], argvalues=["robust-python-demo-with-setup"], indirect=True)
@pytest.mark.parametrize(argnames=["robust_demo__add_rust_extension"], argvalues=[False], indirect=True)
@pytest.fixture(scope="session")
def robust_python_demo_with_setup(request: FixtureRequest, robust_demo: Path) -> Path:
    subprocess.run(["nox", "-s", "setup-git"], cwd=robust_demo, capture_output=True)
    subprocess.run(["nox", "-s", "setup-venv"], cwd=robust_demo, capture_output=True)
    return getattr(request, "param", robust_demo)


@pytest.mark.parametrize(argnames=["robust_demo__name"], argvalues=["robust-maturin-demo-no-setup"], indirect=True)
@pytest.mark.parametrize(argnames=["robust_demo__add_rust_extension"], argvalues=[True], indirect=True)
@pytest.fixture(scope="session")
def robust_maturin_demo_no_setup(request: FixtureRequest, robust_demo: Path) -> Path:
    return getattr(request, "param", robust_demo)


@pytest.mark.parametrize(argnames=["robust_demo__name"], argvalues=["robust-maturin-demo-with-setup"], indirect=True)
@pytest.mark.parametrize(argnames=["robust_demo__add_rust_extension"], argvalues=[True], indirect=True)
@pytest.fixture(scope="session")
def robust_maturin_demo_with_setup(request: FixtureRequest, robust_demo: Path) -> Path:
    subprocess.run(["nox", "-s", "setup-git"], cwd=robust_demo, capture_output=True)
    subprocess.run(["nox", "-s", "setup-venv"], cwd=robust_demo, capture_output=True)
    return getattr(request, "param", robust_demo)


@pytest.fixture(scope="session")
def robust_demo(
    robust_demo__path: Path,
    robust_demo__extra_context: dict[str, Any]
) -> Path:
    cookiecutter(
        str(REPO_FOLDER),
        no_input=True,
        overwrite_if_exists=True,
        output_dir=robust_demo__path,
        extra_context=robust_demo__extra_context,
    )
    return robust_demo__path


@pytest.fixture(scope="session")
def robust_demo__path(request: FixtureRequest, demos_folder: Path, robust_demo__name: str) -> Path:
    return getattr(request, "param", demos_folder / robust_demo__name)


@pytest.fixture(scope="session")
def robust_demo__name(request: FixtureRequest) -> str:
    return getattr(request, "param", "robust-demo")


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
