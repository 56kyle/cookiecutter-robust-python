# 07: Documentation Generation and Building

This section evaluates tools and approaches for generating project documentation. This includes extracting API documentation from code (using docstrings and type hints) and compiling narrative documentation (tutorials, guides, explanations). Well-maintained documentation is fundamental for a project's usability and longevity.

## Goals Addressed

- Make it easy to write project documentation, combining code-generated API references with narrative content.
- Reliably generate API documentation from docstrings (following PEP 257) and type hints.
- Support authoring narrative documentation using standard, easy-to-use formats (e.g., Markdown).
- Provide a simple and scriptable process to build the documentation into a static website (e.g., HTML).
- Ensure the documentation build process is OS-interoperable.
- Produce documentation output that is functional, navigable, and maintainable.

## Evaluation Criteria

- **API Generation (Docstrings & Hints):** How well does it extract documentation from Python docstrings (especially PEP 257) and type hints?
- **Narrative Authoring:** What formats are supported for writing narrative content (reST, Markdown)? How easy is it to write and organize content?
- **Content Combination:** How well does it integrate API reference generated from code with narrative pages?
- **Build Process:** Simplicity, speed, and scriptability of the process to build the documentation website.
- **OS Interoperability (Build):** Does the build process work reliably across Linux, macOS, and Windows?
- **Output Quality:** Functionality (search, navigation), appearance, navigability, and standard format of the generated website.
- **Extensibility:** Can features be added via plugins or extensions?
- **Maturity & Stability:** How stable and battle-tested is the tool?
- **Community & Documentation:** Active development, support, and comprehensive documentation.
- **Best Tool for the Job:** Considering all criteria, which tool provides the strongest overall fit for creating comprehensive, maintainable, and well-integrated project documentation.

## Tools and Approaches Evaluated

We evaluated the leading tools for generating documentation in the Python ecosystem:

### Option 1: :sphinx:`Sphinx` (+ Extensions)

- **Description:** The de-facto standard documentation generator for Python projects. Highly powerful and extensible. Primarily uses reStructuredText (reST) as its source format but supports Markdown via extensions like :myst-parser:`MyST-Parser`. Excels at integrating with code via `autodoc`.
- **Evaluation:**

  - **API Generation (Docstrings & Hints):** Excellent. The `sphinx.ext.autodoc` extension is robust, mature, and widely used for extracting documentation from code based on docstrings (supporting **PEP 257**) and type hints. It integrates seamlessly with extensions like :sphinxautodoctypehints:`sphinx-autodoc-typehints` and [:term:`sphinx.ext.napoleon`](python:sphinx.ext.napoleon) (for Google/NumPy style).
  - **Narrative Authoring:** Moderate (reST). Native reStructuredText is powerful but has a steeper learning curve than Markdown for many developers. Excellent (Markdown via MyST). Using the :myst-parser:`MyST-Parser` allows writing narrative content in more familiar Markdown while retaining Sphinx's advanced features.
  - **Content Combination:** Excellent. :sphinx:`Sphinx` is designed from the ground up to combine narrative content and API references with powerful cross-referencing, indexing, and navigation features.
  - **Build Process:** High. Building is done via the standard `sphinx-build` command, which is highly scriptable (`sphinx-build -b html docs docs/_build/html`). Configuration is in a Python file (`conf.py`), offering flexibility but requiring Python knowledge. Initial setup can involve some steps (running quickstart, configuring extensions).
  - **OS Interoperability (Build):** Excellent. The `sphinx-build` command and core :sphinx:`Sphinx` are pure Python and highly reliable across Linux, macOS, and Windows.
  - **Output Quality:** Excellent. Produces professional, highly navigable websites with advanced search and indexing capabilities. Supports various themes.
  - **Extensibility:** Excellent. Has a vast and mature ecosystem of extensions (`autodoc`, `intersphinx`, themes, plugins for various directives/roles).
  - **Maturity & Stability:** Very High. Extremely mature, stable, and widely used, including for Python's official documentation.
  - **Community & Documentation:** Very High. Large, active community, extensive documentation and resources.

- **Conclusion:** The most powerful and flexible option, particularly strong for deep API documentation and complex content structures. Its primary barrier (reST) is mitigated by MyST Markdown.

### Option 2: :mkdocs:`MkDocs` (+ Plugins)

- **Description:** A simpler, faster documentation generator focused on using Markdown as the source format. Relies heavily on plugins for features like API documentation generation.
- **Evaluation:**

  - **API Generation (Docstrings & Hints):** Moderate. Not built-in. Requires plugins (like `mkdocstrings` + handler plugins for Python) which need to be installed and configured separately. The robustness and feature set of API generation depend entirely on the plugin ecosystem, which is generally less mature and unified than :sphinx:`Sphinx`'s `autodoc`.
  - **Narrative Authoring:** Excellent (Markdown). Designed for writing narrative content in familiar Markdown, making it easy to get started.
  - **Content Combination:** Good (via plugins/structure). Combines narrative Markdown files, with API content often injected via specific plugin directives or generated files linked from the narrative. Less seamless deep linking compared to :sphinx:`Sphinx`.
  - **Build Process:** Excellent. Very simple (`mkdocs build`) and fast. Configuration is in a YAML file (`mkdocs.yml`), generally simpler than :sphinx:`Sphinx`'s Python `conf.py`. Highly scriptable.
  - **OS Interoperability (Build):** Excellent. Pure Python, standard CLI and file operations, highly reliable across OSs.
  - **Output Quality:** High. Produces clean, modern, functional websites, especially with popular themes like Material for :mkdocs:`MkDocs`. Good search and basic navigation.
  - **Extensibility:** High. Has a growing plugin ecosystem for various features, including API docs.
  - **Maturity & Stability:** High. Mature and stable project.
  - **Community & Documentation:** High. Active community, good documentation.

- **Conclusion:** Simpler and faster build process, excellent for Markdown native narrative docs. Less ideal when comprehensive, robust, and deeply integrated API documentation from code is a primary focus, as this requires adding and relying on external plugins.

## Chosen Tool(s)

- Primary Documentation Generator: **:sphinx:`Sphinx`**.
- Source Format: **MyST Markdown** (via :myst-parser:`MyST-Parser`).
- API Integration: **`sphinx.ext.autodoc`**.
- Docstring/Hint Parsing: **:python:sphinx.ext.napoleon)** (Google style), **[:term:`sphinx-autodoc-typehints`](sphinxautodoctypehints:`sphinx.ext.napoleon`**.
- Docstring Linter Helper: **:pydocstyle:`pydocstyle`** (Checks rules used by generator).

## Justification for the Choice

**:sphinx:`Sphinx`** combined with **MyST Markdown** and essential extensions is the best choice for documentation based on its power, standards adherence, and flexibility, while addressing the ease-of-use barrier of its native format:

1.  **Robust API Documentation:** :sphinx:`Sphinx` with `autodoc` is the **standard and most robust method** for extracting documentation directly from Python code's docstrings (following **PEP 257**) and type hints. Integrated with :python:sphinx.ext.napoleon) (for Google style) and [:term:`sphinx-autodoc-typehints`](sphinxautodoctypehints:`sphinx.ext.napoleon` (for type hints), it ensures high-quality, automatically updated API references. This directly serves the **"Documented is better than implied"** philosophy and **API Generation** goal. We use **:pydocstyle:`pydocstyle`** (checked via :ruff:`Ruff` in Topic 04/12) to help ensure docstrings meet the necessary standards for :sphinx:`Sphinx`.
2.  **Flexibility & Power:** :sphinx:`Sphinx` offers unparalleled flexibility for structuring documentation (including complex hierarchies, indices, bibliographies if needed), powerful cross-referencing (linking between API docs, narrative sections, and even external project docs via :sphinx:`intersphinx`), and a vast extension ecosystem (addressing **Content Combination**, **Output Quality**, **Extensibility**).
3.  **Markdown Authoring:** By using the **:myst-parser:`MyST-Parser`** extension, narrative documentation can be written using familiar **Markdown** syntax, significantly lowering the barrier to contribution for most developers compared to reStructuredText (addressing **Narrative Authoring** while keeping Sphinx's power).
4.  **Reliable & OS-Interoperable Build:** The :sphinx:`Sphinx` build process is mature, **scriptable**, and **highly OS-interoperable**, running reliably across Linux, macOS, and Windows (addressing **Build Process** and **OS Interoperability**).
5.  **Community & Standard:** :sphinx:`Sphinx` is the most widely used documentation generator in the Python ecosystem. This provides strong community support and extensive documentation (addressing **Community & Documentation**).

:mkdocs:`MkDocs` was evaluated but its reliance on plugins for robust API documentation generation, coupled with the slightly less flexible content structuring compared to :sphinx:`Sphinx`, made it a secondary choice for a template aiming for comprehensive and deeply integrated documentation from code. The combination chosen here offers the best of both worlds: Markdown ease-of-use with Sphinx's power and robust API integration.

## Interactions with Other Topics

- **pyproject.toml (01):** Documentation dependencies (Sphinx, theme, MyST-Parser, etc.) are managed via :uv:`uv` in a dedicated optional dependency group (Area 02), specified in `pyproject.toml`.
- **Code Linting (04):** :pydocstyle:`pydocstyle` rules (within :ruff:`Ruff`) ensure docstrings are in the correct format (PEP 257) for extraction by :sphinx:`Sphinx`.
- **Task Automation (12):** :nox:`Nox` sessions are defined to build the documentation website (`uv run sphinx-build`).
- **CI Orchestration (13):** Documentation builds are run as part of the automated CI pipeline, triggered by :nox:`Nox`, to check for build errors or warnings.
- **CD Orchestration (14):** Built documentation (from Area 13) can be automatically published (e.g., to GitHub Pages or Read the Docs) via CD pipelines, triggering based on tags or merges to the main branch.
