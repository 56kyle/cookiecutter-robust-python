import sys
from pathlib import Path
from typing import Any

import pre_commit.main
import typer
from retrocookie.core import retrocookie

from scripts.util import in_new_demo


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def match_generated_precommit(
    repo_folder: Path,
    demos_cache_folder: Path,
    demo_name: str,
    no_cache: bool,
    **kwargs: Any
) -> None:
    """Runs precommit in a generated project and matches the template to the results."""
    try:
        with in_new_demo(
            repo_folder=repo_folder,
            demos_cache_folder=demos_cache_folder,
            demo_name=demo_name,
            no_cache=no_cache,
            **kwargs
        ) as demo_path:
            pre_commit.main.main(["run", "--all-files", "--hook-stage=manual", "--show-diff-on-failure"])
        retrocookie(instance_path=demo_path, commits=["HEAD"])
    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == '__main__':
    cli()
