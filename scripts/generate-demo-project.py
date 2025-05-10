"""Python script for generating a demo project."""

import shutil
import sys
from functools import partial
from pathlib import Path
from typing import Annotated

import typer

from cookiecutter.main import cookiecutter
from typer.models import OptionInfo

FolderOption: partial[OptionInfo] = partial(
    typer.Option,
    dir_okay=True,
    file_okay=False,
    resolve_path=True,
    path_type=Path
)


def generate_demo_project(repo_folder: Path, demos_cache_folder: Path, demo_name: str) -> Path:
    """Generates a demo project and returns its root path."""
    demos_cache_folder.mkdir(exist_ok=True)
    _remove_any_existing_demo(demos_cache_folder)
    cookiecutter(
        template=str(repo_folder),
        no_input=True,
        extra_context={"project_name": demo_name},
        overwrite_if_exists=True,
        output_dir=str(demos_cache_folder),
    )
    return demos_cache_folder / demo_name


def _remove_any_existing_demo(parent_path: Path) -> None:
    """Removes any existing demos."""
    for path in parent_path.iterdir():
        shutil.rmtree(path)


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def main(
    repo_folder: Annotated[Path, FolderOption("--repo-folder", "-r")],
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    demo_name: Annotated[str, typer.Option("--demo-name", "-d")]
) -> None:
    """Updates the poetry.lock file."""
    try:
        generate_demo_project(repo_folder=repo_folder, demos_cache_folder=demos_cache_folder, demo_name=demo_name)
    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    cli()
