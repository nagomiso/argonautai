import subprocess
from pathlib import Path
from typing import Any

import ruamel.yaml

yaml = ruamel.yaml.YAML(typ="safe")


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
        return yaml.load(completed.stdout)
