"""Command-line interface."""

import typer


app: typer.Typer = typer.Typer()


@app.command(name="{{cookiecutter.project_name}}")
def main() -> None:
    """{{cookiecutter.friendly_name}}."""


if __name__ == "__main__":
    app()
