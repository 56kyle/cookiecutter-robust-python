"""Noxfile for the {{cookiecutter.project_name}} project."""
from pathlib import Path
from typing import List

import nox
from nox.command import CommandFailed
from nox.sessions import Session


nox.options.default_venv_backend = "uv"

# Logic that helps avoid metaprogramming in cookiecutter-robust-python
MIN_PYTHON_VERSION_SLUG: int = int("{{cookiecutter.min_python_version}}".lstrip("3."))
MAX_PYTHON_VERSION_SLUG: int = int("{{cookiecutter.max_python_version}}".lstrip("3."))

PYTHON_VERSIONS: List[str] = [
    f"3.{VERSION_SLUG}" for VERSION_SLUG in range(MIN_PYTHON_VERSION_SLUG, MAX_PYTHON_VERSION_SLUG + 1)
]
DEFAULT_PYTHON_VERSION: str = PYTHON_VERSIONS[-1]

REPO_ROOT: Path = Path(__file__).parent
CRATES_FOLDER: Path = REPO_ROOT / "rust"
PACKAGE_NAME: str = "{{cookiecutter.package_name}}"


@nox.session(python=DEFAULT_PYTHON_VERSION, name="pre-commit")
def pre_commit(session: Session) -> None:
    """Run pre-commit checks."""
    session.log("Installing pre-commit dependencies...")
    session.install("-e", ".", "--group", "dev")


@nox.session(python=DEFAULT_PYTHON_VERSION, name="format-python")
def format_python(session: Session) -> None:
    """Run Python code formatter (Ruff format)."""
    session.log("Installing formatting dependencies...")
    session.install("-e", ".", "--group", "dev", "--group", "lint")

    session.log(f"Running Ruff formatter check with py{session.python}.")
    # Use --check, not fix. Fixing is done by pre-commit or manual run.
    session.run("ruff", "format", *session.posargs)


@nox.session(python=DEFAULT_PYTHON_VERSION, name="lint-python")
def lint_python(session: Session) -> None:
    """Run Python code linters (Ruff check, Pydocstyle rules)."""
    session.log("Installing linting dependencies...")
    session.install("-e", ".", "--group", "dev", "--group", "lint")

    session.log(f"Running Ruff check with py{session.python}.")
    session.run("ruff", "check", "--verbose")


@nox.session(python=PYTHON_VERSIONS)
def typecheck(session: Session) -> None:
    """Run static type checking (Pyright) on Python code."""
    session.log("Installing type checking dependencies...")
    session.install("-e", ".", "--group", "dev", "--group", "typecheck")

    session.log(f"Running Pyright check with py{session.python}.")
    session.run("pyright")


@nox.session(python=DEFAULT_PYTHON_VERSION, name="security-python")
def security_python(session: Session) -> None:
    """Run code security checks (Bandit) on Python code."""
    session.log("Installing security dependencies...")
    session.install("-e", ".", "--group", "dev", "--group", "security")

    session.log(f"Running Bandit static security analysis with py{session.python}.")
    session.run("bandit", "-r", PACKAGE_NAME, "-c", ".bandit", "-ll", "-s")

    session.log(f"Running pip-audit dependency security check with py{session.python}.")
    session.run("pip-audit", "--python", str(Path(session.python)))


@nox.session(python=PYTHON_VERSIONS, name="tests-python")
def tests_python(session: Session) -> None:
    """Run the Python test suite (pytest with coverage)."""
    session.log("Installing test dependencies...")
    session.install("-e", ".", "--group", "dev", "--group", "test")

    session.log(f"Running test suite with py{session.python}.")
    test_results_dir = Path("test-results")
    test_results_dir.mkdir(parents=True, exist_ok=True)
    junitxml_file = test_results_dir / f"test-results-py{session.python}.xml"

    session.run(
        "pytest",
        "--cov={}".format(PACKAGE_NAME),
        "--cov-report=xml",
        f"--junitxml={junitxml_file}",
        "tests/"
    )


@nox.session(python=None, name="tests-rust")
def tests_rust(session: Session) -> None:
    """Test the project's rust crates."""
    crates: list[Path] = [cargo_toml.parent for cargo_toml in CRATES_FOLDER.glob("*/Cargo.toml")]
    crate_kwargs: list[str] = [f"-p {crate.name}" for crate in crates]
    session.run("cargo", "test", "--all-features", "--no-run", *crate_kwargs, external=True)
    session.run("cargo", "test", "--all-features", *crate_kwargs, external=True)


@nox.session(python=DEFAULT_PYTHON_VERSION, name="docs-build")
def docs_build(session: Session) -> None:
    """Build the project documentation (Sphinx)."""
    session.log("Installing documentation dependencies...")
    session.install("-e", ".", "--group", "dev", "--group", "docs")

    session.log(f"Building documentation with py{session.python}.")
    docs_build_dir = Path("docs") / "_build" / "html"

    session.log(f"Cleaning build directory: {docs_build_dir}")
    session.run("sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-E")

    session.log("Building documentation.")
    session.run("sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-W")


@nox.session(python=DEFAULT_PYTHON_VERSION, name="build-python")
def build_python(session: Session) -> None:
    """Build sdist and wheel packages (uv build)."""
    session.log("Installing build dependencies...")
    # Sync core & dev deps are needed for accessing project source code.
    session.install("-e", ".", "--group", "dev")

    session.log(f"Building sdist and wheel packages with py{session.python}.")
    {% if cookiecutter.add_rust_extension == 'y' -%}
    session.run("uv", "build", "--sdist", "--wheel", "--outdir", "dist/", external=True)
    {% else -%}
    session.run("maturin", "develop", "--uv")
    {% endif -%}

    session.log("Built packages in ./dist directory:")
    for path in Path("dist/").glob("*"):
        session.log(f"- {path.name}")


@nox.session(python=DEFAULT_PYTHON_VERSION, name="build-container")
def build_container(session: Session) -> None:
    """Build the Docker container image.

    Requires Docker or Podman installed and running on the host.
    Ensures core project dependencies are synced in the current environment
    *before* the build context is prepared.
    """
    session.log("Building application container image...")
    try:
        session.run("docker", "info", success_codes=[0], external=True, silent=True)
        container_cli = "docker"
    except CommandFailed:
        try:
            session.run("podman", "info", success_codes=[0], external=True, silent=True)
            container_cli = "podman"
        except CommandFailed:
            session.log("Neither Docker nor Podman command found. Please install a container runtime.")
            session.skip("Container runtime not available.")

    current_dir: Path = Path.cwd()
    session.log(f"Ensuring core dependencies are synced in {current_dir.resolve()} for build context...")
    session.run("-e", ".")

    session.log(f"Building Docker image using {container_cli}.")
    project_image_name = PACKAGE_NAME.replace("_", "-").lower()
    session.run(container_cli, "build", str(current_dir), "-t", f"{project_image_name}:latest", "--progress=plain", external=True)

    session.log(f"Container image {project_image_name}:latest built locally.")


@nox.session(python=DEFAULT_PYTHON_VERSION, name="publish-python")
def publish_python(session: Session) -> None:
    """Publish sdist and wheel packages to PyPI via uv publish.

    Requires packages to be built first (`nox -s build-python` or `nox -s build`).
    Requires TWINE_USERNAME/TWINE_PASSWORD or TWINE_API_KEY environment variables set (usually in CI).
    """
    session.install("-e", ".", "--group", "dev")

    session.log("Checking built packages with Twine.")
    session.run("twine", "check", "dist/*")

    session.log("Publishing packages to PyPI.")
    session.run("uv", "publish", "dist/*", external=True)


@nox.session(python=None, name="publish-rust")
def publish_rust(session: Session) -> None:
    """Publish built crates to crates.io."""
    session.log("Publishing crates to crates.io")
    for cargo_toml in CRATES_FOLDER.glob("*/Cargo.toml"):
        crate_folder: Path = cargo_toml.parent
        session.run("cargo", "publish", "-p", crate_folder.name)


@nox.session(venv_backend="none")
def release(session: Session) -> None:
    """Run the release process using Commitizen.

    Requires uvx in PATH (from uv install). Requires Git. Assumes Conventional Commits.
    Optionally accepts increment (major, minor, patch) after '--'.
    """
    session.log("Running release process using Commitizen...")
    session.install("-e", ".", "--group", "dev")

    try:
        session.run("git", "version", success_codes=[0], external=True, silent=True)
    except CommandFailed:
        session.log("Git command not found. Commitizen requires Git.")
        session.skip("Git not available.")

    session.log("Checking Commitizen availability via uvx.")
    session.run("cz", "--version", success_codes=[0])

    increment = session.posargs[0] if session.posargs else None
    session.log(
        "Bumping version and tagging release (increment: %s).",
        increment if increment else "default",
    )

    cz_bump_args = ["uvx", "cz", "bump", "--changelog"]

    if increment:
         cz_bump_args.append(f"--increment={increment}")

    session.log("Running cz bump with args: %s", cz_bump_args)
    session.run(*cz_bump_args, success_codes=[0, 1], external=True)

    session.log("Version bumped and tag created locally via Commitizen/uvx.")
    session.log(
        "IMPORTANT: Push commits and tags to remote (`git push --follow-tags`) to trigger CD pipeline."
    )


# --- COMPATIBILITY SESSIONS ---
# Sessions needed for compatibility with other tools or ecosystems.

@nox.session(venv_backend="none")
def tox(session: Session) -> None:
    """Run the 'tox' test matrix.

    Requires uvx in PATH. Requires tox.ini file.
    Useful for specific ecosystem conventions (e.g., pytest plugins,
    cookiecutter-driven matrix testing).
    Accepts tox args after '--' (e.g., `nox -s tox -- -e py39`).
    """
    session.log("Running Tox test matrix via uvx...")
    session.install("-e", ".", "--group", "dev")

    tox_ini_path = Path("tox.ini")
    if not tox_ini_path.exists():
        session.log("tox.ini file not found at %s. Tox requires this file.", str(tox_ini_path))
        session.skip("tox.ini not present.")

    session.log("Checking Tox availability via uvx.")
    session.run("tox", "--version", success_codes=[0])

    session.run("tox", *session.posargs)


# --- COMBINED/ORCHESTRATION SESSIONS ---
# These sessions provide easy entry points by notifying or calling granular sessions.
# Their names often align with the intended CI workflow steps (e.g., 'build' orchestrates builds).

@nox.session(python=DEFAULT_PYTHON_VERSION) # Run the orchestrator on the default Python version
def build(session: Session) -> None:
    """Orchestrates building all project artifacts (Python packages, potentially Rust)."""
    session.log(f"Queueing build sessions for py{session.python} if applicable.")
    # Build Rust crate first if included
    {% if cookiecutter.add_rust_extension == 'y' %}
    session.notify("build_rust") # Build Rust crate first if Rust is enabled
    {% endif %}
    # Then build the Python package (uv build)
    session.notify("build-python") # Build Python sdist/wheel


@nox.session(python=DEFAULT_PYTHON_VERSION) # Run the orchestrator on the default Python version
def publish(session: Session) -> None:
    """Orchestrates publishing all project artifacts (Python packages, potentially Rust)."""
    session.log(f"Queueing publish sessions for py{session.python} if applicable.")
    session.notify("publish-python") # Publish Python sdist/wheel
    # Note: publish_rust session might be notified here if needed.


@nox.session(python=PYTHON_VERSIONS)
def check(session: Session) -> None:
    """Run primary quality checks (format, lint, typecheck, security)."""
    session.log(f"Queueing core check sessions for py{session.python} if applicable.")
    session.notify("format-python")
    session.notify("lint-python")
    session.notify("typecheck")
    session.notify("security-python")


@nox.session(python=PYTHON_VERSIONS, name="full-check")
def full_check(session: Session) -> None:
   """Run all core quality checks and tests."""
   session.log(f"Queueing all check and test sessions for py{session.python} if applicable.")
   session.notify("check")
   session.notify("tests-python")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def coverage(session: Session) -> None:
    """Collect and report coverage.

    Requires tests to have been run with --cov and --cov-report=xml across matrix
    (e.g., via `nox -s test-python`).
    """
    session.log("Collecting and reporting coverage across all test runs.")
    session.log("Note: Ensure 'nox -s test-python' was run across all desired Python versions first to generate coverage data.")

    session.log("Installing dependencies for coverage report session...")
    session.install("-e", ".", "--group", "dev", "--group", "test")

    coverage_combined_file: Path = Path.cwd() / ".coverage"

    session.log("Combining coverage data.")
    try:
        session.run("coverage", "combine")
        session.log(f"Combined coverage data into {coverage_combined_file.resolve()}")
    except CommandFailed as e:
        if e.returncode == 1:
             session.log("No coverage data found to combine. Run tests first with coverage enabled.")
        else:
             session.error(f"Failed to combine coverage data: {e}")
        session.skip("Could not combine coverage data.")

    session.log("Generating HTML coverage report.")
    coverage_html_dir = Path("coverage-html")
    session.run("coverage", "html", "--directory", str(coverage_html_dir))

    session.log("Running terminal coverage report.")
    session.run("coverage", "report")

    session.log(f"Coverage reports generated in ./{coverage_html_dir} and terminal.")
