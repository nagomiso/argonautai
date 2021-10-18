from pathlib import Path
from subprocess import CalledProcessError

import pytest

from argonautai.kustomize import Kustomize


@pytest.fixture
def kustomize_dir(request):
    current_dir = request.fspath.join("..")
    return current_dir.join("kustomize/workflow/overlays")


@pytest.fixture
def not_kustomize_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("not_kustomize")


def test_build_normal(kustomize_dir):
    base_dir = Path(kustomize_dir)
    k = Kustomize(base_dir=base_dir)
    assert isinstance(k.build(overlay="dev"), dict)


def test_build_error(not_kustomize_dir):
    base_dir = Path(not_kustomize_dir)
    k = Kustomize(base_dir=base_dir)
    with pytest.raises(
        CalledProcessError,
        match=(
            r"Command '\['kustomize', 'build', "
            f"'{base_dir / 'dev'}'"
            r"\]' returned non-zero .*"
        ),
    ):
        k.build(overlay="dev")
