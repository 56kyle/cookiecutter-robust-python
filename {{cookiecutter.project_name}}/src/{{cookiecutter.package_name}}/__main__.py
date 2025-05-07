"""Command-line interface."""

import typer


@typer.command()
@typer.version_option()
def main() -> None:
    """{{cookiecutter.friendly_name}}."""


if __name__ == "__main__":
    main(prog_name="{{cookiecutter.project_name}}")  # pragma: no cover
