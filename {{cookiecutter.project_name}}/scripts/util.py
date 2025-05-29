"""Module containing util"""
import argparse
import subprocess
from pathlib import Path


class MissingDependencyError(Exception):
    """Exception raised when a depedency is missing from the system running setup-repo."""
    def __init__(self, project: Path, dependency: str):
        super().__init__("\n".join([
            f"Unable to find {dependency=}.",
            f"Please ensure that {dependency} is installed before setting up the repo at {project.absolute()}"
        ]))


def check_dependencies(path: Path, dependencies: list[str]) -> None:
    """Checks for any passed dependencies."""
    for dependency in dependencies:
        try:
            subprocess.check_call([dependency, "--version"], cwd=path)
        except subprocess.CalledProcessError:
            raise MissingDependencyError(path, dependency)


def existing_dir(value: str) -> Path:
    """Responsible for validating argparse inputs and returning them as pathlib Path's if they meet criteria."""
    path = Path(value).expanduser().resolve()

    if not path.exists():
        raise argparse.ArgumentTypeError(f"{path} does not exist.")
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"{path} is not a directory.")

    return path
