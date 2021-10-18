import subprocess
import urllib.parse
from pathlib import Path


class Repository(object):
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    def head_revision(self) -> str:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.base_dir,
            check=True,
            encoding="utf-8",
            capture_output=True,
        )
        return str(completed.stdout).strip()

    def origin_url(self, pip_style: bool = True) -> str:
        completed = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=self.base_dir,
            check=True,
            encoding="utf-8",
            capture_output=True,
        )
        url = str(completed.stdout).strip()
        if pip_style:
            scheme, host, repo = self.parse_url(url)
            return f"{scheme}://{host}/{repo}"
        return url

    @staticmethod
    def parse_url(url: str) -> tuple[str, str]:
        parsed = urllib.parse.urlparse(url)
        if url.startswith("git@"):
            host, repo = parsed.path.split(":")
            scheme = "git+ssh"
        else:
            if "@" in parsed.netloc:
                host = f"git@{parsed.netloc.split('@')[1]}"
            else:
                host = f"git@{parsed.netloc}"
            repo = parsed.path.lstrip("/")
            scheme = f"git+{parsed.scheme}"
        return scheme, host, repo
