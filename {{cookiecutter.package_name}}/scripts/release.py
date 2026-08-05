# /// script
# requires-python = ">=3.10"
# ///
"""Finalize release notes, tag the current version, and create a GitHub release."""

import subprocess
import tomllib
from pathlib import Path

CHANGELOG_DIR = Path("CHANGELOG")
UNRELEASED_PATH = CHANGELOG_DIR / "unreleased.md"
UNRELEASED_TEMPLATE = "# Unreleased\n\nRecord user-visible changes here before the next release.\n"


class ReleaseError(RuntimeError):
    """Raised when release preconditions are not satisfied."""


def _run(*cmd: str) -> None:
    print(f"$ {' '.join(cmd)}")  # noqa: T201
    subprocess.run(cmd, check=True)


def _command_result(*cmd: str) -> subprocess.CompletedProcess[str]:
    """Run a read-only command and return its result without raising."""
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def _ensure_clean_worktree() -> None:
    """Require all release preparation work to be committed already."""
    result = _command_result("git", "status", "--porcelain")
    if result.returncode != 0:
        error = (result.stderr or result.stdout).strip() or "unknown error"
        raise ReleaseError(f"Could not inspect the Git worktree: {error}")
    if result.stdout.strip():
        raise ReleaseError("Git worktree is not clean; commit or stash changes first.")


def _ensure_tag_available(tag: str) -> None:
    """Reject releases whose tag already exists locally or on origin."""
    local = _command_result("git", "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}")
    if local.returncode == 0:
        raise ReleaseError(f"Git tag {tag} already exists locally.")

    remote = _command_result("git", "ls-remote", "--exit-code", "--tags", "origin", f"refs/tags/{tag}")
    if remote.returncode == 0:
        raise ReleaseError(f"Git tag {tag} already exists on origin.")
    if remote.returncode != 2:
        error = (remote.stderr or remote.stdout).strip() or "unknown error"
        raise ReleaseError(f"Could not check whether {tag} exists on origin: {error}")


def _has_release_notes(contents: str) -> bool:
    """Return whether unreleased.md contains notes rather than only its template."""
    lines = [line.strip() for line in contents.splitlines() if line.strip()]
    normalized = "\n".join(lines).lower()
    template_lines = [line.strip() for line in UNRELEASED_TEMPLATE.splitlines() if line.strip()]
    template = "\n".join(template_lines).lower()
    return len(lines) > 1 and normalized != template


def _finalized_contents(contents: str, name: str, version: str) -> str:
    """Turn the unreleased heading into a versioned release heading."""
    lines = contents.splitlines(keepends=True)
    title = f"# {name} {version}\n"
    if lines and lines[0].strip().lower() == "# unreleased":
        lines[0] = title
        return "".join(lines)
    return f"{title}\n{contents.lstrip()}"


def _prepare_release_notes(name: str, version: str) -> Path:
    """Finalize unreleased notes, preserving compatibility with older projects."""
    versioned_path = CHANGELOG_DIR / f"{version}.md"
    if versioned_path.exists() and UNRELEASED_PATH.exists():
        raise ReleaseError("Both release changelog files exist; resolve the state manually.")
    if versioned_path.exists():
        if not _has_release_notes(versioned_path.read_text(encoding="utf-8")):
            raise ReleaseError(f"{versioned_path} does not contain release notes.")
        return versioned_path
    if not UNRELEASED_PATH.exists():
        raise ReleaseError("No release changelog exists; add release notes first.")

    contents = UNRELEASED_PATH.read_text(encoding="utf-8")
    if not _has_release_notes(contents):
        raise ReleaseError(f"{UNRELEASED_PATH} does not contain release notes.")

    versioned_path.parent.mkdir(parents=True, exist_ok=True)
    UNRELEASED_PATH.rename(versioned_path)
    versioned_path.write_text(
        _finalized_contents(contents, name, version),
        encoding="utf-8",
    )
    UNRELEASED_PATH.write_text(UNRELEASED_TEMPLATE, encoding="utf-8")
    _run("git", "add", str(versioned_path), str(UNRELEASED_PATH))
    _run("git", "commit", "-m", f"Prepare release notes for v{version}")
    _run("git", "push", "origin", "HEAD")
    return versioned_path


def _release_notes(notes_path: Path, name: str, version: str) -> tuple[str, str]:
    """Read the GitHub Release title and body from a versioned notes file."""
    lines = notes_path.read_text(encoding="utf-8").splitlines(keepends=True)
    title = f"{name} {version}"
    if lines and lines[0].startswith("# "):
        title = lines[0].lstrip("# ").strip()
        lines = lines[1:]
        if lines and not lines[0].strip():
            lines = lines[1:]
    return title, "".join(lines).rstrip()


def main() -> int:
    """Run all release preflight checks and publish the release."""
    try:
        pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
        name = pyproject["project"]["name"]
        version = pyproject["project"]["version"]
        tag = f"v{version}"

        _ensure_clean_worktree()
        _ensure_tag_available(tag)
        notes_path = _prepare_release_notes(name, version)
        title, notes = _release_notes(notes_path, name, version)

        _run("git", "tag", "-a", tag, "-m", f"Release {tag}")
        _run("git", "push", "origin", tag)
        _run(
            "gh",
            "release",
            "create",
            tag,
            "--verify-tag",
            "--title",
            title,
            "--notes",
            notes,
        )
    except ReleaseError as error:
        print(f"Release aborted: {error}")  # noqa: T201
        return 1
    except subprocess.CalledProcessError as error:
        print(f"Release command failed: {error}")  # noqa: T201
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
