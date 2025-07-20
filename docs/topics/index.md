# Evaluated Toolchain Topics

This section contains the detailed documentation for each of the 18 topics that make up the **cookiecutter-robust-python** template's integrated toolchain. For each topic, you will find:

- The specific goals this area addresses.
- The criteria used to evaluate tools within this area, derived from the template's philosophy ([Template Philosophy](../philosophy.md)) and core criteria ([Criteria](../criteria.md)).
- A list of the key tools and approaches that were evaluated.
- A detailed breakdown and comparison of these tools against the criteria.
- The final tool(s) or approach chosen for the template, with a comprehensive justification explaining _why_ based on meeting the criteria and comparing favorably against alternatives.
- Notes on how this topic interacts with other parts of the template's toolchain.

Reading these topics provides a deep understanding of the template's design choices and the rationale behind the selected tools, empowering you to maintain generated projects effectively and evaluate future tooling changes.

---

```{toctree}
:maxdepth: 2
:caption: Toolchain Topics

01_project-structure.md
02_dependency-management.md
03_code-formatting.md
04_code-linting.md
05_type-checking.md
06_testing-coverage.md
07_documentation.md
08_security-checks.md
09_packaging-build.md
10_packaging-publish.md
11_container-build.md
12_task-automation.md
13_ci-orchestration.md
14_cd-orchestration.md
15_compose-local.md
16_prod-deploy-guidance.md
17_dev-containers.md
18_pre-commit-hooks.md
```

---

**Key Tooling Concepts**

Many topics involve key concepts and tool categories that interact across different areas:

- **`pyproject.toml`:** The central configuration file used by many tools, defining project metadata, build system, dependencies, and tool-specific settings ([Topic 01](01_project-structure.md)).
- **Command-Line Interface (CLI):** Most tools selected have strong CLIs, crucial for integration into automation ([Criteria](criteria.md)).
- **Standard Virtual Environments:** Python's built-in way to isolate project dependencies ([Topic 02](02_dependency-management.md)).
- **Container Images ({unittest-documentation}, Docker/Podman):** Standard format and tools for creating portable application environments ([Topic 11](11_container-build.md)).
- **Layered Workflow:** The template organizes automation into distinct layers: Pre-commit (fast local checks), Task Automation (on-demand/comprehensive local runs), and CI/CD (automated verification/deployment) (Topics [12](12_task-automation.md), [13](13_ci-orchestration.md), [14](14_cd-orchestration.md), [18](18_pre-commit-hooks.md)).

Understanding these interconnected concepts helps to see the "big picture" of the template's design.
