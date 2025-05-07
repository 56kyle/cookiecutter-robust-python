# noxfile.py
# Nox configuration for the cookiecutter-robust-python TEMPLATE development and maintenance.
# See https://nox.thea.codes/en/stable/config.html

from pathlib import Path
import shutil
import tempfile
import sys

import nox
from nox.sessions import Session

nox.options.default_venv_backend = "uv"

DEFAULT_TEMPLATE_PYTHON_VERSION = "3.12"

TEMPLATE_PYTHON_LOCATIONS: tuple[Path, ...] = (
    Path("noxfile.py"),
)

TEMPLATE_CONFIG_AND_DOCS: tuple[Path, ...] = (
    Path("pyproject.toml"),
    Path(".ruff.toml"),
    Path(".editorconfig"),
    Path(".gitignore"),
    Path(".pre-commit-config.yaml"),
    Path(".cz.toml"),
    Path("cookiecutter.json"),
    Path("README.md"),
    Path("LICENSE"),
    Path("CODE_OF_CONDUCT.md"),
    Path("CHANGELOG.md"),
    Path("docs/")
)


# === TEMPLATE MAINTENANCE TASKS ===
# Sessions for checking, formatting, building, and releasing the template itself.


@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def lint(session: Session):
    """Lint the template's own Python files and configurations."""
    session.log("Installing linting dependencies for the template source...")
    session.run("uv", "sync", "--locked", "--clean", "--groups", "dev", "lint", external=True)

    locations: list[str] = [str(loc) for loc in TEMPLATE_PYTHON_LOCATIONS + TEMPLATE_CONFIG_AND_DOCS]
    session.log(f"Running Ruff formatter check on template files with py{session.python}.")
    session.run("uv", "run", "ruff", "format", *locations, "--check", external=True)

    session.log(f"Running Ruff check on template files with py{session.python}.")
    session.run("uv", "run", "ruff", "check", *locations, "--verbose", external=True)


@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def docs(session: Session):
    """Build the template documentation website."""
    session.log("Installing documentation dependencies for the template docs...")
    session.run("uv", "sync", "--locked", "--clean", "--groups", "dev", "docs", external=True)

    session.log(f"Building template documentation with py{session.python}.")
    # Set path to allow Sphinx to import from template root if needed (e.g., __version__.py)
    # session.env["PYTHONPATH"] = str(Path(".").resolve()) # Add template root to PYTHONPATH for Sphinx

    docs_build_dir = Path("docs") / "_build" / "html"

    session.log(f"Cleaning template docs build directory: {docs_build_dir}")
    docs_build_dir.parent.mkdir(parents=True, exist_ok=True)
    session.run("uv", "run", "sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-E", external=True)

    session.log("Building template documentation.")
    session.run("uv", "run", "sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-W", external=True)

    session.log(f"Template documentation built in {docs_build_dir.resolve()}.")


@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def generate_project(session: Session) -> None:
    """Generate a demo project using the template."""
    session.log("Installing demo project generation dependencies...")
    session.install("cookiecutter", "typer")
    session.run("generate-demo-project", "--repo-folder=.", "--demos-cache-folder=.", "--demo-name=demo_project")



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
    session.run("uv", "sync", "--locked", "--clean", "--groups", "dev", "test", external=True)

    # Create a temporary directory for the generated project
    temp_dir: Path = Path(tempfile.mkdtemp())
    session.log(f"Rendering template into temporary directory: {temp_dir}")

    # Run cookiecutter to generate a project
    # Need to find cookiecutter executable - it's in the template dev env installed by uv sync.
    cookiecutter_command: list[str] = ["uv", "run", "cookiecutter", "--no-input", "--output-dir", str(temp_dir), "."]
    # Add cookiecutter variables to customize the generated project for testing, using --extra-context
    cookiecutter_command.extend([
        "--extra-context",
        "project_name='Test Project'",
        "project_slug='test_project'",
        "package_name='test_package'",
        "author_name='Test Author'",
        "author_email='test@example.com'",
        "license='MIT'",
        "python_version='3.12'", # Use a fixed version for test stability
        "add_rust_extension='n'", # Test without Rust initially, add another test session for Rust
        # Add other variables needed by cookiecutter.json here to ensure no prompts
    ])

    session.run(*cookiecutter_command, external=True)

    # Navigate into the generated project directory
    generated_project_dir = temp_dir / "test_project" # Use the slug defined in --extra-context
    if not generated_project_dir.exists():
        session.error(f"Generated project directory not found: {generated_project_dir}")
        return

    session.log(f"Changing to generated project directory: {generated_project_dir}")
    session.cd(generated_project_dir)

    session.log("Installing generated project dependencies using uv sync...")
    session.run("uv", "sync", "--locked", external=True)

    session.log("Running generated project's default checks...")
    session.run("uv", "run", "nox", external=True)

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
    except nox.command.CommandFailed:
        session.log("Git command not found. Commitizen requires Git.")
        session.skip("Git not available.")
        return

    session.log("Checking Commitizen availability via uvx.")
    session.run("uvx", "cz", "--version", successcodes=[0], external=True)

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

