# 08: Code Security and Safety Checks

This section evaluates tools used to identify potential security risks in Python projects. This includes scanning for known vulnerabilities in third-party dependencies and analyzing the project's own code for common insecure coding practices. Implementing automated security checks is a vital part of building reliable and responsible software.

## Goals Addressed

- Scan project dependencies against known vulnerability databases.
- Analyze the project's source code for common security pitfalls (e.g., insecure function usage, hardcoded credentials).
- Provide clear and actionable reports on security findings.
- Integrate security checks into automated workflows (Task Automation, CI/CD, potentially pre-commit).
- Ensure the security scanning tools are OS-interoperable.

## Evaluation Criteria

- **Check Types & Coverage:** What types of security issues does it cover (dependency vulnerabilities, code patterns)? How comprehensive are the checks within its scope?
- **Vulnerability Sources (for Dep Scanning):** How reliable and up-to-date are the databases or sources used to identify dependency vulnerabilities? Does it check against standard sources like the PyPI Advisory Database?
- **Analysis Reliability (for Code Scanning):** How accurate are the rules/patterns used for code analysis?
- **False Positives:** How prone is the tool to reporting issues that are not actual vulnerabilities in context?
- **Reporting:** Clarity, detail, and actionability of security reports. Supported formats for integration (e.g., standard text, JSON, XML).
- **Performance:** Speed of scanning, especially for integration into rapid workflows.
- **OS Interoperability:** Does the tool work reliably and consistently across Linux, macOS, and Windows?
- **Integration:** How well does it integrate into Task Automation runners, CI/CD pipelines, and potentially pre-commit hooks?
- **Maturity & Stability:** How stable and battle-tested is the tool?
- **Community & Documentation:** Active development, support, and comprehensive documentation.
- **Best Tool for the Job:** Considering all criteria, which tool or combination offers the strongest overall fit for providing robust and integrated dependency and code security checks.

## Tools and Approaches Evaluated

We evaluated the primary tools for dependency and code-level security checks in Python:

### Option 1: [:term:`Safety`](safety-documentation)

- **Description:** A command-line tool that checks installed Python dependencies (from environments or requirement files) against a database of known security vulnerabilities (pyup.io vulnerability database).
- **Evaluation:**

  - **Check Types & Coverage:** High (Dep Scanning). Focused specifically on checking installed dependencies for known vulnerabilities.
  - **Vulnerability Sources:** High. Uses a curated and actively maintained database. Focus is primarily on packages listed in PyPI.
  - **Analysis Reliability (Code):** N/A (Dependency scanning only).
  - **False Positives:** Good. Generally reports based on verified vulnerabilities.
  - **Reporting:** High. Clear reports with package name, affected versions, and vulnerability ID/description.
  - **Performance:** High. Generally fast, depends on dependency list size and database query speed. Suitable for automation.
  - **OS Interoperability:** Excellent. Pure Python package, works reliably across OSs.
  - **Integration:** Excellent. Simple CLI (`safety check`), easily integrated into Task Automation, CI/CD, and potentially pre-commit (if run against a static file).
  - **Maturity & Stability:** High. Mature, stable, widely used for dependency checking.
  - **Community & Documentation:** High. Active maintenance and good documentation.

- **Conclusion:** A solid, focused tool for checking dependency vulnerabilities. Well-integrated into workflows.

### Option 2: [:term:`Bandit`](bandit-documentation)

- **Description:** A static analyzer designed specifically for finding common security issues in Python source code based on predefined patterns and rules (e.g., uses of `eval`, hardcoded passwords, SQL injection risks).
- **Evaluation:**

  - **Check Types & Coverage:** High (Code Scanning). Focuses specifically on static analysis of code for common security anti-patterns. Covers a wide range of known pitfalls. Does NOT check dependency vulnerabilities.
  - **Vulnerability Sources (Dep):** N/A (Code scanning only).
  - **Analysis Reliability (Code):** High. Uses a well-developed set of rules based on security expertise.
  - **False Positives:** Moderate. Like most static analysis tools, it can produce false positives depending on code context. Requires review and potential configuration/baselining.
  - **Reporting:** High. Reports with severity levels, confidence scores, rule IDs, and code snippets. Supports various formats.
  - **Performance:** Good. Analysis speed depends on codebase size. Generally reasonable, but can be slower than Rust-based tools like [:term:`Ruff`](ruff-documentation) in the future. Can be too slow for mandated pre-commit hooks on large projects.
  - **OS Interoperability:** Excellent. Pure Python package, works reliably across OSs.
  - **Integration:** Excellent. Simple CLI (`bandit`), easily integrated into Task Automation, CI/CD. Viable for pre-commit if focused or on smaller codebases.
  - **Maturity & Stability:** High. Mature, stable, widely used for code security analysis.
  - **Community & Documentation:** High. Active maintenance and good documentation.

- **Conclusion:** The standard, reliable tool for finding security issues within the project's own code. Complements dependency checkers.

### Option 3: [:term:`pip-audit`](pip-audit-documentation)

- **Description:** A newer, PyPA-backed tool focused on dependency vulnerability scanning. Aims to use a broader set of vulnerability sources (PyPI Advisory Database, OS vendor databases) compared to relying on a single database.
- **Evaluation:**

  - **Check Types & Coverage:** High (Dep Scanning). Focused specifically on checking dependencies.
  - **Vulnerability Sources:** Very High. Accesses multiple sources including the official PyPI Advisory Database, potentially offering broader and more up-to-date coverage than tools using single curated databases.
  - **Analysis Reliability (Code):** N/A (Dependency scanning only).
  - **False Positives:** High. Relies on established vulnerability data, leading to generally low false positives for reported CVEs.
  - **Reporting:** High. Clear reports, supports standard output formats (JSON, JUnit XML) for better integration.
  - **Performance:** High. Similar performance profile to [:term:`Safety`](safety-documentation), suitable for automation.
  - **OS Interoperability:** Excellent. Pure Python package, works reliably across OSs.
  - **Integration:** Excellent. Designed for automation with a clear CLI. Easily integrated into Task Automation, CI/CD.
  - **Maturity & Stability:** High. Newer than [:term:`Safety`](safety-documentation), but rapidly gaining maturity and features, backed by PyPA.
  - **Community & Documentation:** High. Active development, growing community, good documentation.

- **Conclusion:** A modern, technically strong choice for dependency vulnerability scanning, potentially offering better vulnerability source coverage than alternatives. Preferred over [:term:`Safety`](safety-documentation) for a template prioritizing modern standards and potentially broader coverage.

### Option 4: [:term:`Ruff`](ruff-documentation) (Security Rules)

- **Description:** [:term:`Ruff`](ruff-documentation), the fast linter (04), is adding security-focused rules (prefix 'S') that re-implement checks found in [:term:`Bandit`](bandit-documentation). This is an emerging feature.
- **Evaluation:**

  - **Check Types & Coverage:** Moderate (Code Scanning, Limited Subset). Re-implements _some_ [:term:`Bandit`](bandit-documentation) rules, but the coverage is not yet comprehensive enough to replace [:term:`Bandit`](bandit-bandit-documentation) entirely. Does NOT check dependency vulnerabilities.
  - **Analysis Reliability (Code):** High (Rules). Reliability of implemented rules is high, mirroring their source in [:term:`Bandit`](bandit-bandit-documentation).
  - **False Positives:** Moderate. Inherited from source rules.
  - **Reporting:** Excellent. Uses [:term:`Ruff`](ruff-documentation)'s standard, clear reporting format.
  - **Performance:** Excellent. As a Rust binary, running these checks is very fast (similar to linting performance).
  - **OS Interoperability:** Excellent. Rust binary, works across OSs.
  - **Integration:** Excellent. Seamlessly integrated into [:term:`Ruff`](ruff-documentation)'s check command, leveraging its integrations ([:term:`pre-commit`](pre-commit-documentation), [:term:`Nox`](nox-documentation)/[:term:`uv` run](uv-documentation), CI). Speed makes it ideal for fast checks.
  - **Maturity & Stability:** High ([:term:`Ruff`](ruff-documentation)), Low (Security Rules). The [:term:`Ruff`](ruff-documentation) platform is mature. The _security rule set_ is still very new and under active development, not comprehensive enough for full standalone security code analysis.
  - **Community & Documentation:** High ([:term:`Ruff`](ruff-documentation)), Moderate (Security Rules). Benefits from the large [:term:`Ruff`](ruff-documentation) community, but specific documentation and community experience with _just_ the security rules are still building.

- **Conclusion:** Promising for future consolidation and performance, but currently not sufficient to replace a dedicated code security tool like [:term:`Bandit`](bandit-bandit-documentation) for comprehensive checks. Valuable as a complementary set of fast checks if enabled alongside other [:term:`Ruff`](ruff-documentation) rules.

### Option 5: [:term:`SonarCloud`](sonarcloud-documentation) / SonarQube

- **Description:** A cloud-based (or self-hosted SonarQube) code quality and security service. Provides comprehensive static analysis (bugs, vulnerabilities, security hotspots, code smells) across many languages via a dedicated scanner integrated into CI/CD.
- **Evaluation:**

  - **Check Types & Coverage:** Excellent (Comprehensive Analysis Suite). Covers code vulnerabilities, security hotspots, _and_ dependency vulnerabilities (often via integration with other tools or its own analysis). Offers a much broader analysis than single CLI tools, including different types of issues and historical tracking.
  - **Vulnerability Sources (Dep):** High. Uses its own analysis and may integrate with other databases. Coverage varies by language/setup. Can be configured to integrate with standard dependency scanning tool outputs.
  - **Analysis Reliability (Code):** Excellent. Large, proprietary, actively maintained rule set often providing deep and accurate analysis.
  - **False Positives:** Moderate to High. While sophisticated, requires tuning and false positive management on the platform dashboard.
  - **Reporting:** Excellent (Platform-based). Provides rich web dashboards, historical trends, quality gates, PR decorations. Reporting is a core strength, but is service-based, not simple CLI output.
  - **Performance:** Moderate (Analysis + Service). Requires running a scanner (adds analysis time) and uploading data to the service. Not suitable for fast local feedback (editors, pre-commit). Primarily for CI/CD.
  - **OS Interoperability:** High (Scanners). Scanner tools work on major OSs. The service is cloud-based.
  - **Integration:** Excellent (CI/CD). Designed for integration into CI/CD pipelines via dedicated tasks/scanners. Requires service setup.
  - **Maturity & Stability:** Excellent. Mature, industry-standard platform.
  - **Community & Documentation:** Excellent. Large community, extensive documentation.

- **Conclusion:** Provides the most comprehensive analysis suite and reporting _as a service_. However, it requires external service setup and is not suitable as a core, self-contained CLI tool run locally without external dependencies for the base template. It's an optional, highly recommended addition for teams wanting deeper, platform-integrated security analysis.

## Chosen Tool(s) and Strategy

- Dependency Vulnerability Scanning: **[:term:`pip-audit`](pip-audit-documentation)**.
- Code Security Static Analysis: **[:term:`Bandit`](bandit-documentation)**.

## Justification for the Choice

We choose a combination of **[:term:`pip-audit`](pip-audit-documentation)** and **[:term:`Bandit`](bandit-bandit-documentation)** to provide comprehensive coverage for both dependency and code-level security checks, prioritizing robust, standard, and OS-interoperable CLI tools:

1.  **Comprehensive Coverage:** Security requires checking _both_ dependencies (Area 02's outputs) and the project's own code. [:term:`pip-audit`](pip-audit-documentation) excels at the former (addressing **Check Types & Coverage** for deps), while [:term:`Bandit`](bandit-bandit-documentation) excels at the latter (addressing **Check Types & Coverage** for code). Using both provides the necessary breadth.
2.  **Robust Standards and Sources:** [:term:`pip-audit`](pip-audit-documentation) leverages the official PyPI Advisory Database and other sources, offering strong **Vulnerability Sources** and high reporting **Reliability** for dependencies. [:term:`Bandit`](bandit-bandit-documentation) uses a mature and well-established set of rules for **Analysis Reliability** in code scanning.
3.  **Workflow Integration:** Both tools are **OS-interoperable** and have **excellent CLI interfaces** suitable for automation. They are designed to be invoked by Task Automation runners ([:term:`Nox`](nox-documentation) - Area 12) and run within CI/CD pipelines (Area 13, 14) (addressing **OS Interoperability** and **Integration**). While potentially usable in [:term:`pre-commit`](pre-commit-documentation) for focused or small projects, their performance profile makes them better suited for mandatory checks in Task Automation/CI as opposed to instant commit gates.
4.  **Tool Type Alignment:** We prioritize self-contained CLI tools over service-based platforms (like [:term:`SonarCloud`](sonarcloud-documentation)) for the template's core, as CLI tools require less external setup and are more universally runnable without external accounts or infrastructure (addressing **Best Tool for the Job** in the context of a base template).

**[:term:`Ruff`](ruff-documentation)**'s emerging security rules (Area 04) are promising but currently lack the comprehensive coverage of [:term:`Bandit`](bandit-bandit-documentation), so [:term:`Bandit`](bandit-bandit-documentation) is chosen for the full code security analysis. [:term:`Safety`](safety-documentation) is a strong alternative to [:term:`pip-audit`](pip-audit-documentation), but [:term:`pip-audit`](pip-audit-documentation)'s use of official PyPI sources makes it slightly preferred for adherence to PyPA recommended practices.

**Deployment Strategy within Workflow:**

- **Pre-commit Hooks (18):** Do NOT mandate running these comprehensive security checks in pre-commit hooks due to performance concerns and potential for false positives slowing down commits. Pre-commit focuses on fast, high-confidence issues (like formatting, basic lint).
- **Task Automation (12):** Define a dedicated Nox session (e.g., `nox -s security`) that runs both `uv run pip-audit --python session.python` and `uv run bandit -c .bandit -r {{ cookiecutter.package_name }}`. This provides a single command for developers to run the full security suite locally.
- **CI Orchestration (13):** Mandate running the `nox -s security` task as part of the automated CI pipeline, ensuring the full security suite passes before merges or deployments.
- **Optional Service Integration:** Document [:term:`SonarCloud`](sonarcloud-documentation) as a powerful optional addition for teams needing deeper analysis, dashboards, and quality gates, integrated directly into CI workflows.

This layered approach ensures that robust security checks are a mandatory part of the CI process, easily runnable locally on demand, using standard, OS-interoperable CLI tools, while acknowledging the existence of more advanced service options.

## Interactions with Other Topics

- **Dependency Management (02):** [:term:`pip-audit`](pip-audit-documentation) relies on the dependencies managed by [:term:`uv`](uv-documentation) and the `uv.lock` file. Security tools themselves are installed as dependencies via [:term:`uv`](uv-documentation).
- **Code Linting (04):** Both [:term:`Bandit`](bandit-bandit-documentation) and [:term:`Ruff`](ruff-documentation) (which includes some security rules) perform static code analysis, but with different focuses and rule sets. They can be run alongside other linters.
- **Task Automation (12):** [:term:`Nox`](nox-documentation) orchestrates the execution of [:term:`pip-audit`](pip-audit-documentation) and [:term:`Bandit`](bandit-bandit-documentation) within dedicated sessions.
- **CI Orchestration (13):** The CI pipeline mandates running the security checks defined in the Task Automation layer. [:term:`SonarCloud`](sonarcloud-documentation) is integrated at this layer as an optional service.
- **Pre-commit Hooks (18):** While comprehensive security checks are not mandated here, fast subsets could potentially be added in the future.
