"""Module used to sync the poetry.lock file with one generated using a demo project."""

import shutil
import sys
from pathlib import Path

import click

from loguru import logger


FOLDER_TYPE: click.Path = click.Path(dir_okay=True, file_okay=False, resolve_path=True, path_type=Path)


def sync_poetry_with_demo(template_folder: Path, demos_cache_folder: Path, demo_name: str) -> None:
    demo_root: Path = demos_cache_folder / demo_name
    demo_poetry_lock_path: Path = _find_poetry_lock_path(demo_root)
    output_poetry_lock_path: Path = _find_poetry_lock_path(template_folder)

    _copy_poetry_lock_from_demo(
        demo_poetry_lock_path=demo_poetry_lock_path, output_poetry_lock_path=output_poetry_lock_path
    )
    logger.info(f"Copied demo from {demo_poetry_lock_path=} to {output_poetry_lock_path=}.")


def _copy_poetry_lock_from_demo(demo_poetry_lock_path: Path, output_poetry_lock_path: Path) -> None:
    """Copies over the poetry.lock file from the provided demo project root."""
    shutil.copy(
        src=demo_poetry_lock_path,
        dst=output_poetry_lock_path,
    )


def _find_poetry_lock_path(search_root: Path) -> Path:
    for path in search_root.rglob("poetry.lock"):
        return path
    raise FileNotFoundError(f"Failed to find a poetry.lock within the provided search path: {search_root=}")


@click.command()
@click.option("--template-folder", "-t", required=True, type=FOLDER_TYPE)
@click.option("--demos-cache-folder", "-c", required=True, type=FOLDER_TYPE)
@click.option("--demo-name", "-d", required=True, type=str)
def main(template_folder: Path, demos_cache_folder: Path, demo_name: str) -> None:
    """Updates the poetry.lock file."""
    try:
        sync_poetry_with_demo(
            template_folder=template_folder, demos_cache_folder=demos_cache_folder, demo_name=demo_name
        )
    except Exception as error:
        click.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    main(prog_name="prepare-github-release")
