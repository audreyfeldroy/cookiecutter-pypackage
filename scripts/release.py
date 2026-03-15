# /// script
# requires-python = ">=3.10"
# ///
"""Tag the current version and create a GitHub release."""

import subprocess
import tomllib
from pathlib import Path


def _run(*cmd: str) -> None:
    print(f"$ {' '.join(cmd)}")  # noqa: T201
    subprocess.run(cmd, check=True)


def main() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    name = pyproject["project"]["name"]
    version = pyproject["project"]["version"]
    tag = f"v{version}"
    notes_path = Path(f"CHANGELOG/{version}.md")

    lines = notes_path.read_text().splitlines(keepends=True)
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        if lines and not lines[0].strip():
            lines = lines[1:]
    notes = "".join(lines).rstrip()

    _run("git", "tag", "-a", tag, "-m", f"Release {tag}")
    _run("git", "push", "origin", tag)
    _run(
        "gh",
        "release",
        "create",
        tag,
        "--verify-tag",
        "--title",
        f"{name} {version}",
        "--notes",
        notes,
    )


if __name__ == "__main__":
    main()
