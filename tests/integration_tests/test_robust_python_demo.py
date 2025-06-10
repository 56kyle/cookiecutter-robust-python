"""Tests project generation and template functionality using a Python build backend."""

import subprocess
from pathlib import Path

import pytest

from tests.constants import GLOBAL_NOX_SESSIONS


def test_demo_project_generation(robust_python_demo_path: Path) -> None:
    assert robust_python_demo_path.exists()


@pytest.mark.parametrize("session", GLOBAL_NOX_SESSIONS)
def test_demo_project_nox_session(robust_python_demo_path: Path, session: str) -> None:
    command: list[str] = ["nox", "-s", session]
    result: subprocess.CompletedProcess = subprocess.run(
        command,
        cwd=robust_python_demo_path,
        capture_output=True,
    )
    print(result.stdout)
    print(result.stderr)
    result.check_returncode()


def test_demo_project_nox_pre_commit(robust_python_demo_path: Path) -> None:
    command: list[str] = ["nox", "-s", "pre-commit"]
    result: subprocess.CompletedProcess = subprocess.run(
        command,
        cwd=robust_python_demo_path,
        capture_output=True,
        text=True,
        timeout=20.0
    )
    assert result.returncode == 0


def test_demo_project_nox_pre_commit_with_install(robust_python_demo_path: Path) -> None:
    command: list[str] = ["nox", "-s", "pre-commit", "--", "install"]
    pre_commit_hook_path: Path = robust_python_demo_path / ".git" / "hooks" / "pre-commit"
    assert not pre_commit_hook_path.exists()

    result: subprocess.CompletedProcess = subprocess.run(
        command,
        cwd=robust_python_demo_path,
        capture_output=True,
        text=True,
        timeout=20.0
    )
    assert pre_commit_hook_path.exists()
    assert pre_commit_hook_path.is_file()

    assert result.returncode == 0



