"""Python script for generating a demo project."""
import os
import shutil
import stat
import sys
from functools import partial
from pathlib import Path
from typing import Annotated
from typing import Any
from typing import Callable

import typer
from cookiecutter.main import cookiecutter
from typer.models import OptionInfo


FolderOption: partial[OptionInfo] = partial(
    typer.Option, dir_okay=True, file_okay=False, resolve_path=True, path_type=Path
)


def generate_demo_project(repo_folder: Path, demos_cache_folder: Path, demo_name: str, no_cache: bool) -> Path:
    """Generates a demo project and returns its root path."""
    demos_cache_folder.mkdir(exist_ok=True)
    if no_cache:
        _remove_existing_demo(demo_path=demos_cache_folder / demo_name)
    cookiecutter(
        template=str(repo_folder),
        no_input=True,
        extra_context={"project_name": demo_name},
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


def remove_readonly(func: Callable[[str], Any], path: str, _: Any) -> None:
    """Clears the readonly bit and attempts to call the provided function."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def main(
    repo_folder: Annotated[Path, FolderOption("--repo-folder", "-r")],
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    demo_name: Annotated[str, typer.Option("--demo-name", "-d")],
    no_cache: Annotated[bool, typer.Option("--no-cache", "-n")] = False,
) -> None:
    """Updates the poetry.lock file."""
    try:
        generate_demo_project(
            repo_folder=repo_folder,
            demos_cache_folder=demos_cache_folder,
            demo_name=demo_name,
            no_cache=no_cache
        )
    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    cli()
