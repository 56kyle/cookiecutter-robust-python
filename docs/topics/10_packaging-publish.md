# 10: Package Publishing (to PyPI/Index Servers)

This section evaluates tools and approaches for uploading Python distribution packages to package indexes like the Python Package Index (PyPI). Successfully publishing packages is essential for sharing your work and enabling others to use your project as a dependency.

## Goals Addressed

- Provide a simple, secure, and standard way to upload built `sdist` and `wheel` packages to PyPI or other package servers (like TestPyPI, or private indexes).
- Handle authentication with the package index securely.
- Integrate seamlessly into automated workflows (Task Automation, CI/CD).
- Ensure the publishing process is OS-interoperable.
- Produce packages compatible with installation by standard tools like `pip`{pip-documentation}. (Addressed in Area 09's Build Process).

## Evaluation Criteria

- **Standard Practice:** Does it use the current recommended method for uploading to PyPI?
- **Security (Authentication):** How securely does it handle authentication credentials (usernames/passwords, API tokens)? Does it support recommended practices like API tokens and environment variables?
- **Compatibility:** Does it work reliably with packages built using standard tools (PEP 517 frontends/backends)?
- **Reliability:** How robust is the upload process (e.g., handling network issues)?
- **OS Interoperability:** Does the tool work reliably across Linux, macOS, and Windows?
- **CLI Usability:** Is the command-line interface straightforward for uploading packages?
- **Integration:** How well does it integrate into Task Automation runners and CI/CD pipelines?
- **Maturity & Stability:** How stable and battle-tested is the tool?
- **Community & Documentation:** Active development, support, and comprehensive documentation.
- **Best Tool for the Job:** Considering all criteria, which tool provides the strongest overall fit for providing standard, secure, and integrated package publishing capabilities.

## Tools and Approaches Evaluated

While various approaches exist, there is one overwhelmingly recommended standard tool:

### Option 1: `twine`{twine-documentation}

- **Description:** The official, PyPA-recommended command-line utility for securely uploading Python packages. It was developed to replace older, less secure methods like `python setup.py upload` and encourages the use of secure protocols and API tokens.
- **Evaluation:**

  - **Standard Practice:** Excellent. Explicitly the standard and recommended tool by the PyPA.
  - **Security (Authentication):** Excellent. Prioritizes and seamlessly supports using **API tokens** (recommended best practice over username/password) and reading credentials from **environment variables**, which is crucial for secure automation in CI/CD (Area 14). Supports `.pypirc` but environment variables are preferred for automation security.
  - **Compatibility:** Excellent. Designed specifically to upload the standard `.sdist` and `.whl` files produced by any PEP 517 compliant build process (like the one from Area 09).
  - **Reliability:** High. Designed for a robust upload process. Includes checks.
  - **OS Interoperability:** Excellent. Pure Python package with a simple CLI, works reliably on all major OSs.
  - **CLI Usability:** Excellent. Simple command syntax (`twine upload dist/*`) for the core task. Easy to specify repositories or signing options.
  - **Integration:** Excellent. Simple CLI designed for scripting, integrates seamlessly into Task Automation (`Nox`{nox-documentation}) and CI/CD pipelines, especially when leveraging environment variables for credentials.
  - **Maturity & Stability:** Very High. The established standard for publishing, very mature and stable.
  - **Community & Documentation:** Very High. Widely adopted, extensive documentation, supported by PyPA.

- **Conclusion:** The clear, recommended standard tool that meets all criteria exceptionally well, particularly security and compatibility.

### Option 2: Dependency Manager `publish` commands (e.g., `uv`{uv-documentation} publish, `PDM`{pdm-documentation} publish, `Poetry`{poetry-documentation} publish, `Hatch`{hatch-documentation} publish)

- **Description:** Modern dependency managers often include their own `publish` command as part of their integrated workflow CLI. These commands typically wrap the functionality of `twine`{twine-documentation} or implement similar logic internally.
- **Evaluation:**
  - **Standard Practice:** High (Method), Excellent (Outcome). While the _command_ itself is tool-specific (`uv publish` vs `twine upload`), the _underlying process_ often uses or replicates `twine`{twine-documentation}'s logic and interacts with PyPI using standard APIs and authentication methods. They produce the same outcome as using `twine`{twine-documentation} directly.
  - **Security (Authentication):** Excellent. Rely on environment variables (e.g., `UV_TOKEN`, `TWINE_API_KEY`) or integrated config/secrets management, generally supporting secure practices.
  - **Compatibility:** Excellent. Designed to work with packages built using the manager's preferred build process (Area 09).
  - **Reliability:** High. Reliability depends on the manager's implementation of the publishing logic.
  - **OS Interoperability:** Excellent. Tools are cross-platform.
  - **CLI Usability:** Excellent. A simple command within the manager's unified CLI (e.g., `uv publish`). Potentially slightly more convenient if already using the manager's CLI for other tasks.
  - **Integration:** Excellent. Integrates within their manager's ecosystem and is callable from Task Automation (`Nox`{nox-documentation}) and CI/CD.
  - **Maturity & Stability:** High (depends on manager maturity). The `publish` command is usually stable if the manager itself is stable. `uv`{uv-documentation}'s `publish` command is newer but built on a solid base.
- **Conclusion:** A strong, often more convenient alternative within a specific manager's ecosystem. Provides equivalent functionality to `twine`{twine-documentation} for the user interacting via the manager's CLI. For a template, using the manager's publish command simplifies the required tooling listed as development dependencies if the manager handles publishing internally.

## Chosen Tool(s)

- The recommended underlying tool is **`twine`{twine-documentation}**.
- Invocation Method: **`uv`{uv-documentation}**'s `uv publish` command (calls Twine or similar internally) or calling `uv run twine upload` directly.

## Justification for the Choice

For publishing packages, there is a clear consensus on using a tool that adheres to secure, standard practices for interacting with PyPI. **`twine`{twine-documentation}** is the established standard. While other tools like `uv`{uv-documentation} offer `publish` commands, they typically provide a user-facing wrapper around `twine`{twine-documentation}'s functionality or replicate its standard behavior.

Using **`uv`{uv-documentation}**'s native `uv publish` command offers the most integrated experience within the chosen dependency manager's CLI. This simplifies the Task Automation layer (Area 12) by having a single command to call (`uv publish`) rather than needing `twine` explicitly listed as a top-level dev dependency and calling `uv run twine`. It leverages the efficiency and integration provided by `uv`{uv-documentation}. If `uv publish` is confirmed to fully replicate `twine`{twine-documentation}'s best practices (secure authentication, standard protocol) then it's the preferred interface.

Therefore, we choose to standardize on using **`uv`{uv-documentation}'s `uv publish` command** as the primary invocation method for publishing within the Task Automation layer. This command is built using `twine`{twine-documentation}'s best practices or `twine`{twine-documentation} itself. This aligns with having `uv`{uv-documentation} as the central workflow tool (Area 12) for dependency/package operations while relying on the underlying standard (`twine`{twine-documentation} equivalent logic).

## Interactions with Other Topics

- **Packaging Build (09):** The output of Area 09 (files in `dist/`) are the input packages for publishing.
- **Task Automation (12):** `Nox`{nox-documentation} sessions call `uv publish` to automate the publishing process. This session typically runs after a successful `build` session.
- **CD Orchestration (14):** CD pipelines trigger the publish step (via Nox calling `uv publish`). This is where secure API tokens for PyPI are provided to the environment.
- **Dependency Management (02):** If calling `uv run twine`, then `twine` would need to be listed as a dependency (e.g., in the `dev` or a specific `publish` group). If `uv publish` is used, `twine` itself might not need to be a direct dev dependency of the project user (though it is needed by `uv`{uv-documentation} internally if `uv publish` wraps it). Standardizing on `uv publish` might reduce the user's direct dependency list slightly.
