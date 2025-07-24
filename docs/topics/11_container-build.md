# 11: Application Container Building

This section evaluates the process and tools for building application container images. Containerization bundles the application code, its dependencies, and runtime configuration into a single, portable unit, simplifying deployment and ensuring consistency across environments from development to production.

## Goals Addressed

- Define and build lightweight, secure, and runnable application container images.
- Implement container build best practices (multistage builds, minimal base images, non-root users, efficient caching).
- Bundle the application code and its dependencies effectively within the image.
- Produce standard container images compatible with tools like {docker}`Docker<>`, {podman}`Podman<>`, {docker}`docker-compose<>`, and orchestration platforms (Kubernetes, ECS, etc.).
- Integrate the build process into automated workflows (Task Automation, CI/CD).

## Evaluation Criteria

- **Standardization (Format):** Does the definition use a widely accepted standard format (e.g., `Dockerfile`)?
- **Best Practice Support:** Does the format and tool explicitly support implementing containerization best practices for security, size, and efficiency (multistage builds, USER instruction, small base images, layer caching)?
- **Packaging Integration:** How well does it integrate with the project's standard Python packaging (Area 09) and dependency management (Area 02)?
- **Reproducibility:** How reproducible is the image build process given the same inputs?
- **OS Interoperability (Tool):** Does the tool used to execute the build process work reliably across major OSs (Linux, macOS, Windows)? (Note: The definition format is inherently cross-platform).
- **CLI Usability:** Is the command-line interface for triggering the build straightforward?
- **Integration:** How well does it integrate into Task Automation runners, CI/CD pipelines, and related container tools (e.g., {docker-compose}`docker-compose<>`)?
- **Maturity & Stability:** How stable and battle-tested is the tool/format?
- **Community & Documentation:** Active development, support, and comprehensive documentation.
- **Best Tool for the Job:** Considering all criteria, which tool/format provides the strongest overall fit for building standard, production-ready container images based on Python projects.

## Tools and Approaches Evaluated

### Option 1: `Dockerfile` + {docker}`Docker<>` / {podman}`Podman<>` CLI

- **Description:** Using the standard `Dockerfile` format to define image layers and steps, executed by the command-line interface of container runtimes like {docker}`Docker<>` or {podman}`Podman<>`.
- **Evaluation:**

  - **Standardization (Format):** Excellent. `Dockerfile` is the **industry standard** text-based format for defining container images, widely understood and universally compatible across container runtimes.
  - **Best Practice Support:** Excellent. The `Dockerfile` syntax explicitly supports crucial best practices like **multistage builds** (`FROM ... AS <name>`), using the `USER` instruction for non-root users, selecting minimal base images (e.g., `python:3.x-slim`, Alpine, Distroless), managing dependency caching layers effectively via step ordering, copying standard artifacts (like built wheels from Area 09) instead of source. The tool (`docker build`/`podman build`) implements these features.
  - **Packaging Integration:** Excellent. A standard `Dockerfile` workflow involves **copying the project's built wheel** (Area 09) into the image and installing it with {pip}`pip<>` or the project's chosen manager ({uv}`uv<>`). Alternatively, it can copy source/lock files and install dependencies with the manager directly _inside_ the build. This directly leverages the output of packaging and dependency management steps.
  - **Reproducibility:** High (Process). Given the same `Dockerfile`, build context files, and base image, the `docker build`/`podman build` process is highly reproducible layer-by-layer. Reliability of layer caching aids consistent builds.
  - **OS Interoperability (Tool):** Moderate (Runtime Dependency), Excellent (CLI). The `docker build` or `podman build` command-line tools are **OS-interoperable**. However, they require the {docker}`Docker<>` or {podman}`Podman<>` daemon/runtime to be installed and running on the host machine, which is an external dependency.
  - **CLI Usability:** Excellent. Simple command (`docker build . -t <image_name>`) is intuitive and standard.
  - **Integration:** Excellent. The `docker build`/`podman build` command is a standard external process easily called by Task Automation runners ({nox}`Nox<>` - Area 12) and integrated into CI/CD pipelines (Area 13, 14). Images produced are compatible with {docker-compose}`docker-compose<>` (Area 15) and production orchestrators (Area 16).
  - **Maturity & Stability:** Excellent. `Dockerfile` format and {docker}`Docker<>` are the established industry standard for containerization, extremely mature with massive adoption. {podman}`Podman<>` is a mature, highly compatible alternative.
  - **Community & Documentation:** Excellent. Vast community, extensive documentation for `Dockerfile` best practices and the tools.

- **Conclusion:** The standard, robust, and flexible approach for building container images, providing full support for essential best practices and widely compatible output. Requires an external runtime.

### Option 2: Building Directly with Build Backends (Less Common)

- **Description:** Some build backends or tools might offer experimental capabilities to output container images directly (e.g., buildctl backend). This is not a common pattern for application images derived from Python projects compared to standard Dockerfiles.
- **Evaluation:** This is not a widely adopted or standardized approach within the Python ecosystem compared to defining image contents via a `Dockerfile`. Best practices for security (USER, minimal bases) and layers are often less explicit or configurable. Less compatible with the standard tooling surrounding Dockerfiles.

- **Conclusion:** Not suitable as the primary recommended approach due to lack of standardization and broad tool support compared to `Dockerfile` + `docker build`.

## Chosen Approach

- Container Definition Format: **`Dockerfile`** (written following best practices).
- Build Execution Tool: **{docker}`Docker<>`** or **{podman}`Podman<>`** CLI.
- Dependency Installation inside Dockerfile: **{uv}`uv<>`** (`RUN uv sync` or `RUN uv add` depending on stage/pattern).

## Justification for the Choice

Using a standard **`Dockerfile`** executed by the **{docker}`Docker<>`** or **{podman}`Podman<>`** command-line interface is the clear and only technically sound choice for building application container images in this template:

1.  **Industry Standard:** The `Dockerfile` format is the **universally recognized standard**. This makes the resulting image definition highly portable and understandable to any developer familiar with containers, regardless of their host OS or chosen runtime (addressing **Standardization**).
2.  **Essential Best Practices:** The `Dockerfile` syntax inherently supports implementing crucial container build **best practices** for size, security, and efficiency (like multistage builds for minimal final images, defining non-root users, careful layer caching). This directly aligns with the template's focus on robust and maintainable foundations ("Thought out is better than preferred").
3.  **Integration with Python Tooling:** A recommended practice within the `Dockerfile` is to **copy the project's dependencies list or built package** and install them using the project's chosen dependency manager. Using **{uv}`uv<>`** (`RUN uv sync --resolve-only -f requirements.txt` to capture resolved deps, then `RUN uv sync` to install) inside the Dockerfile build process is the most efficient and standard way to handle dependency installation during the image build, leveraging {uv}`uv<>`'s speed (addressing **Packaging Integration**).
4.  **Automated Workflow:** The `docker build` or `podman build` command is a simple **CLI command** easily orchestrated by the Task Automation layer ({nox}`Nox<>` - Area 12) and integrated into CI/CD pipelines (Area 13, 14). The definition format is OS-agnostic even if the build execution tool has an OS dependency.

While requiring an external runtime (Docker/Podman) is a dependency, it is the fundamental requirement for working with containers, and the tools themselves are highly OS-interoperable.

By choosing this approach, the template provides a standard, flexible, robust, and efficient way to containerize the application, ready for deployment.

## Interactions with Other Topics

- **Packaging Build (09):** The output of the build process (built wheel file in `dist/`) is often copied _into_ the Docker image in a later stage of a multistage build.
- **Dependency Management (02):** {uv}`uv<>` is the recommended tool for managing and installing dependencies _inside_ the Docker image.
- **Task Automation (12):** {nox}`Nox<>` sessions call the `docker build` or `podman build` command via `uv run` (or `session.run` directly for the `docker`/`podman` command itself, as it's external) to build the image.
- **CI Orchestration (13) & CD Orchestration (14):** Container image builds are often triggered in CI/CD pipelines via Task Automation. CD pipelines handle pushing the built images to container registries.
- **Container Orchestration (Local) (15):** The image built in this area is the base for defining multi-container setups locally using {docker-compose}`docker-compose<>`.
- **Deployment to Production Orchestrators (16):** The image built here is the primary artifact deployed to production environments managed by tools like Kubernetes/{helm}`Helm<>`/{argocd}`Argo CD<>`.
- **Dev Containers (17):** The Dev Container often uses a similar or shared base image (or even the same `Dockerfile`) as the production image, leveraging common layers and consistency.
