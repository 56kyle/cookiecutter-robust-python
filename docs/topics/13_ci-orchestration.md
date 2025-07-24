# 13: Continuous Integration (CI) Orchestration

This section discusses how to set up Continuous Integration (CI) for a project. CI is the practice of automatically verifying code changes frequently by running checks (linting, typing, security) and tests. The primary goal here is not to define _what_ checks are run (that's done in the Task Automation layer), but _how_ to orchestrate their execution reliably on every code change using an external CI platform.

## Goals Addressed

- Automate the execution of code quality checks, tests, and security scans (defined in the Task Automation layer) on code changes (e.g., on pushes, pull requests).
- Set up environments for running CI jobs, including obtaining the source code and correct Python versions.
- Run tests and checks across relevant Python versions and operating systems.
- Generate and collect reports (test results, coverage) from CI runs.
- Provide clear status reporting on code changes within the version control platform.

## Core Orchestration Strategy: Leveraging Task Automation

A fundamental design choice of this template is to place the specific logic for _how_ to run checks and tests within the project's **Task Automation layer (Topic 12 - `Nox`{nox<>})**. The CI platform's configuration acts as a **thin orchestration layer**.

This design means the CI configuration (e.g., a YAML file) should primarily:

1.  Check out the project's source code.
2.  Set up a compatible Python environment and ensure the Task Automation tool (`Nox`{nox<>}, and `uv`{uv<>} as its backend) is available.
3.  Call the relevant, universal **`nox -s <task>`** commands to execute the desired checks and tests.

## Evaluation Criteria (for CI Platform Orchestration Approach)

Since we don't choose _a single_ CI platform for users, we evaluate _the characteristics that make the strategy of orchestrating via Task Automation beneficial across CI platforms_ and the value of providing examples.

- **Enables CI/CD Agnosticism:** How effectively does this strategy allow using different CI platforms without rewriting core execution logic?
- **Simplifies CI Configuration:** How does placing logic in Task Automation reduce the complexity of the CI platform's configuration file?
- **Improves Workflow Consistency:** How does running tasks via Task Automation in CI align with running tasks locally?
- **Leverages Platform Features:** Does the strategy effectively utilize standard CI platform capabilities (environment setup, matrices, reporting)?
- **Adaptability:** How easy is it to adapt this strategy to a different CI platform?
- **Value of Examples:** How do concrete examples for popular platforms aid users in implementing this strategy?

## Approaches and Tools Evaluated

We focus on the approach of using standard CI platforms to orchestrate the template's built-in Task Automation. We discuss various platforms (e.g., `GitHub Actions`{github-actions<>}, `Bitbucket Pipelines`{bitbucket-pipelines<>}, `GitLab CI`{gitlab-ci<>}) not to select _the_ best platform, but as examples demonstrating this approach.

### Approach: Using Standard CI Platforms (`GitHub Actions`{github-actions<>}, `Bitbucket Pipelines`{bitbucket-pipelines<>}, `GitLab CI`{gitlab-ci<>}, etc.) to orchestrate `Nox`{nox<>} tasks.

- **Description:** Configuring CI workflows (via platform-specific YAML/config) to trigger jobs on VCS events, set up environment, and execute `nox -s <task>` commands to run checks and tests defined in `noxfile.py`.
- **Evaluation against Criteria:**
  - **Enables CI/CD Agnosticism:** Excellent. The core execution logic for checks and tests resides solely within the `noxfile.py`. The CI config is reduced to steps that install dependencies required by the nox session (like `uv`{uv<>}) and `Nox`{nox<>} itself, then run the specific `nox -s <task>` command. This means the CI config for running tests, for instance, looks very similar across different CI platforms, dramatically simplifying migration if needed.
  - **Simplifies CI Configuration:** Excellent. Instead of complex scripts for "how to run ruff," "how to run pyright," "how to run pytest with coverage," etc., the CI config step becomes the simple and readable `run: uvx nox -s <task_name>` or `run: nox -s <task_name>` if uv is already on the system path. This reduces boilerplate and complex scripting directly within the CI config file.
  - **Improves Workflow Consistency:** Excellent. Running `nox -s test` locally uses the same logic and environments as running `nox -s test` in CI. This minimizes "it works on my machine but not in CI" issues related to environment setup and command execution, providing a more reliable and predictable workflow for developers.
  - **Leverages Platform Features:** Excellent. This strategy effectively utilizes standard CI platform features:
    - **Checkout:** Standard step to get code.
    - **Environment Setup:** Uses platform actions/steps to set up required Python versions (e.g., `actions/setup-python` on GitHub Actions) and cache dependencies efficiently, which is better handled by the platform than trying to manage these complex caching strategies manually in a simple Task Automation script.
    - **Matrix Testing:** Combines platform matrix capabilities (OS + Python versions) with Nox's ability to run across multiple Python versions (using the Nox `python=` parameter) or specifically configured sessions to cover testing requirements reliably across combinations.
    - **Reporting:** Leverages the platform's ability to collect standard reports (JUnit XML from `pytest`{pytest<>}, Cobertura XML from `coverage.py`{coveragepy<>}) generated by the Task Automation layer.
    - **Status Checks:** The platform provides visual feedback (pass/fail) linked to commits/PRs based on job outcomes.
  - **Adaptability:** Excellent. Switching CI platforms involves mapping the checkout, Python setup, caching, secrets, and artifact steps from the old platform to the new one, and then configuring the new platform to call the _same_ `nox -s <task>` commands as before. The core Task Automation logic (`noxfile.py`) remains unchanged.
  - **Value of Examples:** Very High. Providing concrete examples for popular platforms (like `GitHub Actions`{github-actions<>}) significantly speeds up user adoption of this strategy by providing a ready-to-use template configuration, demonstrating exactly how to integrate Task Automation calls, setup, matrixing, and reporting.

## Chosen Approach

- **Configure CI workflows (via platform-specific config files)** to orchestrate jobs that install the template's Task Automation tool chain (`uv`{uv<>}, `Nox`{nox<>}) and **call Task Automation (`Nox`{nox<>}) sessions** to execute checks and tests.
- Provide **example configuration file(s)** for popular CI platforms demonstrating this approach.

## Justification for the Choice

This approach is chosen because it maximally aligns the project structure and workflow with the template's goals for automation, consistency, and maintainability across diverse environments:

1.  **CI/CD Agnosticism (Achieved by Strategy):** By defining execution logic _once_ in the Task Automation layer and calling it from CI, the project avoids vendor lock-in at the workflow logic level. This simplifies maintenance and allows switching CI platforms more easily without rewriting extensive build/test scripts. This directly supports **Maintainability** and **Adaptability**.
2.  **Simplified Configuration:** Placing task execution logic in `noxfile.py` keeps the CI platform's configuration file shorter, more readable, and focused on the infrastructure concerns (jobs, environments, steps) rather than the application-specific _how-to-execute_ details.
3.  **Robust Workflow Consistency:** Running checks via Task Automation commands provides the same execution environment and behavior locally and in CI, ensuring reliable and predictable outcomes for automated checks and tests.
4.  **Best Use of Tools:** This strategy leverages the strengths of each layer: VCS (triggering), CI platforms (environment setup, matrices, reporting, secrets), and Task Automation (execution logic, tool orchestration, environment isolation within tasks).

Providing examples for popular platforms (e.g., a `.github/workflows/ci.yml` file) is essential to illustrate _how_ this strategy is implemented in practice ("Leading by example" as a _communication tactic_ to teach the strategy).

## Interactions with Other Topics

- **Task Automation (12):** This is the core layer invoked by CI. CI calls `nox -s <task>` commands.
- **Dependency Management (02):** CI setup includes steps to install dependencies (using `uv`{uv<>}) needed by Nox sessions.
- **Code Quality (03, 04, 05, 08):** CI runs the checks for formatting, linting, typing, and security defined and orchestrated by Task Automation.
- **Testing (06):** CI runs the test suite across matrices defined by Task Automation, leveraging platform matrix capabilities. Test and coverage reports are collected.
- **Packaging Build (09) & Container Build (11):** CI may include jobs to build packages/containers via Task Automation commands to ensure the build process itself passes before merges.
- **CD Orchestration (14):** CI often acts as a prerequisite stage for CD. Successful CI runs trigger CD workflows.
