"""Python script for generating a demo project."""
import sys
from functools import partial
from pathlib import Path
from typing import Annotated

import typer

from util import FolderOption
from util import generate_demo


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def main(
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    demo_name: Annotated[str, typer.Option("--demo-name", "-d")],
    no_cache: Annotated[bool, typer.Option("--no-cache", "-n")] = False,
) -> None:
    """Updates the poetry.lock file."""
    try:
        generate_demo(
            demos_cache_folder=demos_cache_folder,
            demo_name=demo_name,
            no_cache=no_cache,

        )
    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    cli()
