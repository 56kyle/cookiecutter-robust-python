"""Module containing utility functions used throughout cookiecutter_robust_python scripts."""
import os
import shutil
import stat
import subprocess
import sys
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Generator

import typer
from cookiecutter.main import cookiecutter
from cookiecutter.utils import rmtree
from cookiecutter.utils import work_in
from pygments.lexers import q


def remove_readonly(func: Callable[[str], Any], path: str, _: Any) -> None:
    """Clears the readonly bit and attempts to call the provided function.

    Meant for use as the onerror callback in shutil.rmtree.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


def run_command(command: str, *args: str) -> subprocess.CompletedProcess:
    """Runs the provided command in a subprocess."""
    try:
        process = subprocess.run([command, *args], check=True, capture_output=True, text=True)
        return process
    except subprocess.CalledProcessError as error:
        print(error.stdout, end="")
        print(error.stderr, end="", file=sys.stderr)
        raise


git: partial[subprocess.CompletedProcess] = partial(run_command, "git")
uv: partial[subprocess.CompletedProcess] = partial(run_command, "uv")


@contextmanager
def in_new_demo(
    repo_folder: Path,
    demos_cache_folder: Path,
    demo_name: str,
    no_cache: bool,
    **kwargs: Any
) -> Generator[Path]:
    """Returns a context manager for working within a new demo."""
    demo_path: Path = generate_demo_project(
        repo_folder=repo_folder,
        demos_cache_folder=demos_cache_folder,
        demo_name=demo_name,
        no_cache=no_cache,
        **kwargs
    )
    with work_in(demo_path):
        yield demo_path


def generate_demo_project(
    repo_folder: Path,
    demos_cache_folder: Path,
    demo_name: str,
    no_cache: bool,
    **kwargs: Any
) -> Path:
    """Generates a demo project and returns its root path."""
    demos_cache_folder.mkdir(exist_ok=True)
    if no_cache:
        _remove_existing_demo(demo_path=demos_cache_folder / demo_name)
    cookiecutter(
        template=str(repo_folder),
        no_input=True,
        extra_context={"project_name": demo_name, **kwargs},
        overwrite_if_exists=True,
        output_dir=str(demos_cache_folder),
    )
    return demos_cache_folder / demo_name


def _remove_existing_demo(demo_path: Path) -> None:
    """Removes the existing demo if present."""
    if demo_path.exists() and demo_path.is_dir():
        previous_demo_pyproject: Path = Path(demo_path, "pyproject.toml")
        if not previous_demo_pyproject.exists():
            typer.secho(f"No pyproject.toml found at {previous_demo_pyproject=}.", fg="red")
            typer.confirm(
                "This folder may not be a demo, are you sure you would like to continue?",
                default=False,
                abort=True,
                show_default=True
            )

        typer.secho(f"Removing existing demo project at {demo_path=}.", fg="yellow")
        shutil.rmtree(demo_path, onerror=remove_readonly)




