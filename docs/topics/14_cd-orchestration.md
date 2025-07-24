# 14: Continuous Deployment / Delivery (CD) Orchestration

This section discusses the tools and configurations used to set up Continuous Deployment (CD) or Continuous Delivery (CD) pipelines. CD automates the process of taking integrated code that has passed CI, preparing release artifacts (packages, containers), and publishing or deploying them. This layer focuses on _orchestrating_ the build and publish tasks defined elsewhere and managing secrets, rather than executing the build/publish logic itself.

## Goals Addressed

- Automate the preparation of release artifacts (Python packages, container images).
- Automate publishing these artifacts to package indexes (PyPI, etc.) or container registries.
- Trigger deployment/publishing workflows based on appropriate events (e.g., successful CI on main, creation of a Git tag).
- Manage sensitive credentials securely for publishing or deployment steps.
- Orchestrate build and publish/deployment tasks defined in the Task Automation layer (Topic 12).

## Core Orchestration Strategy: Leveraging Task Automation

As with CI (Topic 13), a core principle is **CI/CD agnosticism**. The detailed logic for _how_ to build packages, containers, and publish them resides within the project's **Task Automation layer (Topic 12 - `Nox`{nox})**. The CD configuration acts as a **thin orchestration layer** for these release-focused tasks.

This strategy means the CD configuration primarily:

1.  Checks out the code (often triggered by a specific event like a tag or successful CI run).
2.  Sets up a compatible environment (Python, Task Automation tools like `Nox`{nox}, and `uv`{uv} as its backend).
3.  Securely injects necessary credentials (e.g., PyPI API token, container registry credentials).
4.  Calls the relevant Task Automation commands (e.g., `nox -s build:package`, `nox -s publish`) to perform the release steps.

## Evaluation Criteria (for CD Orchestration Tools/Configurations)

We evaluate the types of tools and configurations used at this orchestration layer based on how well they support the goals and strategy:

- **Event Triggering:** Capability to trigger workflows based on specific VCS events (tags, branches), manual triggers, or successful completion of other workflows (like CI).
- **Environment Setup Features:** Does the platform/tool provide robust ways to obtain source code, set up required runtime environments (Python), and install necessary orchestration tools (`Nox`{nox}, `uv`{uv})?
- **Secure Credential Management:** Ability to store and inject sensitive information (API keys, passwords) securely into job environments without exposing them in logs or configuration.
- **Orchestration Capability:** Ability to define a sequence of steps (jobs, stages) and execute external commands (calling `nox -s ...`).
- **Reporting:** How well does it report the success/failure status of the CD process?
- **Adaptability:** How easy is it to define comparable workflows across different platforms using this approach?
- **Maturity & Stability:** How stable is the platform/configuration method?
- **Community & Documentation:** Active development, support, and comprehensive documentation for implementing CD workflows.
- **Best Fit for Strategy:** How well does it enable the strategy of calling Task Automation layers?

## Tools and Configurations Evaluated

At the CD orchestration layer, the "tool" is primarily the **configuration format provided by the CI/CD platform itself**. While there might be workflow engines or deployment-specific tools _invoked by_ the CD orchestration (like tools from Topic 16), the core task here is _defining the CD pipeline steps_ using the platform's capabilities.

### Approach: Platform-Specific CI/CD Workflow Configurations

- **Configuration Method:** Configuration files provided by the CI/CD platform (e.g., YAML for `GitHub Actions`{github-actions}, `GitLab CI`{gitlab-ci}, `Bitbucket Pipelines`{bitbucket-pipelines}, etc.). These files define jobs, steps, environments, triggers, and secrets.
- **Evaluation:**

  - **Event Triggering:** Excellent. All major platforms provide rich and flexible ways to trigger workflows based on VCS events (push to tag, merge to main branch, etc.) or workflow dependencies.
  - **Environment Setup Features:** Excellent. Platforms provide robust features for checking out code, setting up specific Python versions (via built-in steps/actions), and caching dependencies required for running the Task Automation tools (`Nox`{nox}, `uv`{uv}) in the CD job.
  - **Secure Credential Management:** Excellent. This is a core function of modern CI/CD platforms. They provide secure methods (UI secrets, encrypted variables) to store and inject credentials into job environments using environment variables (like `TWINE_API_KEY`, `DOCKER_HUB_PASSWORD`), making them available for Task Automation commands to use securely.
  - **Orchestration Capability:** Excellent. Platforms are designed to define job sequences (stages), dependencies between jobs, and execute steps which involve running arbitrary command-line commands (crucially, `nox -s ...`).
  - **Reporting:** Excellent. Platforms provide clear success/failure status for CD jobs, detailed logs, and often reporting dashboards.
  - **Adaptability:** Excellent. As demonstrated by providing examples, the underlying _strategy_ of calling Task Automation via platform configs is highly adaptable. The primary effort when switching platforms is mapping the general concepts (triggers, setup, secrets, steps) from one platform's syntax to another.
  - **Maturity & Stability:** Excellent. The major CI/CD platforms are mature, stable, and widely used for orchestrating release pipelines.
  - **Community & Documentation:** Excellent. Extensive documentation and community support for setting up CD workflows on common platforms.

- **Conclusion:** The configuration formats of standard CI/CD platforms are the appropriate and capable "tools" at this orchestration layer, designed to manage triggers, environments, sequences, and secrets to orchestrate build and publish/deployment tasks defined in the Task Automation layer.

### Approach: External CD Workflow Engines (e.g., Jenkins, specialized CD tools)

- **Description:** Using separate workflow engines or dedicated CD platforms that specialize in complex deployment orchestration, which may or may not be tightly coupled with the CI platform.
- **Evaluation:** These platforms also rely on being triggered by events and executing predefined steps, which can be configured to call `nox -s <task>` commands. They often offer more advanced features for complex multi-service deployments, rollouts, environment promotions (more related to Topic 16). Their configuration methods vary widely.
- **Conclusion:** While powerful for complex scenarios (relevant to Topic 16), they are not the most common or simplest configuration method for a basic template's default CD example (e.g., publishing a single package or container). Configuring these is typically outside the scope of a general template. The recommended approach of using standard CI/CD platform features covers the primary CD needs for most templated projects.

## Chosen Approach

- **Leveraging platform-specific CI/CD Workflow Configurations** provided by services like `GitHub Actions`{github-actions}, `Bitbucket Pipelines`{bitbucket-pipelines}, `GitLab CI`{gitlab-ci}.
- Configuring these to install the Task Automation layer (`uv`{uv}, `Nox`{nox}), securely inject credentials, and **call Task Automation (`Nox`{nox}) build and publish tasks** (Topic 09, 10, 11, 12).
- Provide **example configuration file(s)** for popular platforms demonstrating this approach.

## Justification for the Choice

This approach is chosen because it utilizes the appropriate tools for this layer – the orchestration capabilities inherent in CI/CD platform configurations – in a way that is robust, secure, and adaptable across different environments:

1.  **Core CD Functionality:** CI/CD platforms provide the necessary primitives for defining release pipelines: triggering on events, setting up environments, sequencing jobs/steps, and managing secrets (addressing **Event Triggering**, **Environment Setup Features**, **Secure Credential Management**, **Orchestration Capability**).
2.  **Achieves CD Automation Securely:** By configuring platform jobs to call `nox -s build` and `nox -s publish` (which uses `uv publish`, relying on injected secrets), we automate the release process and ensure sensitive information is handled using the platform's secure methods. This directly achieves the goal of **Automating Publishing and Managing Credentials Securely**.
3.  **CD Agnosticism (via Task Automation):** This strategy ensures the underlying build and publish logic (in `noxfile.py`) is decoupled from the CD platform configuration. This dramatically simplifies the CD config file, focusing it solely on platform orchestration (triggers, secrets, job structure) rather than application-specific build/publish shell scripting. This is key for **Adaptability** and **Maintainability** of the CD setup.
4.  **Best Fit for Strategy:** This method effectively leverages the strengths of the CI/CD platform layer for orchestration concerns and delegates execution logic to the Task Automation layer, creating a clean separation of concerns.

Providing example configuration files (e.g., for `GitHub Actions`{github-actions}) is essential to guide users on implementing this strategy in practice and demonstrate secure secret usage when calling publishing tasks (addressing **Value of Examples**).

## Interactions with Other Topics

- **Task Automation (12):** This is the core layer invoked by CD. CD configs call `nox -s build:...` and `nox -s publish` commands.
- **Packaging Build (09), Packaging Publish (10), Container Build (11):** CD pipelines trigger and orchestrate the execution of these build and publish tasks defined in Task Automation.
- **CI Orchestration (13):** CD jobs typically run after CI jobs have successfully passed on a given commit/tag. The configuration for CI and CD often resides within the same platform configuration file.
- **Deployment to Production Orchestrators (16):** The artifacts built and potentially published by CD are the primary inputs for deployment tools operating at the production infrastructure layer. CD pipelines might trigger the next stage managed by tools from Topic 16.
