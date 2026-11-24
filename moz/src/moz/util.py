import sys
from pathlib import Path


def find_git_repo() -> Path:
    path = Path(".").absolute()

    while not (path / ".git").exists():
        path = path.parent
        if path == Path("/"):
            print("error: could not find Git repository")
            sys.exit(1)

    return path
