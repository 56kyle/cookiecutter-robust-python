"""Noxfile for the cookiecutter-robust-python template."""
import os
import shutil
import tempfile
from pathlib import Path

import nox
import platformdirs
from nox.command import CommandFailed
from nox.sessions import Session


nox.options.default_venv_backend = "uv"

DEFAULT_TEMPLATE_PYTHON_VERSION = "3.9"

REPO_ROOT: Path = Path(__file__).parent.resolve()
SCRIPTS_FOLDER: Path = REPO_ROOT / "scripts"
TEMPLATE_FOLDER: Path = REPO_ROOT / "{{cookiecutter.project_name}}"


COOKIECUTTER_ROBUST_PYTHON_CACHE_FOLDER: Path = Path(
    platformdirs.user_cache_path(
        appname="cookiecutter-robust-python",
        appauthor="56kyle",
        ensure_exists=True,
    )
).resolve()

DEFAULT_PROJECT_DEMOS_FOLDER = COOKIECUTTER_ROBUST_PYTHON_CACHE_FOLDER / "project_demos"
PROJECT_DEMOS_FOLDER: Path = Path(os.getenv(
    "COOKIECUTTER_ROBUST_PYTHON_PROJECT_DEMOS_FOLDER", default=DEFAULT_PROJECT_DEMOS_FOLDER
)).resolve()
DEFAULT_DEMO_NAME: str = "robust-python-demo"
DEMO_ROOT_FOLDER: Path = PROJECT_DEMOS_FOLDER / DEFAULT_DEMO_NAME

GENERATE_DEMO_PROJECT_SCRIPT: Path = SCRIPTS_FOLDER / "generate-demo-project.py"
GENERATE_DEMO_PROJECT_OPTIONS: tuple[str, ...] = (
    *("--repo-folder", REPO_ROOT),
    *("--demos-cache-folder", PROJECT_DEMOS_FOLDER),
    *("--demo-name", DEFAULT_DEMO_NAME),
)

SYNC_UV_WITH_DEMO_SCRIPT: Path = SCRIPTS_FOLDER / "sync-uv-with-demo.py"
SYNC_UV_WITH_DEMO_OPTIONS: tuple[str, ...] = (
    *("--template-folder", TEMPLATE_FOLDER),
    *("--demos-cache-folder", PROJECT_DEMOS_FOLDER),
    *("--demo-name", DEFAULT_DEMO_NAME),
)


@nox.session(name="generate-demo-project", python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def generate_demo_project(session: Session) -> None:
    """Generates a project demo using the cookiecutter-robust-python template."""
    session.install("cookiecutter", "platformdirs", "loguru", "typer")
    session.run(
        "python",
        GENERATE_DEMO_PROJECT_SCRIPT,
        *GENERATE_DEMO_PROJECT_OPTIONS,
        *session.posargs
    )


@nox.session(name="sync-uv-with-demo", python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def sync_uv_with_demo(session: Session) -> None:
    """Syncs the uv environment with the current demo project."""
    session.install("cookiecutter", "platformdirs", "loguru", "typer")
    session.run(
        "python",
        SYNC_UV_WITH_DEMO_SCRIPT,
        *SYNC_UV_WITH_DEMO_OPTIONS,
    )


@nox.session(name="uv-in-demo", python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def uv_in_demo(session: Session) -> None:
    """Runs a uv command in a new project demo project then syncs with it."""
    session.install("cookiecutter", "platformdirs", "loguru", "typer")
    session.run(
        "python",
        GENERATE_DEMO_PROJECT_SCRIPT,
        *GENERATE_DEMO_PROJECT_OPTIONS,
    )
    original_dir: Path = Path.cwd()
    session.cd(DEMO_ROOT_FOLDER)
    session.run("uv", *session.posargs)
    session.cd(original_dir)
    session.run(
        SYNC_UV_WITH_DEMO_SCRIPT,
        *SYNC_UV_WITH_DEMO_OPTIONS,
        external=True,
    )


@nox.session(name="in-demo", python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def in_demo(session: Session) -> None:
    """Generates a project demo and run a uv command in it."""
    session.install("cookiecutter", "platformdirs", "loguru", "typer")
    session.run(
        "python",
        GENERATE_DEMO_PROJECT_SCRIPT,
        *GENERATE_DEMO_PROJECT_OPTIONS,
    )
    original_dir: Path = Path.cwd()
    session.cd(DEMO_ROOT_FOLDER)
    session.run(*session.posargs)
    session.cd(original_dir)


@nox.session(name="clear-cache", python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def clear_cache(session: Session) -> None:
    """Clear the cache of generated project demos.

    Not commonly used, but sometimes permissions might get messed up if exiting mid-build and such.
    """
    session.log("Clearing cache of generated project demos...")
    shutil.rmtree(PROJECT_DEMOS_FOLDER, ignore_errors=True)
    session.log("Cache cleared.")


@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def lint(session: Session):
    """Lint the template's own Python files and configurations."""
    session.log("Installing linting dependencies for the template source...")
    session.install("-e", ".", "--group", "dev", "--group", "lint")

    session.log(f"Running Ruff formatter check on template files with py{session.python}.")
    session.run("ruff", "format")

    session.log(f"Running Ruff check on template files with py{session.python}.")
    session.run("ruff", "check", "--verbose", "--fix")


@nox.session(python=None)
def lint_generated_project(session: Session):
    """Lint the generated project's Python files and configurations."""
    session.log("Installing linting dependencies for the generated project...")
    session.install("-e", ".", "--group", "dev")
    session._runner.posargs = ["nox", "-s", "pre-commit"]
    in_demo(session)
    session._runner.posargs = [""]
    session.run("retrocookie")


@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def docs(session: Session):
    """Build the template documentation website."""
    session.log("Installing documentation dependencies for the template docs...")
    session.install("-e", ".", "--group", "dev", "--group", "docs")

    session.log(f"Building template documentation with py{session.python}.")
    # Set path to allow Sphinx to import from template root if needed (e.g., __version__.py)
    # session.env["PYTHONPATH"] = str(Path(".").resolve()) # Add template root to PYTHONPATH for Sphinx

    docs_build_dir = Path("docs") / "_build" / "html"

    session.log(f"Cleaning template docs build directory: {docs_build_dir}")
    docs_build_dir.parent.mkdir(parents=True, exist_ok=True)
    session.run("sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-E")

    session.log("Building template documentation.")
    session.run("sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-W")

    session.log(f"Template documentation built in {docs_build_dir.resolve()}.")


@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def test(session: Session) -> None:
    """Run tests for the template's own functionality.

    This could involve:
    1. Rendering a project from the template into a temporary directory.
    2. Changing into the temporary directory.
    3. Running essential checks and tests *in the generated project* using uv run nox.
    """
    session.log("Running template tests...")
    session.log("Installing template testing dependencies...")
    # Sync deps from template's own pyproject.toml, e.g., 'dev' group that includes 'pytest', 'cookiecutter'
    session.install("-e", ".", "--group", "dev", "--group", "test")

    # Create a temporary directory for the generated project
    temp_dir: Path = Path(tempfile.mkdtemp())
    session.log(f"Rendering template into temporary directory: {temp_dir}")

    # Run cookiecutter to generate a project
    # Need to find cookiecutter executable - it's in the template dev env installed by uv sync.
    cookiecutter_command: list[str] = ["uv", "run", "cookiecutter", "--no-input", "--output-dir", str(temp_dir), "."]

    session.run(*cookiecutter_command, external=True)

    # Navigate into the generated project directory
    generated_project_dir = temp_dir / "test_project"  # Use the slug defined in --extra-context
    if not generated_project_dir.exists():
        session.error(f"Generated project directory not found: {generated_project_dir}")

    session.log(f"Changing to generated project directory: {generated_project_dir}")
    session.cd(generated_project_dir)

    session.log("Installing generated project dependencies using uv sync...")
    session.install("-e", ".", external=True)

    session.log("Running generated project's default checks...")
    session.run("nox")

    session.log(f"Cleaning up temporary directory: {temp_dir}")
    shutil.rmtree(temp_dir)


@nox.session(venv_backend="none")
def release_template(session: Session):
    """Run the release process for the TEMPLATE using Commitizen.

    Requires uvx in PATH (from uv install). Requires Git.
    Assumes Conventional Commits practice is followed for TEMPLATE repository.
    Optionally accepts increment level (major, minor, patch) after '--'.
    """
    session.log("Running release process for the TEMPLATE using Commitizen...")
    try:
        session.run("git", "version", success_codes=[0], external=True, silent=True)
    except CommandFailed:
        session.log("Git command not found. Commitizen requires Git.")
        session.skip("Git not available.")

    session.log("Checking Commitizen availability via uvx.")
    session.run("cz", "--version", successcodes=[0])

    increment = session.posargs[0] if session.posargs else None
    session.log(
        "Bumping template version and tagging release (increment: %s).",
        increment if increment else "default",
    )

    cz_bump_args = ["uvx", "cz", "bump", "--changelog"]

    if increment:
        cz_bump_args.append(f"--increment={increment}")

    session.log("Running cz bump with args: %s", cz_bump_args)
    # success_codes=[0, 1] -> Allows code 1 which means 'nothing to bump' if no conventional commits since last release
    session.run(*cz_bump_args, success_codes=[0, 1], external=True)

    session.log("Template version bumped and tag created locally via Commitizen/uvx.")
    session.log("IMPORTANT: Push commits and tags to remote (`git push --follow-tags`) to trigger CD for the TEMPLATE.")
