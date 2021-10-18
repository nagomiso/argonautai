import subprocess
from typing import Any
from pathlib import Path

import yaml


class Kustomize(object):
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    def build(self, overlay: str) -> dict[str, Any]:
        completed = subprocess.run(
            ["kustomize", "build", str(self.base_dir.joinpath(overlay))],
            check=True,
            encoding="utf-8",
            capture_output=True,
        )
        return yaml.safe_load(completed.stdout)
