# noxfile.py
# See https://nox.thea.codes/en/stable/config.html

from pathlib import Path # Use pathlib for path manipulation
from typing import Any # Import Any for type hints
from typing import List # Import List for type hints
from typing import Optional # Import Optional for type hints

import nox
from nox.sessions import Session # Import Session type for hinting

nox.options.default_venv_backend = "uv"
nox.options.sessions = ["default"]

# Logic that helps avoid metaprogramming in cookiecutter-robust-python
MIN_PYTHON_VERSION_SLUG: int = int({{ cookiecutter.min_python_version }} * 100)
MAX_PYTHON_VERSION_SLUG: int = int({{ cookiecutter.max_python_version }} * 100)

# Python versions to test against. As of April 2025, generally 3.9-3.13 are actively supported.
# See: https://devguide.python.org/versions/ and https://endoflife.date/python
PYTHON_VERSIONS: List[str] = [
    str(VERSION_SLUG / 100) for VERSION_SLUG in range(MIN_PYTHON_VERSION_SLUG, MAX_PYTHON_VERSION_SLUG + 1)
]
DEFAULT_PYTHON_VERSION: str = PYTHON_VERSIONS[-1]

REPO_ROOT: Path = Path(__file__).parent
CRATES_FOLDER: Path = REPO_ROOT / "rust"
PACKAGE_NAME: str = "{{ cookiecutter.package_name }}"


# --- GRANULAR TASK AUTOMATION SESSIONS ---
# These sessions perform specific types of checks or builds.
# Their names align with modular CI workflow files.

@nox.session(python=DEFAULT_PYTHON_VERSION)
def format_python(session: Session) -> None:
    """Run Python code formatter (Ruff format)."""
    session.log("Installing formatting dependencies...")
    session.run("uv", "sync", "--locked", "--clean", "--groups", "dev", "lint", external=True)

    session.log(f"Running Ruff formatter check with py{session.python}.")
    # Use --check, not fix. Fixing is done by pre-commit or manual run.
    session.run("uv", "run", "ruff", "format", *session.posargs, external=True)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_python(session: Session) -> None:
    """Run Python code linters (Ruff check, Pydocstyle rules)."""
    session.log("Installing linting dependencies...")
    session.run("uv", "sync", "--locked", "--clean", "--groups", "dev", "lint", external=True)

    session.log(f"Running Ruff check with py{session.python}.")
    session.run("uv", "run", "ruff", "check", "--verbose", external=True)


@nox.session(python=PYTHON_VERSIONS)
def typecheck_python(session: Session) -> None:
    """Run static type checking (Pyright) on Python code."""
    session.log("Installing type checking dependencies...")
    session.run("uv", "sync", "--locked", "--clean", "--groups", "dev", "typecheck", external=True)

    session.log(f"Running Pyright check with py{session.python}.")
    session.run("uv", "run", "pyright", external=True)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def security_python(session: Session) -> None:
    """Run code security checks (Bandit) on Python code."""
    session.log("Installing security dependencies...")
    session.run("uv", "sync", "--locked", "--clean", "--groups", "dev", "security", external=True)

    session.log(f"Running Bandit static security analysis with py{session.python}.")
    session.run("uv", "run", "bandit", "-r", PACKAGE_NAME, "-c", ".bandit", "-ll", "-s", external=True)

    session.log(f"Running pip-audit dependency security check with py{session.python}.")
    session.run("uv", "run", "pip-audit", "--python", str(Path(session.python)), external=True)


@nox.session(python=PYTHON_VERSIONS)
def test_python(session: Session) -> None:
    """Run the Python test suite (pytest with coverage)."""
    session.log("Installing test dependencies...")
    session.run("uv", "sync", "--locked", "--clean", "--groups", "dev", "test", external=True)

    session.log(f"Running test suite with py{session.python}.")
    test_results_dir = Path("test-results")
    test_results_dir.mkdir(parents=True, exist_ok=True)
    junitxml_file = test_results_dir / f"test-results-py{session.python}.xml"

    session.run(
        "uv", "run", "pytest",
        "--cov={}".format(PACKAGE_NAME),
        "--cov-report=xml",
        f"--junitxml={junitxml_file}",
        "tests/",
        external=True
    )


@nox.session(venv=None)
def test_rust(session: Session) -> None:
    """Test the project's rust crates."""
    crates: list[Path] = [cargo_toml.parent for cargo_toml in CRATES_FOLDER.glob("*/Cargo.toml")]
    crate_kwargs: list[str] = [f"-p {crate.name}" for crate in crates]
    session.run("cargo", "test", "--all-features", "--no-run", *crate_kwargs, external=True)
    session.run("cargo", "test", "--all-features", *crate_kwargs, external=True)


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs_build(session: Session) -> None:
    """Build the project documentation (Sphinx)."""
    session.log("Installing documentation dependencies...")
    session.run("uv", "sync", "--locked", "--clean", "--groups", "dev", "docs", external=True)

    session.log(f"Building documentation with py{session.python}.")
    docs_build_dir = Path("docs") / "_build" / "html"

    session.log(f"Cleaning build directory: {docs_build_dir}")
    session.run("uv", "run", "sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-E", external=True)

    session.log("Building documentation.")
    session.run("uv", "run", "sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-W", external=True)


# Note: Sessions for building Rust (build_rust) and possibly publishing Rust artifacts
# would be added here, potentially conditionally based on the 'add_rust_extension' prompt.
# Example conditional session inclusion based on cookiecutter variable:
{% if cookiecutter.add_rust_extension == 'y' %}
@nox.session(python=DEFAULT_PYTHON_VERSION)
def build_rust(session: Session) -> None:
    """Build the Rust crate.

    Requires Rust toolchain (managed separately or via CI setup).
    Requires uvx in PATH. Requires Cargo.toml in the rust/ directory.
    """
    session.log("Checking Rust toolchain availability via uvx/cargo.")
    # uvx can run cargo if rustup is on the PATH or configured.
    # or the CI setup ensures rust toolchain is installed (e.g., via actions-rs/toolchain).
    try:
        session.run("cargo", "--version", success_codes=[0], external=True, silent=True)
    except nox.command.CommandFailed:
         session.log("Rust toolchain (cargo) not found in PATH.")
         session.skip("Rust toolchain not available.")
         return

    # Change to the directory containing Cargo.toml
    rust_crate_dir = Path("rust") # Assumes rust/ directory contains Cargo.toml
    if not (rust_crate_dir / "Cargo.toml").exists():
        session.log(f"Cargo.toml not found in {rust_crate_dir}.")
        session.skip("Rust crate not found.")
        return

    session.log(f"Building Rust crate in {rust_crate_dir}.")
    # Use cargo build command, typically run from the crate root directory
    session.run("cargo", "build", "--release", external=True, cwd=str(rust_crate_dir)) # cwd ensures command runs in Rust dir
    session.log("Rust crate built.")

# Note: publish_rust session might go here for publishing Rust crates (e.g. to crates.io)
{% endif %} # End of conditional Rust build session

@nox.session(python=DEFAULT_PYTHON_VERSION)
def build_python(session: Session) -> None:
    """Build sdist and wheel packages (uv build)."""
    session.log("Installing build dependencies...")
    # Sync core & dev deps are needed for accessing project source code.
    session.run("uv", "sync", "--locked", "--clean", "--groups", "dev", external=True)

    session.log(f"Building sdist and wheel packages with py{session.python}.")
    session.run("uv", "build", "--sdist", "--wheel", "--outdir", "dist/", external=True)

    session.log("Built packages in ./dist directory:")
    session.run("uv", "run", "ls", "-l", "dist/", external=True)


@nox.session(python=DEFAULT_PYTHON_VERSION)
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
    except nox.command.CommandFailed:
        try:
            session.run("podman", "info", success_codes=[0], external=True, silent=True)
            container_cli = "podman"
        except nox.command.CommandFailed:
            session.log("Neither Docker nor Podman command found. Please install a container runtime.")
            session.skip("Container runtime not available.")
            return

    current_dir = Path(".")
    session.log(f"Ensuring core dependencies are synced in {current_dir.resolve()} for build context...")
    session.run("uv", "sync", "--locked", "--clean", external=True)

    session.log(f"Building Docker image using {container_cli}.")
    project_image_name = PACKAGE_NAME.replace("_", "-").lower()
    session.run(container_cli, "build", str(current_dir), "-t", f"{project_image_name}:latest", "--progress=plain", external=True)

    session.log(f"Container image {project_image_name}:latest built locally.")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def publish_python(session: Session) -> None:
    """Publish sdist and wheel packages to PyPI via uv publish.

    Requires packages to be built first (`nox -s build_python` or `nox -s build`).
    Requires TWINE_USERNAME/TWINE_PASSWORD or TWINE_API_KEY environment variables set (usually in CI).
    """
    session.log("Checking built packages with Twine.")
    session.run("uvx", "twine", "check", "dist/*", external=True)

    session.log("Publishing packages to PyPI.")
    session.run("uv", "publish", "dist/*", external=True)


# Note: publish_rust session might go here for publishing Rust crates (e.g. to crates.io)


# === RELEASING SESSIONS ===
# These sessions prepare or perform releases. Often run manually first, then potentially automated.

@nox.session(venv_backend="none")
def release(session: Session) -> None:
    """Run the release process using Commitizen.

    Requires uvx in PATH (from uv install). Requires Git. Assumes Conventional Commits.
    Optionally accepts increment (major, minor, patch) after '--'.
    """
    session.log("Running release process using Commitizen...")
    try:
        session.run("git", "version", success_codes=[0], external=True, silent=True)
    except nox.command.CommandFailed:
        session.log("Git command not found. Commitizen requires Git.")
        session.skip("Git not available.")
        return

    session.log("Checking Commitizen availability via uvx.")
    session.run("uvx", "cz", "--version", success_codes=[0], external=True)

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
    tox_ini_path = Path("tox.ini")
    if not tox_ini_path.exists():
        session.log("tox.ini file not found at %s. Tox requires this file.", str(tox_ini_path))
        session.skip("tox.ini not present.")
        return

    session.log("Checking Tox availability via uvx.")
    session.run("uvx", "tox", "--version", success_codes=[0], external=True)

    session.run("uvx", "tox", *session.posargs, external=True)


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
    session.notify("build_python") # Build Python sdist/wheel


@nox.session(python=DEFAULT_PYTHON_VERSION) # Run the orchestrator on the default Python version
def publish(session: Session) -> None:
    """Orchestrates publishing all project artifacts (Python packages, potentially Rust)."""
    session.log(f"Queueing publish sessions for py{session.python} if applicable.")
    session.notify("publish_python") # Publish Python sdist/wheel
    # Note: publish_rust session might be notified here if needed.


@nox.session(python=PYTHON_VERSIONS)
def check(session: Session) -> None:
    """Run primary quality checks (format, lint, typecheck, security)."""
    session.log(f"Queueing core check sessions for py{session.python} if applicable.")
    # Notify granular sessions. Their python version is controlled by their decorators.
    # Sessions without explicit python versions or limited run on DEFAULT_PYTHON_VERSION.
    session.notify("format_python")
    session.notify("lint_python")
    session.notify("typecheck_python")
    session.notify("security_python")
    session.notify("security_deps")


@nox.session(python=PYTHON_VERSIONS)
def full_check(session: Session) -> None:
   """Run all core quality checks and tests."""
   session.log(f"Queueing all check and test sessions for py{session.python} if applicable.")
   session.notify("check")
   session.notify("test_python")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def coverage(session: Session) -> None:
    """Collect and report coverage.

    Requires tests to have been run with --cov and --cov-report=xml across matrix
    (e.g., via `nox -s test-python`).
    """
    session.log("Collecting and reporting coverage across all test runs.")
    session.log("Note: Ensure 'nox -s test-python' was run across all desired Python versions first to generate coverage data.")

    session.log("Installing dependencies for coverage report session...")
    session.run("uv", "sync", "--locked", "--clean", "--groups", "dev", "test", external=True)

    coverage_combined_file = Path(".") / ".coverage"

    session.log("Combining coverage data.")
    try:
        session.run("uv", "run", "coverage", "combine", external=True)
        session.log(f"Combined coverage data into {coverage_combined_file.resolve()}")
    except nox.command.CommandFailed as e:
        if e.returncode == 1:
             session.log("No coverage data found to combine. Run tests first with coverage enabled.")
        else:
             session.error(f"Failed to combine coverage data: {e}")
        session.skip("Could not combine coverage data.")
        return

    session.log("Generating HTML coverage report.")
    coverage_html_dir = Path("coverage-html")
    session.run("uv", "run", "coverage", "html", "--directory", str(coverage_html_dir), external=True)

    session.log("Running terminal coverage report.")
    session.run("uv", "run", "coverage", "report", external=True)

    session.log(f"Coverage reports generated in ./{str(coverage_html_dir)} and terminal.")

