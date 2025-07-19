# 09: Distribution Package Building (sdist/wheel)

This section evaluates the tools and approaches for creating standard Python distribution packages. This process transforms your source code and metadata into artifacts (`sdist` and `.whl` files) that can be easily installed and shared within the Python ecosystem.

## Goals Addressed

- Create standard, PEP-compliant Python source distributions (`.tar.gz`) and built distributions (wheels - `.whl`).
- Ensure packages include all necessary metadata, source files, assets, and entry points according to standards.
- Support building packages with native code extensions (like Rust) in an OS-interoperable manner.
- Provide a reproducible build process.
- Integrate seamlessly into automated workflows (Task Automation, CI/CD).
- Produce artifacts ready for publishing to PyPI or other package indexes (Area 10).

## Evaluation Criteria

- **PEP Compliance (Build System & Metadata):** Strict adherence to PEP 517 (build frontends/backends) and PEP 621 (metadata in pyproject.toml). Adherence to PEP 427 (Wheel specification).
- **Standard Artifacts:** Does it produce standard `.sdist` and `.whl` files consumable by tools like :pip-documentation:`pip` and :twine-documentation:`twine`?
- **OS Interoperability (Build Process):** Does the tool and its backend enable building packages reliably across Linux, macOS, and Windows, particularly for projects with native extensions?
- **Support for Native Extensions:** How well does it support including and compiling code written in other languages (e.g., Rust, C, C++) into the built wheel?
- **Reproducible Builds:** Does the build process ensure the same inputs reliably produce the same outputs (within acceptable build system variations)? Relies on PEP 518 (build requires isolation).
- **Ease of Configuration:** How simple is it to configure the build process, especially defining metadata and including non-Python files?
- **Performance:** Speed of the build process.
- **Integration:** How well does it integrate with dependency managers, Task Automation runners, and CI/CD pipelines?

## Tools and Approaches Evaluated

Python packaging involves a **Frontend** (what the user calls to start the build) and a **Backend** (the tool configured in `pyproject.toml` that implements the PEP 517 build logic). We evaluate options for both roles.

### Frontend Option: :build-documentation:`build`

- **Description:** The recommended standard frontend from PyPA for building packages. You run `python -m build` in your project directory. It reads `pyproject.toml`, determines the backend(s), installs build dependencies in isolated environments, and invokes the backend's PEP 517 hooks (`build_wheel`, `build_sdist`).
- **Evaluation:**

  - **PEP Compliance:** Excellent. Directly implements the PEP 517 frontend specification. Requires backends to be PEP 517 compliant.
  - **Standard Artifacts:** Excellent. Designed to orchestrate backends that produce standard artifacts.
  - **OS Interoperability:** Excellent. Pure Python, cross-platform tool that correctly sets up build environments across OSs using standard Python tools.
  - **Support for Native Extensions:** N/A (Frontend). Delegates compilation to the backend.
  - **Reproducible Builds:** High (Isolation). Enforces isolation for build dependencies (PEP 518), contributing significantly to reproducibility. Ultimate reproducibility depends on the backend and pinning build requirements.
  - **Ease of Configuration:** Excellent. Simple command (`python -m build`). Configuration _of the build itself_ depends on the backend's config in `pyproject.toml`.
  - **Performance:** High (Orchestration). Adds minimal overhead; performance depends on the invoked backend.
  - **Integration:** Excellent. Simple CLI easily callable from Task Automation (:nox-documentation:`Nox`) and CI. Works with any PEP 517 backend.
  - **Maturity & Stability:** High. PyPA recommended, stable, gaining widespread adoption.
  - **Community & Documentation:** High.

- **Conclusion:** The ideal, standard frontend for building. It should be the tool invoked by the Task Automation layer.

### Frontend Option: Dependency Managers (e.g., :uv-documentation:`uv` build, :pdm-documentation:`PDM` build, :poetry-documentation:`Poetry` build, :hatch-documentation:`Hatch` build)

- **Description:** Modern dependency managers often provide their own `build` command that acts as a PEP 517 frontend, wrapping calls to the specified backend using their internal environment management.
- **Evaluation:**
  - **PEP Compliance:** Excellent. Act as valid PEP 517 frontends.
  - **Standard Artifacts:** Excellent.
  - **OS Interoperability:** Excellent. Tools are cross-platform and manage environments correctly.
  - **Support for Native Extensions:** N/A (Frontend). Delegates to backend.
  - **Reproducible Builds:** High (Isolation). Enforce build requires isolation. Reproducibility depends on backend.
  - **Ease of Configuration:** Excellent. A single command within the manager's CLI (e.g., `uv build`). Configuration of the build itself still depends on the backend.
  - **Performance:** Varies. Performance is usually tied to their core manager's implementation, can be fast (e.g., `uv build`).
  - **Integration:** Excellent. Integrates within their manager's ecosystem. Callable from Task Automation. Can be simpler than `python -m build` if using that manager's environment setup.
  - **Maturity & Stability:** Varies (depends on manager maturity). High for PDM/Poetry/Hatch, Moderate for uv (but rapidly stabilizing build command).
- **Conclusion:** Using the `build` command from your chosen dependency manager can provide a slightly more integrated experience within that manager's ecosystem. It fulfills the frontend role equivalently to `python -m build` but requires the manager itself to be installed. For this template, as :uv-documentation:`uv` is the chosen manager and has a native `uv build` command, using this simplifies the dependency stack slightly over needing the separate `build` tool.

### Backend Option 1: :setuptools-documentation:`setuptools`

- **Description:** The most common and historically widely used PEP 517 build backend. Configured using the standard `[project]` metadata (PEP 621) and `[build-system]` entrypoint. Written in Python. Supports building C extensions.
- **Evaluation:**

  - **PEP Compliance:** High. Largely adheres to PEP 517/621 when used with `pyproject.toml`. PEP 660 (editable installs) compliant.
  - **Standard Artifacts:** Excellent. Produces universally compatible sdist and wheel files.
  - **OS Interoperability (Build):** Moderate to High. Builds Python parts reliably. **Native compilation with C/C++ extensions is OS-dependent**, requiring platform-specific compilers (MSVC, GCC/Clang). Setting up complex cross-platform builds for universal wheels (manylinux, Windows, macOS) can be challenging and often requires external CI infrastructure complexities.
  - **Support for Native Extensions:** Yes, standard support for C/C++ via `Extension` objects in `setup.py` or `pyproject.toml` configuration, invoked by the backend.
  - **Reproducible Builds:** High. Works with frontend isolation. Reproducibility of native parts relies on compiler and environmental consistency.
  - **Ease of Configuration:** High. Configuring using PEP 621 `[project]` is straightforward. Configuring native extensions cross-platform can become complex.
  - **Performance:** High. Python execution, generally efficient for standard builds.
  - **Maturity & Stability:** Very High. Extremely mature, widely used, stable.
  - **Community & Documentation:** Very High. Vast resources and community knowledge.

- **Conclusion:** The standard, robust backend for most pure Python or simple native extension projects. Relies on external compiler toolchains which makes _cross-platform_ native building the main complexity.

### Backend Option 2: :flit-documentation:`flit`

- **Description:** A simpler PEP 517 build backend focused exclusively on **pure Python** packages. Reads metadata solely from the standard `[project]` table (PEP 621). Written in Python. Does NOT support native extensions.
- **Evaluation:**

  - **PEP Compliance:** Very High. Designed specifically around PEP 621 for simplicity.
  - **Standard Artifacts:** Excellent. Produces standard sdist/wheel for pure Python.
  - **OS Interoperability (Build):** Excellent. Pure Python, build process is inherently cross-platform.
  - **Support for Native Extensions:** Poor (None). Explicitly not supported. Makes it unsuitable for projects requiring any compilation.
  - **Reproducible Builds:** Very High. Simplicity reduces external factors impacting reproducibility.
  - **Ease of Configuration:** Excellent. Very simple using only `[project]` in `pyproject.toml`.
  - **Performance:** High. Optimized for pure Python, can be slightly faster than setuptools for simple cases.
  - **Maturity & Stability:** High. Mature, stable, reliable for its specific pure-Python niche.
  - **Community & Documentation:** High.

- **Conclusion:** Excellent for its pure-Python niche, offering maximum simplicity. Unsuitable for a template that includes the option for native extensions.

### Backend Option 3: Modern Manager Backends (e.g., :pdm-documentation:`pdm-backend`, :hatch-documentation:`hatchling`, :poetry-documentation:`poetry-core`)

- **Description:** The PEP 517 backends bundled with or part of the modern project managers (PDM, Hatch, Poetry). Read metadata and configuration from their respective sections (mostly in `pyproject.toml`).
- **Evaluation:**

  - **PEP Compliance:** Varies (Metadata). :pdm-documentation:`pdm-backend` and :hatch-documentation:`hatchling` adhere strongly to PEP 621. :poetry-documentation:`poetry-core` uses its custom format for primary metadata (PEP 621 not for deps). All implement PEP 517 hooks.
  - **Standard Artifacts:** Excellent.
  - **OS Interoperability (Build):** Moderate to High. Like setuptools, native compilation relies on external toolchains, but backends like :hatch-documentation:`hatchling` offer configurable hooks to assist with complex builds.
  - **Support for Native Extensions:** Varies. :hatch-documentation:`hatchling` has robust hooks, :pdm-documentation:`pdm-backend` good via scripts, :poetry-documentation:`poetry-core` less focused here.
  - **Reproducible Builds:** High. Works with frontend isolation. Reproducibility depends on backend implementation and external toolchains for native.
  - **Ease of Configuration:** Varies (depends on backend's config format and build hook complexity).
  - **Performance:** High. Python execution, depends on backend implementation.
  - **Maturity & Stability:** High. Part of mature manager projects.
  - **Community & Documentation:** High.

- **Conclusion:** Provides tight integration if using their manager as primary tool. :hatchling-documentation:`hatchling` is notable for build hooks. Still rely on external compilers for native.

### Backend Option 4: :maturin-documentation:`Maturin`

- **Description:** A PEP 517 build backend specialized for building Python packages with **Rust** extensions. Designed to simplify complex, cross-platform native compilation into wheels (`manylinux`, Windows, macOS) by managing toolchains (like Zig) for the user. Reads metadata from `pyproject.toml` (PEP 621) and uses `[tool.maturin]`. Written in Rust/Python.
- **Evaluation:**

  - **PEP Compliance:** Very High. Primarily designed around PEP 517/621. Produces PEP 427 wheels.
  - **Standard Artifacts:** Excellent. Produces standard, correct, **platform-specific** sdist and wheel files crucial for distributing native extensions.
  - **OS Interoperability (Build):** Excellent. **Core Strength.** Its entire design focuses on enabling **robust cross-platform native compilation into wheels**, often simplifying it dramatically compared to Python-based backends by handling toolchain provisioning.
  - **Support for Native Extensions:** Excellent (for Rust). It is the de-facto standard for PyO3/Rust + Python projects.
  - **Reproducible Builds:** Very High. Robust management of native toolchains contributes significantly to reproducible native builds.
  - **Ease of Configuration:** High. Relatively simple config in `pyproject.toml` to point to the Rust crate. Less complex than hand-rolling cross-platform C extensions with setuptools.
  - **Performance:** Excellent (Native Compilation). Native build times depend on the Rust project size, but Maturin's overhead is minimal, and it optimizes the native build orchestration.
  - **Maturity & Stability:** High. Mature, stable, actively developed standard in the Rust+Python space.
  - **Community & Documentation:** High. Dedicated community, good documentation.

- **Conclusion:** The definitive choice _specifically for projects requiring Rust extensions_. Solves the complex problem of cross-platform native builds uniquely well.

## Chosen Tool(s)

- Primary Frontend: **:uv-documentation:`uv`** (`uv build`).
- Backend for Pure Python: **:setuptools-documentation:`setuptools`** (`setuptools.build_meta`).
- Backend for Rust Extensions: **:maturin-documentation:`Maturin`** (`maturin`).

## Justification for the Choice

This template provides flexibility for generating either pure Python projects or those with Rust extensions, managed via a Cookiecutter prompt. Therefore, the build process needs to support both cases robustly:

1.  **Standard Frontend:** Using **:uv-documentation:`uv`**'s native `uv build` command as the primary frontend is the logical choice, as :uv-documentation:`uv` is already the core Dependency Manager (02) and Task Automation orchestrator (12) in this template. It is a **PEP 517 compliant frontend**, leveraging :uv-documentation:`uv`'s performance and environment management. This simplifies the required tooling compared to needing the separate `build` command globally.
2.  **Pure Python Backend:** For projects without native extensions, **:setuptools-documentation:`setuptools`** is chosen as the backend (`setuptools.build_meta`). :setuptools-documentation:`setuptools` is the **most common, mature, and widely compatible** backend in the ecosystem. Crucially, when used as a PEP 517 backend with `pyproject.toml`, it adheres to **PEP 621** for standard metadata, aligning with our non-negotiable standard format requirement. It provides excellent support for including pure Python code, data files, and defining entry points reliably across OSs. :flit-documentation:`flit` was considered for pure-Python simplicity but doesn't add significant benefit over :setuptools-documentation:`setuptools`'s standard approach with PEP 621 and lacks native extension support if that were ever added later to the project manually.
3.  **Rust Extension Backend:** For projects with Rust extensions, **:maturin-documentation:`Maturin`** is selected as the backend. :maturin-documentation:`Maturin` is the **"Best Tool for the Job"** specifically for Rust extensions, uniquely simplifying **cross-platform native compilation** and wheel building. It handles the complex process of ensuring the compiled Rust code is correctly embedded into standard, distributable Python wheels (`.whl` files compatible with PyPI and different operating systems). It also adheres to **PEP 621** metadata and **PEP 517** build processes.

The template's `pyproject.toml` will be conditionally generated based on the `add_rust_extension` prompt in `cookiecutter.json`, setting the `[build-system].build-backend` accordingly to either `setuptools.build_meta` or `maturin` and listing the required backend (`setuptools` or `maturin`) in `[build-system].requires`.

This approach ensures that the generated project uses a standard, robust, and PEP-compliant build process tailored to its specific content (pure Python vs. Rust) and easily invoked via :uv-documentation:`uv`'s build command orchestrated by :nox-documentation:`Nox`.

## Interactions with Other Topics

- **pyproject.toml (01):** Defines project metadata (`[project]`) used by the chosen backends (both read PEP 621). Crucially configures the `[build-system]` table specifying the chosen backend (`setuptools` or `maturin`) and their dependencies.
- **Dependency Management (02):** :uv-documentation:`uv` is the frontend (`uv build`). It also installs the build backend dependencies listed in `[build-system].requires`.
- **Task Automation (12):** :nox-documentation:`Nox` sessions call `uv build` to automate the build process.
- **Packaging Publish (10):** The output of the build process (files in `dist/`) are the inputs for the publishing step.
- **Container Build (11):** The application's built package (`.whl` or `.tar.gz`) is often copied and installed _inside_ the production Docker image.
- **CI Orchestration (13) & CD Orchestration (14):** CI pipelines verify the build process, and CD pipelines trigger the build (via Nox calling `uv build`) and subsequent publishing steps.
