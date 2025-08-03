import sys
from pathlib import Path
from typing import Annotated

import cruft
import typer
from cookiecutter.utils import work_in

from util import get_demo_name
from util import git
from util import FolderOption
from util import REPO_FOLDER
from util import require_clean_and_up_to_date_repo


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def update_demo(
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    add_rust_extension: Annotated[bool, typer.Option("--add-rust-extension", "-r")] = False
) -> None:
    """Runs precommit in a generated project and matches the template to the results."""
    try:
        demo_name: str = get_demo_name(add_rust_extension=add_rust_extension)
        demo_path: Path = demos_cache_folder / demo_name
        typer.secho(f"Updating demo project at {demo_path=}.", fg="yellow")
        with work_in(demo_path):
            require_clean_and_up_to_date_repo()
            git("checkout", "develop")
            cruft.update(
                project_dir=demo_path,
                template_path=REPO_FOLDER,
                extra_context={"project_name": demo_name, "add_rust_extension": add_rust_extension},
            )
            git("add", ".")
            git("commit", "-m", "chore: update demo to the latest cookiecutter-robust-python", "--no-verify")
            git("push")

    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == '__main__':
    cli()
