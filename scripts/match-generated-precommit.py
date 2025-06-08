import sys
from pathlib import Path
from typing import Annotated

import pre_commit.main
import typer
from retrocookie.core import retrocookie

from util import FolderOption
from util import in_new_demo


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def match_generated_precommit(
    repo_folder: Annotated[Path, FolderOption("--repo-folder", "-r")],
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    demo_name: Annotated[str, typer.Option("--demo-name", "-d")],
    no_cache: Annotated[bool, typer.Option("--no-cache", "-n")] = False,
) -> None:
    """Runs precommit in a generated project and matches the template to the results."""
    try:
        with in_new_demo(
            repo_folder=repo_folder,
            demos_cache_folder=demos_cache_folder,
            demo_name=demo_name,
            no_cache=no_cache
        ) as demo_path:
            pre_commit.main.main(["run", "--all-files", "--hook-stage=manual", "--show-diff-on-failure"])
        retrocookie(instance_path=demo_path, commits=["HEAD"])
    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == '__main__':
    cli()
