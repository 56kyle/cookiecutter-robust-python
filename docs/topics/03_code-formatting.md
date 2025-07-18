# 03: Code Formatting

This section evaluates tools designed to automatically reformat source code to adhere to a consistent style guide. Automated code formatting reduces cognitive load during code reviews, prevents debates about style, and ensures a clean, uniform codebase, significantly aiding long-term maintainability.

## Goals Addressed

- Automatically enforce a consistent code style across the entire project.
- Reduce style-related discussions during code reviews.
- Ensure compliance with (or create a style based on) PEP 8 guidelines.
- Integrate seamlessly with pre-commit hooks, Task Automation layers, and CI/CD pipelines.

## Evaluation Criteria

- **Style & Adherence:** How well does it enforce a consistent style? Does it adhere to (or provide a strong opinionated style based on) PEP 8?
- **Opinionatedness & Configuration:** How opinionated is it? Does it require minimal or zero configuration to get a good result?
- **Performance:** Speed of formatting, especially on larger codebases or when run frequently (e.g., in pre-commit).
- **OS Interoperability:** Does the tool work reliably and consistently across Linux, macOS, and Windows?
- **Integration:** How well does it integrate with pre-commit hooks, Task Automation runners, CI/CD, and editors/IDEs?
- **Tool Count:** Does it handle related tasks like import sorting, or require additional tools?
- **Maturity & Stability:** How stable and battle-tested is the tool?
- **Community & Documentation:** Active development, support, and comprehensive documentation.
- **Best Tool for the Job:** Considering all criteria, which tool offers the strongest overall fit, prioritizing performance, standards, OS interop, and ease of use.

## Tools and Approaches Evaluated

We evaluated the leading options for automated code formatting:

### Option 1: [:term:`Black`](black-documentation) (+ [:term:`isort`](isort-documentation))

- **Description:** [:term:`Black`](black-documentation) is a widely adopted, highly opinionated code formatter known for its minimal configuration. It enforces a consistent style that is largely PEP 8 compliant. It does not handle import sorting, so it's commonly paired with [:term:`isort`](isort-documentation).
- **Evaluation:**
  - **Style & Adherence:** High. Enforces a consistent, opinionated style ("Black style") that is generally considered PEP 8 compatible. Not pedantically PEP 8, but focuses on creating a clear, automatic style.
  - **Opinionatedness & Configuration:** Very High. Famously requires minimal configuration (`--line-length` is a common option). Aligns with the "Opinionated is better than impartial" philosophy.
  - **Performance:** Good. Reasonably fast for typical file sizes and project sizes. Noticeably slower than Rust-based alternatives like [:term:`Ruff`](ruff-documentation) on larger codebases or when run very frequently.
  - **OS Interoperability:** Excellent. Pure Python package, works reliably on all major operating systems.
  - **Integration:** Excellent. Long-standing standard, strong integration with [:term:`pre-commit`](pre-commit-documentation), [:term:`Nox`](nox-documentation)/[:term:`uv` run](uv-documentation), CI platforms, and almost all editors/IDEs.
  - **Tool Count:** Moderate. Requires using two separate tools (`black`, `isort`) for the complete formatting task (code style + import sorting). Adds a small layer of management (dependencies, running both).
  - **Maturity & Stability:** Very High. Mature, stable, widely used standard.
  - **Community & Documentation:** Very High. Large, active community, extensive documentation.
- **Conclusion:** The current established standard. Strong on philosophy alignment (opinionated, PEP compatible style) and integration. Its main drawbacks are performance compared to newer tools and requiring a second tool for import sorting.

### Option 2: [:term:`autopep8`](autopep8-documentation)

- **Description:** Applies PEP 8 formatting using the `pep8` (now `pycodestyle`) utility. Less opinionated and performs fewer transformations than [:term:`Black`](black-documentation).
- **Evaluation:**

  - **Style & Adherence:** Moderate. Focuses narrowly on applying basic PEP 8 violations flagged by `pycodestyle`. Doesn't enforce a holistic, consistent style like [:term:`Black`](black-documentation) or [:term:`Ruff`](ruff-documentation). Doesn't handle import sorting.
  - **Opinionatedness & Configuration:** Moderate. More configuration options than [:term:`Black`](black-documentation), less opinionated.
  - **Performance:** Good. Generally similar to [:term:`Black`](black-documentation).
  - **OS Interoperability:** Excellent. Pure Python package, works reliably across OSs.
  - **Integration:** Good. Standard CLI, integrates into workflows.
  - **Tool Count:** High. Needs a separate linter to identify issues, needs [:term:`isort`](isort-documentation) for import sorting, less all-in-one than [:term:`Black`](black-documentation).
  - **Maturity & Stability:** High. Mature, stable.
  - **Community & Documentation:** Good.

- **Conclusion:** Less suitable for a template aiming for a strongly opinionated, consistent style with minimal configuration. Better as a tool to fix specific, limited PEP 8 violations.

### Option 3: [:term:`yapf`](yapf-documentation)

- **Description:** Google's opinionated code formatter. Similar goals to [:term:`Black`](black-documentation) but often with different formatting output and more configuration options.
- **Evaluation:**

  - **Style & Adherence:** High. Enforces a consistent, opinionated style. Adherence to PEP 8 varies based on configuration.
  - **Opinionatedness & Configuration:** High opinionated defaults, but also offers significant configuration, which can deviate from minimal config philosophy.
  - **Performance:** Good.
  - **OS Interoperability:** Excellent. Pure Python, works across OSs.
  - **Integration:** Good. Standard CLI, integrates into workflows. Less ubiquitous editor/IDE support than [:term:`Black`](black-documentation).
  - **Tool Count:** Needs [:term:`isort`](isort-documentation) for import sorting.
  - **Maturity & Stability:** High. Mature, stable.
  - **Community & Documentation:** Moderate compared to [:term:`Black`](black-documentation).

- **Conclusion:** A viable alternative to [:term:`Black`](black-documentation) for opinionated formatting, but its style is less universally adopted in the Python community compared to Black, and its higher configurability doesn't align as strongly with the "zero-config opinionated" goal.

### Option 4: [:term:`Ruff`](ruff-documentation) (Formatter)

- **Description:** An extremely fast linter and formatter written in Rust. The formatter aims to be a drop-in, style-compatible replacement for [:term:`Black`](black-documentation) and [:term:`isort`](isort-documentation), offering significantly higher performance.
- **Evaluation:**
  - **Style & Adherence:** High. Explicitly designed to match [:term:`Black`](black-documentation)'s default formatting style, providing a consistent, PEP 8 compatible style (effectively implementing "Black style").
  - **Opinionatedness & Configuration:** Very High. Highly opinionated with minimal configuration, inheriting philosophy from [:term:`Black`](black-documentation). Configuration is shared with the linter in `pyproject.toml` or `.ruff.toml`.
  - **Performance:** Excellent. **Orders of magnitude faster** than all Python-based formatters ([:term:`Black`](black-documentation), [:term:`isort`](isort-documentation), [:term:`autopep8`](autopep8-documentation), [:term:`yapf`](yapf-documentation)). This is a major practical advantage, especially for pre-commit hooks and large projects.
  - **OS Interoperability:** Excellent. Rust binary, works natively and reliably across all major operating systems.
  - **Integration:** Excellent and Growing Rapidly. Native support in [:term:`pre-commit`](pre-commit-documentation), easily callable via CLI for [:term:`Nox`](nox-documentation)/[:term:`uv` run](uv-documentation), integrates into CI, rapidly gaining editor/IDE support due to its speed and dual formatting/linting capabilities.
  - **Tool Count:** Excellent. **Consolidates code formatting AND import sorting** into a single tool and command (`ruff format`).
  - **Maturity & Stability:** High (Formatter is newer than Linter, but built on stable core). [:term:`Ruff`](ruff-documentation) as a project is very mature. The formatter feature itself is newer but built on the same highly performant core and rapidly stabilizing, considered production-ready by its authors.
  - **Community & Documentation:** High (Exploding). Very active development, massive and rapidly growing user base, excellent and extensive documentation.

## Chosen Tool(s)

- **[:term:`Ruff`](ruff-documentation)** (using the `ruff format` command).

## Justification for the Choice

**[:term:`Ruff`](ruff-documentation) (Formatter)** is the clear choice for code formatting based on its exceptional technical advantages and strong alignment with the template's core principles:

1.  **Superior Performance:** [:term:`Ruff`](ruff-documentation)'s **unmatched speed** is a game-changer for the development workflow. It significantly accelerates automated formatting, making [:term:`pre-commit`](pre-commit-documentation) hooks (Area 18) nearly instantaneous and dramatically reducing CI build times (Area 13). This directly embodies the **"Automated is better than manual"** principle by optimizing automation's efficiency and is the primary reason it stands out (addressing **Performance**).
2.  **Toolchain Simplification:** [:term:`Ruff`](ruff-documentation) **consolidates code formatting and import sorting** ([:term:`isort`](isort-documentation) functionality) into a single tool and command (`ruff format`), simplifying the project's dependencies and configuration compared to the traditional [:term:`Black`](black-documentation) + [:term:`isort`](isort-documentation) pairing (addressing **Tool Count** and contributing to **Maintainability**).
3.  **Opinionated Style & Standard Alignment:** It adopts a highly opinionated style by default that **matches [:term:`Black`](black-documentation)**, which is a widely accepted convention based on **PEP 8**. This provides the desired consistent style with minimal configuration (aligning with **"Opinionated is better than impartial"**, **"Thought out is better than preferred"**, **Style & Adherence**, **Opinionatedness & Configuration**).
4.  **Robust & Cross-Platform:** As a Rust binary, it is **fully OS-interoperable** and reliable across development environments (addressing **OS Interoperability**).
5.  **Seamless Integration:** [:term:`Ruff`](ruff-documentation)'s speed and straightforward CLI integrate **excellently** with [:term:`pre-commit`](pre-commit-documentation) hooks (Area 18), Task Automation runners ([:term:`Nox`](nox-documentation) - Area 12), and CI/CD pipelines (Area 13) (addressing **Integration**).

While [:term:`Black`](black-documentation) and [:term:`isort`](isort-documentation) are mature standards with vast adoption, [:term:`Ruff`](ruff-documentation)'s performance and consolidation benefits provide a tangible, superior advantage for the template's goals without compromising on style quality, opinionation, or standard compatibility (as it implements a widely accepted standard style). [:term:`autopep8`](autopep8-documentation) and [:term:`yapf`](yapf-documentation) were less suitable due to either less comprehensive styling or higher configuration/less community adoption compared to [:term:`Black`](black-documentation)/[:term:`Ruff`](ruff-documentation).

The choice of [:term:`Ruff`](ruff-documentation) embodies the **"Best Tool for the Job"** principle by prioritizing a tool that significantly optimizes a key automated task (formatting) while meeting all other essential criteria and simplifying the toolchain.

## Interactions with Other Topics

- **Code Linting (04):** [:term:`Ruff`](ruff-documentation) is also the chosen linter. This creates a powerful single-tool solution for both linting and formatting, simplifying configuration (shared `.ruff.toml` file) and dependency management (one tool to install).
- **pyproject.toml (01):** While configured primarily in a separate `.ruff.toml` file, [:term:`Ruff`](ruff-documentation) reads its configuration from there.
- **Pre-commit Hooks (18):** [:term:`Ruff`](ruff-documentation)'s exceptional speed makes it ideal for mandated pre-commit hooks, ensuring style is checked and fixed automatically before every commit.
- **Task Automation (12):** [:term:`Nox`](nox-documentation) sessions will call `uv run ruff format` to run the formatter across the project.
- **CI Orchestration (13):** Formatting checks are run as part of the automated CI pipeline, triggered by [:term:`Nox`](nox-documentation).
