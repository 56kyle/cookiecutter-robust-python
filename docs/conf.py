# conf.py - Sphinx configuration for the cookiecutter-robust-python TEMPLATE documentation.
# This file belongs to the TEMPLATE SOURCE CODE, NOT the generated project.
# See https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import date


project = "cookiecutter-robust-python Template Documentation"
copyright = f"{date.today().year}, Kyle Oliver"  # noqa

author = "Kyle Oliver"

release = "2025.04.28"
version = "2025.04"

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.extlinks",
    "myst_parser",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
]
templates_path = ["_templates"]

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    ".nox",
    "rust",
    "tests",
    "cookiecutter.json",
    "README.md",
    "noxfile.py",
    ".pre-commit-config.yaml",
    "pyproject.toml",
]

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
    "attrs_inline",
    "attrs_block",
]

extlinks = {
    "argocd": ("https://argo-cd.readthedocs.io", None),
    "autopep8": ("https://pypi.org/project/autopep8", None),
    "bandit-bandit": ("https://bandit.readthedocs.io", None),
    "bandit": ("https://github.com/PyCQA/bandit", None),
    "beartype": ("https://beartype.readthedocs.io", None),
    "bitbucket-pipelines": ("https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines", None),
    "black": ("https://black.readthedocs.io", None),
    "build": ("https://pypa-build.readthedocs.io", None),
    "commitizen": ("https://commitizen-tools.github.io/commitizen", None),
    "coveragepy-coverage": ("https://coverage.readthedocs.io", None),
    "coveragepy": ("https://github.com/nedbat/coveragepy", None),
    "cruft": ("https://cruft.github.io/cruft", None),
    "docker-compose": ("https://docs.docker.com/compose", None),
    "docker": ("https://docs.docker.com", None),
    "flake8": ("https://flake8.pycqa.org", None),
    "flit": ("https://flit.pypa.io", None),
    "github-actions": ("https://docs.github.com/en/actions", None),
    "gitlab-ci": ("https://docs.gitlab.com/ee/ci", None),
    "hatch": ("https://hatch.pypa.io", None),
    "hatchling": ("https://hatch.pypa.io/latest/hatchling", None),
    "helm": ("https://helm.sh", None),
    "invoke": ("https://www.pyinvoke.org", None),
    "isort": ("https://pycqa.github.io/isort", None),
    "just": ("https://just.systems", None),
    "maturin": ("https://maturin.rs", None),
    "mkdocs": ("https://www.mkdocs.org", None),
    "mypy": ("https://mypy-lang.org", None),
    "myst-parser": ("https://myst-parser.readthedocs.io", None),
    "nox": ("https://nox.thea.codes", None),
    "pdm": ("https://pdm.fming.dev", None),
    "pip-audit": ("https://github.com/pypa/pip-audit", None),
    "pip": ("https://pip.pypa.io", None),
    "pip-tools": ("https://pip-tools.readthedocs.io", None),
    "podman": ("https://podman.io", None),
    "poethepoet": ("https://github.com/nat-n/poethepoet", None),
    "poetry": ("https://python-poetry.org", None),
    "pre-commit": ("https://pre-commit.com", None),
    "pydocstyle": ("https://www.pydocstyle.org", None),
    "pylint": ("https://pylint.pycqa.org", None),
    "pyright": ("https://github.com/microsoft/pyright", None),
    "pytest": ("https://docs.pytest.org", None),
    "pytest-pytest-cov": ("https://pytest-cov.readthedocs.io", None),
    "pytype": ("https://github.com/google/pytype", None),
    "ruff": ("https://docs.astral.sh/ruff", None),
    "safety": ("https://pyup.io", None),
    "setuptools": ("https://setuptools.pypa.io", None),
    "sonarcloud": ("https://sonarcloud.io", None),
    "sphinx": ("https://www.sphinx-doc.org", None),
    "sphinxautodoctypehints": ("https://sphinx-autodoc-typehints.readthedocs.io", None),
    "tox": ("https://tox.readthedocs.io", None),
    "twine": ("https://twine.readthedocs.io", None),
    "uv": ("https://docs.uv.dev", None),
    "virtualenv": ("https://virtualenv.pypa.io", None),
    "yapf": ("https://github.com/google/yapf", None)
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pip": ("https://pip.pypa.io/en/stable/", None),
}

html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "sidebar_hide_name": True,
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/56kyle/cookiecutter-robust-python",
            "html": "<svg stroke='currentColor' fill='currentColor' stroke-width='0' viewBox='0 0 16 16'><path fill-rule='evenodd' d='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.22.82.69 1.19 1.81.85 2.23.65.07-.51.28-.85.54-1.04-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38C13.71 14.53 16 11.53 16 8c0-4.42-3.58-8-8-8z'></path></svg>",
            "aria-label": "GitHub",
        },
    ],
    "source_repository": "https://github.com/56kyle/cookiecutter-robust-python/",
    "source_branch": "main",
    "source_directory": "docs/",
}

napoleon_google_docstrings = True
napoleon_numpy_docstrings = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_keyword = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_attr_annotations = True

set_type_checking_flag = True
always_document_param_types = False
typehints_fully_qualified = False
typehints_document_rtype = True
typehints_format = "google"
