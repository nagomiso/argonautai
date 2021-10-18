import subprocess

from pathlib import Path
from tempfile import TemporaryDirectory


def current_revision(base_dir: Path) -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=base_dir, check=True)
    return str(result.stdout)
