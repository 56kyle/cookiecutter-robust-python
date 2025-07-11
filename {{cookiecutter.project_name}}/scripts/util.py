"""Module containing util."""

import argparse
import stat
import subprocess
from pathlib import Path
from typing import Any
from typing import Callable


class MissingDependencyError(Exception):
    """Exception raised when a depedency is missing from the system running setup-repo."""

    def __init__(self, project: Path, dependency: str):
        """Initializes MisssingDependencyError."""
        message_lines: list[str] = [
            f"Unable to find {dependency=}.",
            f"Please ensure that {dependency} is installed before setting up the repo at {project.absolute()}",
        ]
        message: str = "\n".join(message_lines)
        super().__init__(message)


def check_dependencies(path: Path, dependencies: list[str]) -> None:
    """Checks for any passed dependencies."""
    for dependency in dependencies:
        try:
            subprocess.check_call([dependency, "--version"], cwd=path)
        except subprocess.CalledProcessError as e:
            raise MissingDependencyError(path, dependency) from e


def existing_dir(value: str) -> Path:
    """Responsible for validating argparse inputs and returning them as pathlib Path's if they meet criteria."""
    path = Path(value).expanduser().resolve()

    if not path.exists():
        raise argparse.ArgumentTypeError(f"{path} does not exist.")
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"{path} is not a directory.")

    return path


def remove_readonly(func: Callable[[str], Any], path: str, _: Any) -> None:
    """Clears the readonly bit and attempts to call the provided function.

    This is passed to shutil.rmtree as the onerror kwarg.
    """
    Path(path).chmod(stat.S_IWRITE)
    func(path)
