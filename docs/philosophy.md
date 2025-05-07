# Template Philosophy

This section details the core principles and philosophy behind the design and tooling choices made in the `cookiecutter-robust-python` template. This is the foundation for understanding *why* the template is structured the way it is and serves as guidance for its ongoing maintenance and evolution.

## The Zen of cookiecutter-robust-python

```text
Opinionated is better than impartial.
Thought out is better than preferred.
Leading by example is better than demanding.
Maintainable is better than feature-filled.
Documented is better than implied.
Compatibility counts.
Special cases should be allowed, but at their own expense.
Although providing a way out might prevent them entirely.
Metaprogramming should be avoided.
Unless it improves maintainability on both ends.
In the face of ambiguity, prioritize future compatibility.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Astral.
Automated is better than manual.
Although manual is better than poorly automated.
If the implementation isn't PEP compliant, it's a bad idea.
If the implementation is PEP compliant, it may be a good idea.
Type hints are one honking great idea -- let's do more of those!
```
## Core Principles

The philosophy of `cookiecutter-robust-python` centers on creating Python projects that are **reliable, easy to maintain, and enable efficient developer workflows**. These core principles guide every decision about the template's structure and tools:

1.  **Focus on Reliability:** Build projects that are technically solid and minimize potential for errors in development and production. This involves selecting tools that perform rigorous quality checks, facilitate comprehensive testing, and support reproducible environments across operating systems. Multi-OS compatibility is fundamental.
2.  **Prioritize Maintainability:** Structure projects and select tools that make them easy to understand, update, and adapt over time. Consistency in code style, clear configuration, predictable workflows, and dependency management that supports straightforward updates contribute to long-term health. Documentation of the *reasons* for choices is essential for maintaining the template itself.
3.  **Enable Efficient Automation:** Automate repetitive tasks to improve efficiency and consistency. Checks, tests, builds, and other workflow steps should be easily runnable via command line. Automation should be as fast as possible to provide rapid feedback, particularly for local checks.
4.  **Adhere to Applicable Standards:** Follow relevant Python Enhancement Proposals (PEPs) and established community standards where they exist and provide clear benefits, especially for defining configurations and tool interfaces. Pragmatism may be needed where newer, technically superior tools temporarily deviate in less critical areas (like lock file formats) while upholding core standards (like PEP 621 declaration).
5.  **Provide a Curated, Opinionated Approach:** Offer a specific, well-reasoned set of tools and configurations based on evaluation against defined criteria, rather than trying to support all possibilities. The template presents a clear path believed to be the best starting point.
6.  **Demonstrate Effective Practices:** The template serves as a working example. It shows *how* to integrate tools into real-world development, testing, and deployment workflows through provided configurations and scripts, guiding users by illustrating functional patterns.

These principles form the basis for the evaluation criteria and justifications detailed in the [Evaluated Toolchain Topics](topics/index.md). They are the underlying reasons for selecting the specific tools included in `cookiecutter-robust-python`, aimed at providing a solid and practical foundation for Python projects.

## Solved Issues

The [Robust Python Cookiecutter] also exists to solve a few key issues that were omnipresent in [cookiecutter-hypermodern-python].

### 
