"""Module used to sync the uv.lock file with one generated using a demo project."""

import shutil
import sys
from functools import partial
from pathlib import Path
from typing import Annotated

import typer
from loguru import logger
from typer.models import OptionInfo


FolderOption: partial[OptionInfo] = partial(
    typer.Option, dir_okay=True, file_okay=False, resolve_path=True, path_type=Path
)


def sync_uv_with_demo(template_folder: Path, demos_cache_folder: Path, demo_name: str) -> None:
    demo_root: Path = demos_cache_folder / demo_name
    demo_uv_lock_path: Path = _find_uv_lock_path(demo_root)
    output_uv_lock_path: Path = _find_uv_lock_path(template_folder)

    _copy_uv_lock_from_demo(demo_uv_lock_path=demo_uv_lock_path, output_uv_lock_path=output_uv_lock_path)
    logger.info(f"Copied demo from {demo_uv_lock_path=} to {output_uv_lock_path=}.")


def _copy_uv_lock_from_demo(demo_uv_lock_path: Path, output_uv_lock_path: Path) -> None:
    """Copies over the uv.lock file from the provided demo project root."""
    shutil.copy(
        src=demo_uv_lock_path,
        dst=output_uv_lock_path,
    )


def _find_uv_lock_path(search_root: Path) -> Path:
    for path in search_root.rglob("uv.lock"):
        return path
    raise FileNotFoundError(f"Failed to find a uv.lock within the provided search path: {search_root=}")


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def main(
    template_folder: Annotated[Path, FolderOption("--template-folder", "-t", exists=True)],
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c", exists=True)],
    demo_name: Annotated[str, typer.Option("--demo-name", "-d")],
) -> None:
    """Updates the uv.lock file."""
    try:
        sync_uv_with_demo(template_folder=template_folder, demos_cache_folder=demos_cache_folder, demo_name=demo_name)
    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    cli()
