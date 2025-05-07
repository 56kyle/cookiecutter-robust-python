# conf.py - Sphinx configuration for the cookiecutter-robust-python TEMPLATE documentation.
# This file belongs to the TEMPLATE SOURCE CODE, NOT the generated project.
# See https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from datetime import date # Import date to get the current year


# --- Project information -----------------------------------------------------

# General info about the TEMPLATE documentation itself
project = 'cookiecutter-robust-python Template Documentation'
# Copyright year and author name
copyright = f'{date.today().year}, Kyle Oliver' # Dynamically get current year

# Author name
author = 'Kyle Oliver'

# The version info for the TEMPLATE. Using Calendar Versioning: YYYY.MM.DD
# **UPDATE MANUALLY OR VIA SIMPLE SCRIPT WITH EACH TEMPLATE RELEASE**
# This version tracks the template's development state, not generated projects.
release = "2025.04.28" # Example: YYYY.MM.DD - **UPDATE MANUALLY**
# The short X.Y version for the template (YYYY.MM)
version = "2025.04"   # Example: YYYY.MM - **UPDATE MANUALLY**


# --- Path Setup (No Autodoc on Template Code) ---
# No sys.path manipulation needed as we are not using autodoc to document template source code files.

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here.
extensions = [
    'sphinx.ext.intersphinx',    # Link to documentation of other projects
    'sphinx.ext.napoleon',       # Support for Google and NumPy style docstrings (useful for understanding code mentioned)
    'myst_parser',               # Support for parsing Markdown files (.md)
    'sphinx_autodoc_typehints',  # Better rendering of type hints (useful for understanding code mentioned/evaluated)
    'sphinx_copybutton',         # Adds a "copy" button to code blocks (Excellent QoL)
    # 'sphinx_inlinecopy',       # Alternative inline copy button (remove if using only one copy extension)
    'sphinx_tabs.tabs',          # Adds tab support (Useful for showing OS-specific commands/configs, code variants)
    # 'sphinxcontrib.typer',     # Document Typer CLI applications (if documenting CLIs) - Not essential for tool evaluation docs
    # 'sphinx_click.ext',        # Document Click CLI applications (Fallback for Typer) - Not essential for tool evaluation docs
    # 'sphinx.ext.graphviz',     # For rendering diagrams (if using graphviz directives) - Optional
]

# Add any paths that contain templates relative to this directory.
templates_path = ['_templates'] # Create this directory if needed

# List of patterns relative to source directory, that match files/directories to ignore.
exclude_patterns = [
    '_build',            # Output directory
    'Thumbs.db',         # MacOS files
    '.DS_Store',         # MacOS files
    '.venv',             # Standard virtual environment directory
    '.nox',              # Nox environment directory (for template docs build)
    # EXCLUDE THE GENERATED PROJECT TEMPLATE DIRECTORY ITSELF!!
    # Sphinx runs from 'docs/' directory, so path is relative to there '../{{ cookiecutter.project_slug }}'
    # The {{ cookiecutter.project_slug }} variable is not available here at TEMPLATE doc build time.
    # You need to manually exclude the directory name based on your typical generated slug structure or use a simpler pattern
    # Assuming the generated slug will likely be lowercase/hyphenated based on cookiecutter.json logic
    # e.g., exclude patterns like 'my-robust-python-project', 'another-project-name'
    # Alternatively, exclude based on path structure if generated output goes to a known sibling dir
    # A simple solution for template docs is to manually add generated projects to this list if they cause build issues.
    # For robust template docs, you'd build from the template root and exclude the *rendered* output dir of the generated project.
    # Let's just exclude common development/build environment dirs and rely on the build process to only target the 'docs/' dir.
    'rust',              # Exclude example Rust source dir at template root
    'tests',             # Exclude template's own tests if any (e.g., tests/ directory at template root)
    'cookiecutter.json', # Exclude the cookiecutter input file itself from being treated as a doc source
    'README.md',         # Exclude the template's README file from being treated as a doc source
    'noxfile.py',        # Exclude the template's noxfile
    '.pre-commit-config.yaml', # Exclude template's pre-commit config
    'pyproject.toml',    # Exclude the template's pyproject.toml
    # Add exclusions for other template root files/dirs not meant as docs source
]

# MyST-Parser settings (allows using Markdown + Sphinx features)
myst_enable_extensions = [
    "amsmath", "assign_short_names", "colon_fence", "deflist", "dollarmath",
    "html_admonition", "html_image", "linkify", "replacements", "smartquotes",
    "strikethrough", "substitution", "tasklist", "attrs_inline", "attrs_block",
    # "include", # Optional: If you need to include raw files. Requires myst-enable-extensions loaded before base config
    "codefence_description", # Add description after code fences
]

# Intersphinx mapping: Link to documentation of standard libraries or tools mentioned
# **COMPREHENSIVE LIST of potential tools evaluated**
# Define abbreviations (keys) to link to external docs (values)
# Tuple: (base URL, inventory file path/None for standard)
# Ensure URLs end with / and are correct. Use 'latest' or 'stable' versions often.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None), # Python Standard Library
    'pip': ('https://pip.pypa.io/en/stable/', None), # pip installer
    'venv': ('https://docs.python.org/3/library/venv.html', None), # venv stdlib module (points into python docs)
    'virtualenv': ('https://virtualenv.pypa.io/en/latest/', None), # virtualenv tool
    'piptools': ('https://pip-tools.readthedocs.io/en/latest/', None), # pip-tools
    'poetry': ('https://python-poetry.org/docs/', None), # Poetry
    'pdm': ('https://pdm.fming.dev/latest/', None), # PDM
    'hatch': ('https://hatch.pypa.io/latest/', None), # Hatch
    'uv': ('https://docs.astral.sh/uv/', None), # uv
    'ruff': ('https://docs.astral.sh/ruff/', None), # Ruff
    'pytest': ('https://docs.pytest.org/en/stable/', None), # pytest
    'nox': ('https://nox.thea.codes/en/stable/', None), # Nox
    'build': ('https://pypa-build.readthedocs.io/en/stable/', None), # build
    'twine': ('https://twine.readthedocs.io/en/stable/', None), # twine
    'pre-commit': ('https://pre-commit.com/', None), # pre-commit
    'docker': ('https://docs.docker.com/', None), # Docker (broad docs, maybe less useful intersphinx?)
    'podman': ('https://podman.io/docs/', None), # Podman (check if .inv exists)
    'commitizen': ('https://commitizen-tools.github.io/commitizen/', None), # Commitizen
    'pyright': ('https://pyright.readthedocs.io/en/latest/', None), # Pyright (check if .inv exists)
    'bandit': ('https://bandit.readthedocs.io/en/latest/', None), # Bandit
    'pip-audit': ('https://pip-audit.readthedocs.io/en/latest/', None), # pip-audit
    'pydocstyle': ('https://pydocstyle.readthedocs.io/en/latest/', None), # pydocstyle
    'setuptools': ('https://setuptools.pypa.io/en/latest/', None), # setuptools
    'maturin': ('https://www.maturin.rs/', None), # Maturin homepage (check for .inv) - specific doc links harder
    'typer': ('https://typer.tiangolo.com/', None), # Typer (check for .inv)
    'click': ('https://click.palletsprojects.com/en/latest/', None), # Click
    'coveragepy': ('https://coverage.readthedocs.io/en/latest/', None), # coverage.py (different alias than 'coverage')
    'pytest-cov': ('https://pytest-cov.readthedocs.io/en/latest/', None), # pytest-cov
    'myst-parser': ('https://myst-parser.readthedocs.io/en/latest/', None), # MyST-Parser
    'furo': ('https://pradyunsg.me/furo/latest/', None), # Furo theme
    'sphinxautodoctypehints': ('https://sphinx-autodoc-typehints.readthedocs.io/en/stable/', None), # sphinx-autodoc-typehints
    # Other potential tools evaluated or mentioned:
    'virtualenvwrapper': ('https://virtualenvwrapper.readthedocs.io/en/latest/', None), # virtualenvwrapper
    'tox': ('https://tox.wiki/en/latest/', None), # Tox
    'invoke': ('https://docs.pyinvoke.org/en/latest/', None), # Invoke
    'poethepoet': ('https://poethepoet.natpad.net/latest/', None), # Poe the Poet
    'just': ('https://github.com/casey/just/', None), # Just (no RTD, likely no .inv, link might not work well) - maybe exclude command-line tools w/o standard docs
    # Add other specific flake8 plugins if evaluated beyond general Ruff rules:
    # 'flake8': ('https://flake8.pycqa.org/en/latest/', None),
    # 'flake8-bugbear': ('https://pypi.org/project/flake8-bugbear/', None), # Pypi links rarely have .inv
    'sonarcloud': ('https://docs.sonarcloud.io/', None), # SonarCloud docs (check if .inv exists)
    'argocd': ('https://argo-cd.readthedocs.io/en/stable/', None), # Argo CD docs
    'helm': ('https://helm.sh/docs/', None), # Helm docs (check for .inv)
    'cookiecutter': ('https://cookiecutter.readthedocs.io/en/latest/', None), # cookiecutter itself
    'cruft': ('https://cruft.github.io/', None), # cruft
}


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML output
html_theme = 'furo'

# Add any paths that contain custom static files (like logo, css).
html_static_path = ['_static'] # Create this directory (docs/_static) if you add files like logo.png

# HTML theme options (example for Furo)
html_theme_options = {
     # Use a logo for the template docs (recommended)
     # Create docs/_static/logo-light.png and logo-dark.png
     "sidebar_hide_name": True, # Hide project name next to logo if logo contains it
     # "light_logo": "logo-light.png",
     # "dark_logo": "logo-dark.png",

     # Footer icons
     "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/56kyle/cookiecutter-robust-python", # **UPDATE THIS URL IF TEMPLATE REPO CHANGES**
            "html": "<svg stroke='currentColor' fill='currentColor' stroke-width='0' viewBox='0 0 16 16'><path fill-rule='evenodd' d='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.22.82.69 1.19 1.81.85 2.23.65.07-.51.28-.85.54-1.04-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38C13.71 14.53 16 11.53 16 8c0-4.42-3.58-8-8-8z'></path></svg>",
            "aria-label": "GitHub",
        },
     ],
     # Configure links back to the source repo itself
     "source_repository": "https://github.com/56kyle/cookiecutter-robust-python/", # **UPDATE THIS URL IF TEMPLATE REPO CHANGES**
     "source_branch": "main", # Or your default branch
     "source_directory": "docs/", # Tells Furo that the doc source is in this subdir relative to repo root
}


# -- Options for Napoleon -----------------------------------------------------
# Ensure Napoleon processes Google style docstrings correctly
napoleon_google_docstrings = True # Enable Google style (Parameters, Returns, etc.)
napoleon_numpy_docstrings = False # Disable NumPy style if not used
napoleon_include_init_with_doc = False # Set to true if __init__ only calls super() but has docstrings
napoleon_include_private_with_doc = False # Include private members with docstrings if needed
napoleon_include_special_with_doc = True # Include special members (__str__, etc.)
napoleon_use_admonition_for_examples = True # Render Examples sections as admonitions (Recommended)
napoleon_use_admonition_for_notes = True    # Render Notes sections as admonitions (Recommended)
napoleon_use_admonition_for_references = True # Render References sections as admonitions (Recommended)
# Control parameter list format: use keyword is often nicer
napoleon_use_keyword = True # Use :keyword: role (aligns with Google style recommendation)
napoleon_use_param = True # Use :param: role
napoleon_use_rtype = True # Use :rtype: role (Recommended when using type hints)
napoleon_attr_annotations = True # Document attributes with type annotations

# -- Options for sphinx-autodoc-typehints -------------------------------------
# This extension handles displaying type hints correctly and adds type annotation to Parameters/Returns sections
# https://sphinx-autodoc-typehints.readthedocs.io/en/stable/
set_type_checking_flag = True # Needed for some strict type hint interpretations with autodoc
always_document_param_types = False # Usually False; Set True to add ':param type: param' even if description is only hint
typehints_fully_qualified = False # Display type hints without the module path (e.g., "str" instead of "builtins.str") (Recommended)
typehints_document_rtype = True # Add return type annotation to "Returns" section (recommended)
# typehints_format = 'short' # Or 'fully-qualified', 'google', 'numpy'. 'short' is common

# -- Options for other extensions (Optional, uncomment if used) --------------
# sphinx_tabs_enable_tabs_js = True # Enable JavaScript for Sphinx-tabs (Required if sphinx_tabs.tabs is enabled)
