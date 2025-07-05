import sys
from pathlib import Path
from typing import Annotated

import pre_commit.main
import typer
from retrocookie.core import retrocookie

from util import git
from util import FolderOption
from util import in_new_demo


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def lint_from_demo(
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    add_rust_extension: Annotated[bool, typer.Option("--add-rust-extension", "-r")] = False,
    no_cache: Annotated[bool, typer.Option("--no-cache", "-n")] = False
) -> None:
    """Runs precommit in a generated project and matches the template to the results."""
    try:
        with in_new_demo(
            demos_cache_folder=demos_cache_folder,
            add_rust_extension=add_rust_extension,
            no_cache=no_cache
        ) as demo_path:
            pre_commit.main.main(["run", "--all-files", "--hook-stage=manual", "--show-diff-on-failure"])
        try:
            retrocookie(instance_path=demo_path, commits=["HEAD"])
        finally:
            git("checkout", "HEAD", "--", "{{cookiecutter.project_name}}/pyproject.toml")
    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == '__main__':
    cli()
