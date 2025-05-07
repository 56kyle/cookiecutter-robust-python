"""Python script for generating a demo project."""

import shutil
import sys
from pathlib import Path
from typing import Annotated

import typer

from cookiecutter.main import cookiecutter

FOLDER_TYPE: click.Path = click.Path(dir_okay=True, file_okay=False, resolve_path=True, path_type=Path)


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


@typer.command()
@click.option("--repo-folder", "-r", required=True, type=FOLDER_TYPE)
@click.option("--demos-cache-folder", "-c", required=True, type=FOLDER_TYPE)
@click.option("--demo-name", "-d", required=True, type=str)
def main(
    repo_folder: Annotated[Path, typer.Option()],
    demos_cache_folder: Path,
        demo_name: str
) -> None:
    """Updates the poetry.lock file."""
    try:
        generate_demo_project(repo_folder=repo_folder, demos_cache_folder=demos_cache_folder, demo_name=demo_name)
    except Exception as error:
        click.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    main(prog_name="generate-demo-project")
