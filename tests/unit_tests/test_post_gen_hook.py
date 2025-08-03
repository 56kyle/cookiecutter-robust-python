from pathlib import Path

import pytest


@pytest.mark.parametrize(
    argnames="removed_relative_path",
    argvalues=[".gitlab-ci.yml", "bitbucket-pipelines.yml"]
)
@pytest.mark.parametrize(
    argnames="robust_demo__repository_provider",
    argvalues=["github"],
    indirect=True
)
def test_files_removed_for_github(robust_demo: Path, removed_relative_path: str) -> None:
    path: Path = robust_demo / removed_relative_path
    assert not path.exists()


@pytest.mark.parametrize(
    argnames="removed_relative_path",
    argvalues=[".github", "bitbucket-pipelines.yml"]
)
@pytest.mark.parametrize(
    argnames="robust_demo__repository_provider",
    argvalues=["gitlab"],
    indirect=True
)
def test_files_removed_for_gitlab(robust_demo: Path, removed_relative_path: str) -> None:
    path: Path = robust_demo / removed_relative_path
    assert not path.exists()


@pytest.mark.parametrize(
    argnames="removed_relative_path",
    argvalues=[".github", ".gitlab-ci.yml"]
)
@pytest.mark.parametrize(
    argnames="robust_demo__repository_provider",
    argvalues=["bitbucket"],
    indirect=True
)
def test_files_removed_for_bitbucket(robust_demo: Path, removed_relative_path: str) -> None:
    path: Path = robust_demo / removed_relative_path
    assert not path.exists()


@pytest.mark.parametrize(
    argnames="removed_relative_path",
    argvalues=[
        "rust",
        ".github/workflows/lint-rust.yml",
        ".github/workflows/build-rust.yml",
        ".github/workflows/test-rust.yml"
    ]
)
@pytest.mark.parametrize(
    argnames="robust_demo__add_rust_extension",
    argvalues=[False],
    indirect=True,
    ids=["no-rust"]
)
@pytest.mark.parametrize(
    argnames="robust_demo__repository_provider",
    argvalues=["github"],
    indirect=True,
)
def test_files_removed_for_no_rust_extension(robust_demo: Path, removed_relative_path: str) -> None:
    path: Path = robust_demo / removed_relative_path
    assert not path.exists()
