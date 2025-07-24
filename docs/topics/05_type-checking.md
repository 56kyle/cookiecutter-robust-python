# 05: Type Checking

This section evaluates static type checkers, which analyze code leveraging type hints without executing it to find potential type errors. Incorporating static type checking catches bugs earlier in the development cycle, improves code maintainability, and aids refactoring, aligning with the "Type hints are one honking great idea" philosophy.

## Goals Addressed

- Statically verify the correct usage of type hints and catch type errors before runtime.
- Identify inconsistencies between declared types and actual usage across different code paths.
- Ensure adherence to Python's type hinting PEPs (PEP 484, 526, 593, etc.).
- Integrate seamlessly into editor feedback, Task Automation layers, and CI/CD pipelines.
- Work effectively with type stubs for libraries without native type hints.
- (Implicit Goal for this template) Enable/accept the practice of _requiring_ type hints in project code.

## Evaluation Criteria

- **PEP Compliance:** How well does the tool understand and enforce Python's type hinting PEPs?
- **Comprehensive & Strict Checking:** Does it perform thorough analysis? Can strict modes be enabled to enforce type safety comprehensively?
- **Performance:** Speed of analysis, especially on larger codebases or for fast feedback loops (editors, pre-commit, CI).
- **OS Interoperability:** Does the tool work reliably and consistently across Linux, macOS, and Windows?
- **Integration:** How well does it integrate with editors/IDEs (real-time feedback), pre-commit hooks, Task Automation runners, and CI/CD platforms?
- **Support for Stubs:** Does it effectively use type stubs (typeshed, third-party `.pyi` files) for libraries?
- **Error Messages:** Clarity, precision, and actionability of reported type errors.
- **Maturity & Stability:** How stable and battle-tested is the tool?
- **Community & Documentation:** Active development, support, and comprehensive documentation.
- **Best Tool for the Job:** Considering all criteria, which tool offers the strongest overall fit, prioritizing accurate PEP adherence, performance, and integration for a streamlined, reliable type checking workflow in a template that expects type hints.

## Tools and Approaches Evaluated

We evaluated the primary static type checkers for Python:

### Option 1: {mypy}`Mypy<>`

- **Description:** The original static type checker for Python, often considered the reference implementation for type hinting PEPs. Implemented in Python.
- **Evaluation:**
  - **PEP Compliance:** Very High. Closely follows type hinting PEPs, seen as a reference for interpretation.
  - **Comprehensive & Strict Checking:** Very High. Provides extensive checks and strong strictness modes (`--strict`).
  - **Performance:** Moderate. Can be slow on larger codebases or initial runs. Caching helps, but still generally slower than {pyright}`Pyright<>`. Impacts fast feedback loops.
  - **OS Interoperability:** Excellent. Pure Python package, works reliably across OSs.
  - **Integration:** Excellent. Widely supported, integrates well into editors (though real-time performance is a factor), {pre-commit}`pre-commit<>` (official hook exists but can be slow), Task Automation, CI/CD.
  - **Support for Stubs:** Excellent. Deep integration with :python{typeshed}`typeshed<>` and the stub ecosystem.
  - **Error Messages:** High. Generally clear, but can be verbose or challenging in complex cases.
  - **Maturity & Stability:** Very High. Extremely mature, stable, long-standing.
  - **Community & Documentation:** Very High. Large, active community, extensive documentation and resources.
- **Conclusion:** The mature, standard Python-based checker. Strong on PEP adherence, comprehensiveness, and community. Its main drawback is performance, which hinders its use in fast, iterative workflow stages.

### Option 2: {pyright}`Pyright<>`

- **Description:** A static type checker from Microsoft, implemented in TypeScript/Node.js. Built with performance and strong PEP adherence as key goals. Powers the :pyright-documentation - part of Pyright documentation:`Pylance` VS Code extension.
- **Evaluation:**
  - **PEP Compliance:** Very High. Actively developed to adhere closely to and quickly support type hinting PEPs. Provides excellent and sometimes stricter analysis based on PEP interpretation than default {mypy}`Mypy<>`.
  - **Comprehensive & Strict Checking:** Very High. Provides a deep level of type analysis. Strong strictness modes (`strict` flag).
  - **Performance:** Excellent. **Significantly faster** than {mypy}`Mypy<>`. Designed for fast incremental checks and overall lower analysis time. Much more practical for real-time editor feedback, fast pre-commit runs, and quicker CI.
  - **OS Interoperability:** High. Works on major OSs. Relies on Node.js runtime internally (often bundled in distributions), making installation/setup slightly more complex than pure Python tools, but seamless for users of common distributions (like `npm` or bundled wheels/binaries).
  - **Integration:** Excellent. Strong CLI (`pyright`). Integrates exceptionally well with editors (real-time analysis via Language Server Protocol), well-suited for fast {pre-commit}`pre-commit<>` hooks (better performance than {mypy}`Mypy<>`), Task Automation, CI/CD.
  - **Support for Stubs:** Excellent. Works effectively with :python{typeshed}`typeshed<>` and other stub sources.
  - **Error Messages:** Very High. Generally very clear, precise, and actionable messages.
  - **Maturity & Stability:** High. Mature, actively developed by Microsoft. Large user base, especially via :pyright-documentation - part of Pyright documentation:`Pylance`. Stable for production use.
  - **Community & Documentation:** High. Strong community (especially VS Code users), extensive documentation (though sometimes focused on :pyright-documentation - part of Pyright documentation:`Pylance`).
- **Conclusion:** Offers compelling performance advantages over {mypy}`Mypy<>` while maintaining high standards adherence and comprehensiveness. Its speed makes it a much better fit for integrating type checks into rapid workflow stages.

### Option 3: {pytype}`Pytype<>`

- **Description:** A static type analyzer from Google. Key feature is its ability to infer types even in unannotated code. Can perform checks on partially or fully annotated code as well. Implemented in Python.
- **Evaluation:**
  - **PEP Compliance:** High. Supports relevant PEPs, but its inference approach interacts differently than analysis focused solely on declared hints. Might not strictly enforce hint completeness in the same way if inference is enabled.
  - **Comprehensive & Strict Checking:** High. Comprehensive checks when hints are present, but its strength in inference makes its strictness model different. Not ideal for a template _requiring_ annotations, where inference is less needed than strict checking of explicit hints.
  - **Performance:** Moderate. Can be faster than {mypy}`Mypy<>` on initial runs for some codebases due to backend, but not typically as fast as {pyright}`Pyright<>` for incremental checks.
  - **OS Interoperability:** Excellent. Pure Python package, works reliably across OSs.
  - **Integration:** High. CLI tool for Task Automation and CI. Less common for real-time editor feedback or fast pre-commit due to performance and focus.
  - **Support for Stubs:** Very High. Deep integration with :python{typeshed}`typeshed<>` and excels at type inference.
  - **Error Messages:** Moderate to High. Can be less precise in inference scenarios.
  - **Maturity & Stability:** High. Mature, actively developed at Google. Community outside Google is smaller than {mypy}`Mypy<>` or {pyright}`Pyright<>`.
- **Conclusion:** Best suited for gradually adding typing to unannotated codebases. For a template that _mandates_ or strongly encourages type hints, its core strength (inference) is less relevant, and its performance and strictness on explicit hints are not better than {mypy}`Mypy<>` or {pyright}`Pyright<>`.

### Option 4: {beartype}`Beartype<>`

- **Description:** A runtime type checker using the `@beartype` decorator. Enforces type hints _at runtime_ when code is executed. Also has performance optimization aspects.
- **Evaluation:**
  - **Static Analysis Capabilities:** Poor (None). {beartype}`Beartype<>` is a _runtime_ checker, not a static analysis tool. It doesn't find errors in unexecuted code paths or provide design-time feedback like the other options.
  - **Enforces Coding Standards:** N/A (different type of tool).
  - **Informative & Actionable Feedback:** Excellent (Runtime). Provides very clear, specific exceptions at runtime if type hints are violated during execution. Useful for debugging runtime issues but not for static analysis.
  - **Configurable:** High (Decorator/Global Config). Configured in code via decorator or globally.
  - **Performance:** Excellent (Runtime). Minimal to negative runtime overhead.
  - **OS Interoperability:** Excellent. Pure Python, works across OSs.
  - **Integration:** Moderate (Code-centric). Integrated by adding decorators to code. Not a standalone analysis tool run in a workflow. Relevant during testing or in production.
  - **Support for Stubs:** N/A (operates on source code/runtime values).
  - **Maturity & Stability:** High. Mature, stable.
  - **Community & Documentation:** High. Active development and community.
- **Conclusion:** A powerful _complementary_ tool for runtime type checking and optimization, especially in testing or production. It does **not** fulfill the role of a static type checker and should not be evaluated as one for this area's primary goal of static analysis feedback. It's best included as an optional addition documented separately.

## Chosen Tool(s)

- **{pyright}`Pyright<>`** as the primary **Static Type Checker**.

## Justification for the Choice

**{pyright}`Pyright<>`** is selected as the primary static type checker because it best balances accurate standards adherence, performance, and workflow integration, crucial for a template promoting the use of type hints:

1.  **Exceptional Performance:** {pyright}`Pyright<>` offers **significantly faster analysis speed** than {mypy}`Mypy<>` (its main competitor), which is a major advantage for providing rapid type feedback in editors and accelerating CI pipelines. This practical **Performance** benefit is key for user adoption and aligns with optimizing automation ("Automated is better than manual").
2.  **Standards Conformance & Strictness:** {pyright}`Pyright<>` is actively developed to adhere rigorously to Python's type hinting **PEPs** and provides powerful **comprehensive and strict checking** capabilities. It reliably enforces type safety based on declared hints.
3.  **Seamless Workflow Integration:** Its speed makes it much more viable for fast feedback loops (e.g., potential inclusion in {pre-commit}`pre-commit<>` hooks, very fast editor feedback via Language Server integration) and integrates **excellently** into Task Automation ({nox}`Nox<>`) and CI/CD pipelines (Area 12, 13, 14). It's **OS-interoperable**.
4.  **Clear Feedback:** {pyright}`Pyright<>`'s error messages are typically **very clear and actionable**, aiding developers in fixing type issues.

While {mypy}`Mypy<>` is the standard and historical reference, {pyright}`Pyright<>`'s performance advantage for iterative development and CI is a critical factor that provides a tangibly better experience for users when type checking is mandated or heavily used. {pytype}`Pytype<>` is less suitable for a template _requiring_ explicit hints. {beartype}`Beartype<>` is a different class of tool (runtime checker).

By choosing {pyright}`Pyright<>`, the template selects a tool that delivers high-quality, standard-aligned type checking with the speed necessary for a modern, automated workflow.

## Interactions with Other Topics

- **pyproject.toml (01):** {pyright}`Pyright<>`'s configuration lives in `pyrightconfig.json` or `[tool.pyright]` in `pyproject.toml`.
- **Code Linting (04):** {ruff}`Ruff<>` can catch some basic type-related issues (e.g., unused imports related to typing), but {pyright}`Pyright<>` performs the deep static type analysis.
- **Testing (06):** Passing type checks should ideally be a prerequisite to running tests in CI, catching type errors before test execution.
- **Task Automation (12):** {nox}`Nox<>` sessions call `uv run pyright` to run the type checker.
- **CI Orchestration (13):** Type checks are run as part of the automated CI pipeline, triggered by {nox}`Nox<>`.
- **Dev Containers (17):** {pyright}`Pyright<>` is installed and configured within the development container for editor integration and terminal checks.
- **Pre-commit Hooks (18):** {pyright}`Pyright<>`'s speed makes it potentially viable for a comprehensive type checking pre-commit hook (compared to {mypy}`Mypy<>`), though full checks are often left to Task Automation/CI.
