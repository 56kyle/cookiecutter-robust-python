"""Tests project generation and template functionality using a Python build backend."""
import subprocess
from pathlib import Path

import pytest

from tests.constants import GLOBAL_NOX_SESSIONS


def test_demo_project_generation(robust_python_demo_path: Path) -> None:
    assert robust_python_demo_path.exists()


@pytest.mark.parametrize("session", GLOBAL_NOX_SESSIONS)
def test_demo_project_noxfile(robust_python_demo_path: Path, session: str) -> None:
    command: list[str] = ["uvx", "nox", "-s", session]
    result: subprocess.CompletedProcess = subprocess.run(
        command,
        cwd=robust_python_demo_path,
        capture_output=True,
        text=True,
        timeout=10.0,
    )
    print(result.stdout)
    print(result.stderr)
    result.check_returncode()



