# 15: Container Orchestration (Local / Single Host)

This section evaluates tools used to define and run multi-container applications. While Topic 11 covers building individual application container images, many applications consist of multiple interconnected services (e.g., a web API, a database, a message queue). This topic focuses on orchestrating these containers, particularly for development, testing, or simple single-host deployments.

## Goals Addressed

- Define multi-container application architectures (services, networks, volumes).
- Build, manage the lifecycle (start, stop, restart), and scale (to a limited extent on a single host) interconnected services based on container images.
- Facilitate local development and testing of multi-service applications.
- Provide a configuration format that is understandable and maintainable.
- Support referencing and building container images (potentially using Dockerfiles from Topic 11).
- Ensure the orchestration tools work reliably across development operating systems.

## Evaluation Criteria

- **Definition Format:** Is the format for describing the multi-container application clear, standard, and easy to read/write?
- **Service Orchestration:** Ability to define multiple interconnected services, networks, and volumes. Control service dependencies and startup order.
- **Image Management:** Ability to reference pre-built images from registries or build images locally using a `Dockerfile`.
- **Ease of Use (Development Workflow):** How easy is it to start, stop, restart, and manage the logs of the defined services for development and testing?
- **OS Interoperability:** Does the tool work reliably across Linux, macOS, and Windows development environments?
- **Integration:** How well does it integrate with individual container building (Topic 11) and the local development workflow?
- **Maturity & Stability:** How stable and battle-tested is the tool?
- **Community & Documentation:** Active development, support, and comprehensive documentation.
- **Best Tool for the Job:** Considering all criteria, which tool is the strongest fit for defining and orchestrating multi-container applications primarily in a local development context.

## Tools and Approaches Evaluated

### Option 1: {docker-compose}`Docker Compose<>`

- **Description:** A widely used tool for defining and running multi-container Docker applications. Configuration is done via a `compose.yaml` (or `docker-compose.yml`) file using YAML.
- **Evaluation:**

  - **Definition Format:** Excellent. Uses a standard, widely understood YAML format (`compose.yaml`/`docker-compose.yml`) that is clear and easy to write, describing services, networks, and volumes.
  - **Service Orchestration:** Excellent. Core purpose is to define and orchestrate multiple interconnected services, setting up internal networks, defining volumes for data persistence, and managing dependencies/startup order. Provides commands (`up`, `down`, `start`, `stop`, `restart`, `logs`, `exec`).
  - **Image Management:** Excellent. Can reference pre-built images from registries (`image: ...`) or build images locally based on a `Dockerfile` (`build: .` pointing to a directory containing a Dockerfile) – directly integrating with Topic 11's output.
  - **Ease of Use (Development Workflow):** Excellent. Designed for developer productivity. Simple commands (`docker compose up`) start the entire defined application stack. Easy to stop the stack or view combined logs.
  - **OS Interoperability:** Excellent. The {docker-compose}`Docker Compose<>` CLI tool itself works reliably across Linux, macOS, and Windows. It interacts with the local {docker}`Docker<>` or {podman}`Podman<>` runtime, which are also cross-platform.
  - **Integration:** Excellent. Integrates directly with `Dockerfile`s (Topic 11). Commands are easily run from the terminal, within Dev Containers (Topic 17), or via Task Automation ({nox}`Nox<>`) if needed to control the multi-container setup. Can define health checks and dependencies for orchestration.
  - **Maturity & Stability:** Very High. A mature, stable, widely used standard for local/single-host container orchestration. Recently transitioned from `docker-compose` (Python CLI) to `docker compose` (built into Docker CLI, Go implementation), but the configuration file format remains compatible.
  - **Community & Documentation:** Very High. Large, active community, extensive documentation.

- **Conclusion:** The standard and most suitable tool for defining and managing multi-container applications in local development or single-host contexts, aligning well with standard Dockerfile workflows and OS interoperability needs.

### Option 2: Orchestrator Tools (e.g., Raw Kubernetes Manifests, {helm}`Helm<>` - Kubernetes package manager, {argocd}`Argo CD<>` - Kubernetes CD)

- **Description:** Tools used for orchestrating containers in production environments, primarily Kubernetes. (More aligned with Topic 16).
- **Evaluation:** These tools (Kubernetes, Helm, Argo CD, etc.) are designed for complex, distributed, production-grade orchestration, not the streamlined local multi-container development experience. Their configuration is typically more complex and their local developer workflows are often less seamless for simple start/stop/log tasks compared to {docker-compose}`Docker Compose<>`. They are designed to consume images, not necessarily simplify the local build-and-run loop for multiple dependent services in development.
- **Conclusion:** While crucial for production (Topic 16), they are not the appropriate tools for the local/single-host multi-container development workflow task defined in this area.

## Chosen Tool(s)

- Multi-container definition and orchestration: **{docker-compose}`Docker Compose<>`** (using `compose.yaml` or `docker-compose.yml`).

## Justification for the Choice

**{docker-compose}`Docker Compose<>`** is the definitive choice for defining and orchestrating multi-container applications in the context of this template's primary focus areas (local development, testing, simple single-host deployment) because it directly meets the needs of this specific layer:

1.  **Standard for Local Orchestration:** {docker-compose}`Docker Compose<>` is the **widely accepted standard tool** for defining multi-service Docker applications using a simple, **standard YAML format** (`compose.yaml`/`docker-compose.yml`). This makes the configuration **understandable and maintainable**.
2.  **Excellent Local Development DX:** It provides **easy-to-use command-line interface** for controlling the entire application stack locally (`docker compose up`, `docker compose down`, `logs`, etc.). This directly supports the goal of facilitating local development workflows for multi-service applications (addressing **Ease of Use**).
3.  **Seamless Dockerfile Integration:** It natively supports referencing pre-built images and, crucially, **building images directly from a `Dockerfile`** within the compose configuration. This creates a direct link to the container image building process defined in Topic 11.
4.  **Robust and Cross-Platform:** The tool is **highly OS-interoperable**, running reliably on Linux, macOS, and Windows, requiring only the underlying Docker or Podman runtime to be present (addressing **OS Interoperability**).

Other tools (like raw Kubernetes manifests or Helm) are designed for more complex production orchestration environments (Topic 16) and are not suitable replacements for the streamlined local multi-container development workflow that {docker-compose}`Docker Compose<>` provides.

By choosing {docker-compose}`Docker Compose<>`, the template provides a standard, straightforward way for developers to work with multi-service application architectures during development and testing, built upon the individual container images produced using the guidelines from Topic 11.

## Interactions with Other Topics

- **Application Container Building (11):** {docker-compose}`Docker Compose<>` references the container images built in Area 11, often via a `build: .` directive pointing to the project's `Dockerfile` or via an `image:` reference to a registry.
- **Dev Containers (17):** Dev Containers might potentially use {docker-compose}`Docker Compose<>` as their backing "dev container" when setting up a development environment that itself consists of multiple containers.
- **Deployment to Production Orchestrators (16):** While different tools are used, the _concepts_ defined in `compose.yaml` (services, networks, volumes) have analogies in production orchestrators. Users might transition from a local compose setup to production manifests.
