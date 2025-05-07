# Criteria for Tool Selection

Tooling choices in `cookiecutter-robust-python` are not arbitrary. Every significant tool or approach evaluated for inclusion was assessed based on a consistent set of criteria derived directly from the template's core philosophy ([Template Philosophy: The Zen of cookiecutter-robust-python](philosophy.md)).

Understanding these criteria is key to understanding *why* the template uses the tools it does, and how to evaluate alternative tools or approaches as the ecosystem evolves.

## Global Criteria

These criteria were applied broadly across most tool categories and workflow stages. They represent fundamental requirements or strong preferences for any tool adopted as a core part of the template's foundation:

*   **PEP Compliance:** Adherence to relevant Python Enhancement Proposals (packaging - PEP 518, 621, 427, 660; typing - PEP 484, 526; style - PEP 8, PEP 257) and other established standards (e.g., TOML, YAML for configuration, standard report formats like JUnit XML, Cobertura XML). *Especially crucial for configuration formats and standard tool interaction methods*. This is a **non-negotiable requirement** where applicable and defined standards exist.
*   **OS Interoperability:** The tool itself, its method of installation, and its core execution logic (including environment management for task runners) must work reliably and consistently across standard development operating systems: Linux, macOS, and Windows. Complex OS-specific workarounds in standard workflows are strongly avoided. This is a **non-negotiable requirement** for the core developer experience and automated workflows.
*   **CLI Callability:** The tool must have a stable and predictable command-line interface that can be easily invoked and scripted by automation layers ([Task Automation (12)](topics/12_task-automation.md), [CI Orchestration (13)](topics/13_ci-orchestration.md), [CD Orchestration (14)](topics/14_cd-orchestration.md)).
*   **Developer Experience (DX):** How intuitive, straightforward, and efficient is the tool's usage for a developer? Does it streamline common tasks (e.g., adding deps, running checks)? Does it provide clear feedback?
*   **Performance:** Speed of execution for the task the tool performs. This is particularly important for automated steps that run frequently (editors, pre-commit, CI) or take significant time (dependency resolution, large test suites, complex builds). Faster automation directly supports the "Automated is better than manual" principle by reducing waiting time.
*   **Maintainability:** The tool should contribute to the long-term health of the project and the template. Factors include: ease of updating the tool, clarity of its configuration, potential for tool consolidation (reducing tool count), stability of its API/behavior, and ease of contributing to its development (community).
*   **Reproducibility:** Tools involved in dependency management ([Dependency Management (02)](topics/02_dependency-management.md)) and building ([Packaging Build (09)](topics/09_packaging-build.md), [Container Build (11)](topics/11_container-build.md)) must ensure that the same inputs consistently produce the same outputs across environments where feasible.
*   **Maturity & Stability:** How stable is the tool's public interface and behavior? How long has it been battle-tested in real-world projects? Tools marked as explicitly "experimental" are generally avoided for the template's core foundation unless their technical merits are overwhelmingly compelling and stable for the task *despite* the label.
*   **Community & Documentation:** An active development community, good community support (forums, Stack Overflow), and comprehensive, clear documentation are vital for troubleshooting and learning.
*   **Best Tool for the Job vs. Tooling Origin:** The primary goal is to select the tool that best meets *all other criteria* for its specific task, even if it means choosing a tool not implemented in Python itself (e.g., Rust-based). Technical merit and alignment with core requirements override the language of implementation.

## Area-Specific Criteria

In addition to the global criteria, certain areas introduced specific criteria relevant to the task at hand. These are detailed within each topic's dedicated documentation page but include examples like:

*   For [Dependency Management (02)](topics/02_dependency-management.md): Reliability of the dependency resolver on complex graphs, effectiveness of lock files.
*   For [Code Formatting (03)](topics/03_code-formatting.md): Opinionatedness of style, accuracy of style enforcement (vs. PEP 8 compatible).
*   For [Type Checking (05)](topics/05_type-checking.md): Strictness of type checking, support for standard type hinting PEPs, effectiveness with type stubs.
*   For [Packaging Build (09)](topics/09_packaging-build.md): Support for native code extensions and the complexity of cross-platform compilation.
*   For [Task Automation (12)](topics/12_task-automation.md): Effectiveness of task environment isolation.
*   For [Container Build (11)](topics/11_container-build.md): Support for container build best practices (multistage builds, non-root users).
*   For [CI Orchestration (13)](topics/13_ci-orchestration.md): Effectiveness of platform matrix testing features.
*   For [Pre-commit Hooks (18)](topics/18_pre-commit-hooks.md): Speed of execution relative to the commit process.

By evaluating all potential tools against these consistent criteria, we aim to demonstrate that the template's toolchain is not just a collection of popular tools, but a thoughtfully selected, integrated stack designed for building **robust and maintainable** Python projects.
