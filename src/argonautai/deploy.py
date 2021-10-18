import subprocess
from pathlib import Path


def current_revision(base_dir: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=base_dir,
        check=True,
        encoding="utf-8",
        capture_output=True,
    )
    return str(result.stdout).strip()
