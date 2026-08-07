# /// script
# requires-python = ">=3.10"
# ///
"""Finalize release notes, tag the current version, and create a GitHub release."""

import subprocess
import tomllib
from pathlib import Path
from typing import NamedTuple

CHANGELOG_DIR = Path("CHANGELOG")
UNRELEASED_PATH = CHANGELOG_DIR / "unreleased.md"
RELEASE_BRANCH = "main"
UNRELEASED_TEMPLATE = "# Unreleased\n\nRecord user-visible changes here before the next release.\n"


class ReleaseError(RuntimeError):
    """Raised when release preconditions are not satisfied."""


class TagState(NamedTuple):
    """Whether the release tag exists locally and on the remote."""

    local: bool
    remote: bool


def _run(*cmd: str) -> None:
    print(f"$ {' '.join(cmd)}")  # noqa: T201
    try:
        subprocess.run(cmd, check=True)
    except OSError as error:
        raise ReleaseError(f"Could not run {' '.join(cmd)}: {error}") from error


def _command_result(*cmd: str) -> subprocess.CompletedProcess[str]:
    """Run a read-only command and return its result without raising."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=False)
    except OSError as error:
        return subprocess.CompletedProcess(cmd, 127, stdout="", stderr=str(error))


def _ensure_clean_worktree() -> None:
    """Require all release preparation work to be committed already."""
    result = _command_result("git", "status", "--porcelain")
    if result.returncode != 0:
        error = (result.stderr or result.stdout).strip() or "unknown error"
        raise ReleaseError(f"Could not inspect the Git worktree: {error}")
    if result.stdout.strip():
        raise ReleaseError("Git worktree is not clean; commit or stash changes first.")


def _ensure_release_branch() -> None:
    """Require HEAD to be the current commit on the protected release branch."""
    branch = _command_result("git", "branch", "--show-current")
    if branch.returncode != 0:
        error = (branch.stderr or branch.stdout).strip() or "unknown error"
        raise ReleaseError(f"Could not inspect the current Git branch: {error}")
    if branch.stdout.strip() != RELEASE_BRANCH:
        raise ReleaseError(f"Releases must run from the {RELEASE_BRANCH} branch.")

    head = _command_result("git", "rev-parse", "HEAD")
    remote = _command_result("git", "ls-remote", "--exit-code", "origin", f"refs/heads/{RELEASE_BRANCH}")
    if head.returncode != 0 or remote.returncode not in {0, 2}:
        error = (head.stderr or remote.stderr or head.stdout or remote.stdout).strip()
        raise ReleaseError(f"Could not verify that {RELEASE_BRANCH} matches origin: {error or 'unknown error'}")
    remote_lines = [line.split("\t", 1) for line in remote.stdout.splitlines() if "\t" in line]
    remote_refs = {ref: commit for commit, ref in remote_lines}
    remote_commit = remote_refs.get(f"refs/heads/{RELEASE_BRANCH}")
    if remote_commit is None:
        raise ReleaseError(f"origin does not have a {RELEASE_BRANCH} branch.")
    if head.stdout.strip() != remote_commit:
        raise ReleaseError(f"{RELEASE_BRANCH} must match origin/{RELEASE_BRANCH} before release.")


def _push_release_branch() -> None:
    """Push prepared release work and re-verify the protected branch."""
    _run("git", "push", "origin", f"HEAD:{RELEASE_BRANCH}")
    _ensure_release_branch()


def _ensure_tag_state(tag: str) -> TagState:
    """Validate an existing tag so interrupted releases can be resumed safely."""
    local = _command_result("git", "show-ref", "--verify", "--quiet", f"refs/tags/{tag}")
    if local.returncode not in {0, 1}:
        error = (local.stderr or local.stdout).strip() or "unknown error"
        raise ReleaseError(f"Could not check local tag {tag}: {error}")
    local_exists = local.returncode == 0

    remote = _command_result(
        "git", "ls-remote", "--exit-code", "--tags", "origin", f"refs/tags/{tag}", f"refs/tags/{tag}^" + "{}"
    )
    if remote.returncode not in {0, 2}:
        error = (remote.stderr or remote.stdout).strip() or "unknown error"
        raise ReleaseError(f"Could not check whether {tag} exists on origin: {error}")
    remote_lines = [line.split("\t", 1) for line in remote.stdout.splitlines() if "\t" in line]
    remote_refs = {ref: commit for commit, ref in remote_lines}
    remote_tag_ref = f"refs/tags/{tag}"
    remote_commit = remote_refs.get(remote_tag_ref + "^{}") or remote_refs.get(remote_tag_ref)
    remote_exists = remote_commit is not None

    if remote_exists and not local_exists:
        _run("git", "fetch", "origin", "tag", tag)
        local = _command_result("git", "show-ref", "--verify", "--quiet", f"refs/tags/{tag}")
        if local.returncode != 0:
            raise ReleaseError(f"Could not fetch tag {tag} from origin.")
        local_exists = True

    if local_exists:
        tag_commit = _command_result("git", "rev-list", "-n", "1", f"refs/tags/{tag}^" + "{commit}")
        head_commit = _command_result("git", "rev-parse", "HEAD")
        if tag_commit.returncode != 0 or head_commit.returncode != 0:
            raise ReleaseError(f"Could not verify that tag {tag} points to HEAD.")
        local_commit = tag_commit.stdout.strip()
        if remote_commit and remote_commit != local_commit:
            raise ReleaseError(f"Git tag {tag} differs between local and origin.")
        if local_commit != head_commit.stdout.strip():
            raise ReleaseError(f"Git tag {tag} does not point to the current HEAD.")

    return TagState(local_exists, remote_exists)


def _github_release_exists(tag: str) -> bool:
    """Return whether GitHub already has a release for the tag."""
    result = _command_result("gh", "release", "view", tag)
    if result.returncode == 0:
        return True
    error = (result.stderr or result.stdout).strip() or "unknown error"
    if "not found" in error.lower():
        return False
    raise ReleaseError(f"Could not check whether GitHub release {tag} exists: {error}")


def _has_release_notes(contents: str) -> bool:
    """Return whether unreleased.md contains notes rather than only its template."""
    lines = [line.strip() for line in contents.splitlines() if line.strip()]
    normalized = "\n".join(lines).lower()
    template_lines = [line.strip() for line in UNRELEASED_TEMPLATE.splitlines() if line.strip()]
    template = "\n".join(template_lines).lower()
    return len(lines) > 1 and normalized != template


def _is_unreleased_template(contents: str) -> bool:
    """Return whether unreleased.md is the fresh placeholder created by release."""
    lines = [line.strip() for line in contents.splitlines() if line.strip()]
    template_lines = [line.strip() for line in UNRELEASED_TEMPLATE.splitlines() if line.strip()]
    return lines == template_lines


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
        versioned_contents = versioned_path.read_text(encoding="utf-8")
        unreleased_contents = UNRELEASED_PATH.read_text(encoding="utf-8")
        if _has_release_notes(versioned_contents) and _is_unreleased_template(unreleased_contents):
            return versioned_path
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
        _ensure_release_branch()
        _ensure_tag_state(tag)
        notes_path = _prepare_release_notes(name, version)
        _push_release_branch()
        title, notes = _release_notes(notes_path, name, version)

        tag_state = _ensure_tag_state(tag)
        if not tag_state.local:
            _run("git", "tag", "-a", tag, "-m", f"Release {tag}")
        if not tag_state.remote:
            _run("git", "push", "origin", tag)
        if not _github_release_exists(tag):
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
    except OSError as error:
        print(f"Release command failed: {error}")  # noqa: T201
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
