from subprocess import CalledProcessError
from pathlib import Path

import pytest

from argonautai.git import Repository


@pytest.fixture
def not_repo_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("not_repo")


def test_head_revision_normal():
    base_dir = Path(".")
    repo = Repository(base_dir=base_dir)
    actual = repo.head_revision()
    assert len(actual) == 40


def test_head_revision_base_dir_is_not_repo(not_repo_dir):
    repo = Repository(base_dir=not_repo_dir)
    with pytest.raises(
        CalledProcessError,
        match=r"Command '\['git', 'rev-parse', 'HEAD'\]' returned non-zero.*",
    ):
        repo.head_revision()


@pytest.mark.parametrize(
    "pip_style, expected",
    [
        (False, "git@github.com:nagomiso/argonautai.git"),
        (True, "git+ssh://git@github.com/nagomiso/argonautai.git"),
    ],
)
def test_origin_url_normal(pip_style, expected):
    base_dir = Path(".")
    repo = Repository(base_dir=base_dir)
    actual = repo.origin_url(pip_style=pip_style)
    assert actual == expected


def test_origin_url_base_dir_is_not_repo(not_repo_dir):
    repo = Repository(base_dir=not_repo_dir)
    with pytest.raises(
        CalledProcessError,
        match=r"Command '\['git', 'remote', 'get-url', 'origin'\]' returned non-zero.*",
    ):
        repo.origin_url()


@pytest.mark.parametrize(
    "url, expected",
    [
        # SSH
        ("git@github.com:foo/bar.git", ("git+ssh", "git@github.com", "foo/bar.git")),
        ("git@gitlab.com:foo/bar.git", ("git+ssh", "git@gitlab.com", "foo/bar.git")),
        (
            "git@bitbucket.org:foo/bar.git",
            ("git+ssh", "git@bitbucket.org", "foo/bar.git"),
        ),
        # HTTPS
        (
            "https://github.com/foo/bar.git",
            ("git+https", "git@github.com", "foo/bar.git"),
        ),
        (
            "https://gitlab.com/foo/bar.git",
            ("git+https", "git@gitlab.com", "foo/bar.git"),
        ),
        (
            "https://foo@bitbucket.org/foo/bar.git",
            ("git+https", "git@bitbucket.org", "foo/bar.git"),
        ),
    ],
)
def test_parse_url(url, expected):
    base_dir = Path(".")
    repo = Repository(base_dir=base_dir)
    actual = repo.parse_url(url=url)
    assert actual == expected
