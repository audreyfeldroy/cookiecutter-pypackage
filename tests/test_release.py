"""Tests for the release script's changelog lifecycle."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "release.py"
TEMPLATE_SCRIPT_PATH = Path(__file__).parents[1] / "{{cookiecutter.package_name}}" / "scripts" / "release.py"


def load_release_script():
    """Load the outer release script without executing its CLI entry point."""
    spec = importlib.util.spec_from_file_location("release_script", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def release(tmp_path, monkeypatch):
    """Load the release script in an isolated project directory."""
    (tmp_path / "CHANGELOG").mkdir()
    monkeypatch.chdir(tmp_path)
    return load_release_script()


def write_pyproject(tmp_path, *, name="example-package", version="1.2.3"):
    """Write the minimal project metadata read by the release script."""
    (tmp_path / "pyproject.toml").write_text(
        f'[project]\nname = "{name}"\nversion = "{version}"\n',
        encoding="utf-8",
    )


def allow_release_branch(monkeypatch, release):
    """Skip branch verification when a test targets a later release stage."""
    monkeypatch.setattr(release, "_ensure_release_branch", lambda: None)


def test_unreleased_notes_are_finalized_before_tagging(release, tmp_path, monkeypatch):
    """A release notes commit is pushed before the release tag is created."""
    write_pyproject(tmp_path)
    (tmp_path / "CHANGELOG" / "unreleased.md").write_text(
        "# Unreleased\n\n## Added\n\n- A feature.\n",
        encoding="utf-8",
    )
    commands = []
    monkeypatch.setattr(release, "_ensure_clean_worktree", lambda: None)
    allow_release_branch(monkeypatch, release)
    monkeypatch.setattr(release, "_ensure_tag_state", lambda tag: release.TagState(False, False))
    monkeypatch.setattr(release, "_github_release_exists", lambda tag: False)
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release.main() == 0

    changelog = tmp_path / "CHANGELOG"
    assert (changelog / "1.2.3.md").read_text(encoding="utf-8").startswith("# example-package 1.2.3\n")
    assert (changelog / "unreleased.md").read_text(encoding="utf-8") == (release.UNRELEASED_TEMPLATE)
    commit_index = commands.index(("git", "commit", "-m", "Prepare release notes for v1.2.3"))
    tag_index = commands.index(("git", "tag", "-a", "v1.2.3", "-m", "Release v1.2.3"))
    assert commit_index < tag_index
    assert commands[commit_index + 1] == ("git", "push", "origin", "HEAD:main")


def test_legacy_versioned_notes_are_used_without_a_notes_commit(release, tmp_path, monkeypatch):
    """Older generated projects with versioned notes remain supported."""
    write_pyproject(tmp_path)
    notes_path = tmp_path / "CHANGELOG" / "1.2.3.md"
    notes_path.write_text("# example-package 1.2.3\n\n- Existing notes.\n", encoding="utf-8")
    commands = []
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release._prepare_release_notes("example-package", "1.2.3") == Path("CHANGELOG/1.2.3.md")
    assert commands == []


def test_notes_push_failure_leaves_retryable_state(release, tmp_path, monkeypatch):
    """A failed notes push can be retried without recreating the commit."""
    write_pyproject(tmp_path)
    unreleased = tmp_path / "CHANGELOG" / "unreleased.md"
    unreleased.write_text("# Unreleased\n\n## Added\n\n- A feature.\n", encoding="utf-8")
    commands = []

    def fail_push(*command):
        commands.append(command)
        if command == ("git", "push", "origin", "HEAD:main"):
            raise release.subprocess.CalledProcessError(1, command)

    monkeypatch.setattr(release, "_ensure_clean_worktree", lambda: None)
    allow_release_branch(monkeypatch, release)
    monkeypatch.setattr(release, "_ensure_tag_state", lambda tag: release.TagState(False, False))
    monkeypatch.setattr(release, "_github_release_exists", lambda tag: False)
    monkeypatch.setattr(release, "_run", fail_push)

    assert release.main() == 1

    assert (tmp_path / "CHANGELOG" / "1.2.3.md").exists()
    assert unreleased.read_text(encoding="utf-8") == release.UNRELEASED_TEMPLATE

    retry_commands = []
    monkeypatch.setattr(release, "_run", lambda *command: retry_commands.append(command))
    assert release.main() == 0
    assert retry_commands[0] == ("git", "push", "origin", "HEAD:main")
    assert not any(command[:2] == ("git", "commit") for command in retry_commands)


def test_prepared_changelog_pair_is_retryable(release, tmp_path, monkeypatch):
    """A notes commit that was not pushed can be resumed without duplication."""
    write_pyproject(tmp_path)
    (tmp_path / "CHANGELOG" / "1.2.3.md").write_text("# example-package 1.2.3\n\n- Existing notes.\n", encoding="utf-8")
    (tmp_path / "CHANGELOG" / "unreleased.md").write_text(release.UNRELEASED_TEMPLATE, encoding="utf-8")
    commands = []
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release._prepare_release_notes("example-package", "1.2.3") == Path("CHANGELOG/1.2.3.md")
    assert commands == []


def test_local_tag_retry_pushes_without_retagging(release, tmp_path, monkeypatch):
    """A failed tag push can resume from the validated local tag."""
    write_pyproject(tmp_path)
    (tmp_path / "CHANGELOG" / "1.2.3.md").write_text("# example-package 1.2.3\n\n- Existing notes.\n", encoding="utf-8")
    commands = []
    monkeypatch.setattr(release, "_ensure_clean_worktree", lambda: None)
    allow_release_branch(monkeypatch, release)
    monkeypatch.setattr(release, "_ensure_tag_state", lambda tag: release.TagState(True, False))
    monkeypatch.setattr(release, "_github_release_exists", lambda tag: False)
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release.main() == 0
    assert ("git", "push", "origin", "HEAD:main") in commands
    assert not any(command[:2] == ("git", "tag") for command in commands)
    assert ("git", "push", "origin", "v1.2.3") in commands
    assert any(command[:3] == ("gh", "release", "create") for command in commands)


def test_existing_github_release_skips_republish(release, tmp_path, monkeypatch):
    """A retry does not recreate a GitHub Release that already exists."""
    write_pyproject(tmp_path)
    (tmp_path / "CHANGELOG" / "1.2.3.md").write_text("# example-package 1.2.3\n\n- Existing notes.\n", encoding="utf-8")
    commands = []
    monkeypatch.setattr(release, "_ensure_clean_worktree", lambda: None)
    allow_release_branch(monkeypatch, release)
    monkeypatch.setattr(release, "_ensure_tag_state", lambda tag: release.TagState(True, True))
    monkeypatch.setattr(release, "_github_release_exists", lambda tag: True)
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release.main() == 0
    assert commands == [("git", "push", "origin", "HEAD:main")]


def test_legacy_notes_push_main_before_tagging(release, tmp_path, monkeypatch):
    """Legacy notes still synchronize main before creating the release tag."""
    write_pyproject(tmp_path)
    (tmp_path / "CHANGELOG" / "1.2.3.md").write_text("# example-package 1.2.3\n\n- Existing notes.\n", encoding="utf-8")
    commands = []
    monkeypatch.setattr(release, "_ensure_clean_worktree", lambda: None)
    allow_release_branch(monkeypatch, release)
    monkeypatch.setattr(release, "_ensure_tag_state", lambda tag: release.TagState(False, False))
    monkeypatch.setattr(release, "_github_release_exists", lambda tag: False)
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release.main() == 0

    assert commands.index(("git", "push", "origin", "HEAD:main")) < commands.index(
        ("git", "tag", "-a", "v1.2.3", "-m", "Release v1.2.3")
    )


@pytest.mark.parametrize(
    ("tag_state", "failed_command"),
    [
        ("local_only", ("git", "push", "origin", "v1.2.3")),
        (
            "published_tag",
            (
                "gh",
                "release",
                "create",
                "v1.2.3",
                "--verify-tag",
                "--title",
                "Release",
                "--notes",
                "Notes",
            ),
        ),
    ],
)
def test_publish_failures_abort_without_reporting_success(release, tmp_path, monkeypatch, tag_state, failed_command):
    """Tag and GitHub publish failures return a failed release result."""
    write_pyproject(tmp_path)
    (tmp_path / "CHANGELOG" / "1.2.3.md").write_text("# Release\n\nNotes\n", encoding="utf-8")
    states = {
        "local_only": release.TagState(True, False),
        "published_tag": release.TagState(True, True),
    }
    monkeypatch.setattr(release, "_ensure_clean_worktree", lambda: None)
    allow_release_branch(monkeypatch, release)
    monkeypatch.setattr(release, "_ensure_tag_state", lambda tag: states[tag_state])
    monkeypatch.setattr(release, "_github_release_exists", lambda tag: False)

    def fail_command(*command):
        if command == failed_command:
            raise release.subprocess.CalledProcessError(1, command)

    monkeypatch.setattr(release, "_run", fail_command)

    assert release.main() == 1


def test_github_release_lookup_failure_is_reported(release, monkeypatch):
    """Unexpected GitHub lookup errors do not look like a missing release."""
    monkeypatch.setattr(
        release,
        "_command_result",
        lambda *command: release.subprocess.CompletedProcess(command, 1, stdout="", stderr="permission denied"),
    )

    with pytest.raises(release.ReleaseError, match="permission denied"):
        release._github_release_exists("v1.2.3")


def test_main_reports_unexpected_os_error(release, tmp_path, monkeypatch):
    """The CLI converts unexpected executable errors into a failed result."""
    write_pyproject(tmp_path)
    monkeypatch.setattr(release, "_ensure_clean_worktree", lambda: None)
    allow_release_branch(monkeypatch, release)
    monkeypatch.setattr(release, "_push_release_branch", lambda: None)
    monkeypatch.setattr(release, "_ensure_tag_state", lambda tag: release.TagState(True, True))
    monkeypatch.setattr(
        release,
        "_prepare_release_notes",
        lambda name, version: Path("CHANGELOG/1.2.3.md"),
    )
    monkeypatch.setattr(release, "_release_notes", lambda *args: ("Release", "Notes"))
    monkeypatch.setattr(
        release,
        "_github_release_exists",
        lambda tag: (_ for _ in ()).throw(OSError("gh unavailable")),
    )

    assert release.main() == 1


def test_non_main_branch_aborts_before_release_mutation(release, tmp_path, monkeypatch):
    """A release cannot publish a feature branch by accident."""
    write_pyproject(tmp_path)
    unreleased = tmp_path / "CHANGELOG" / "unreleased.md"
    unreleased.write_text("# Unreleased\n\n- A feature.\n", encoding="utf-8")
    commands = []
    monkeypatch.setattr(release, "_ensure_clean_worktree", lambda: None)

    def fake_command_result(*command):
        if command == ("git", "branch", "--show-current"):
            return release.subprocess.CompletedProcess(command, 0, stdout="feature\n")
        raise AssertionError(f"Unexpected command: {command}")

    monkeypatch.setattr(release, "_command_result", fake_command_result)
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release.main() == 1
    assert commands == []
    assert unreleased.exists()
    assert not (tmp_path / "CHANGELOG" / "1.2.3.md").exists()


def test_diverged_main_aborts_before_release_mutation(release, tmp_path, monkeypatch):
    """A local main that differs from origin/main cannot be released."""
    write_pyproject(tmp_path)
    commands = []
    monkeypatch.setattr(release, "_ensure_clean_worktree", lambda: None)

    def fake_command_result(*command):
        if command == ("git", "branch", "--show-current"):
            return release.subprocess.CompletedProcess(command, 0, stdout="main\n")
        if command == ("git", "rev-parse", "HEAD"):
            return release.subprocess.CompletedProcess(command, 0, stdout="local\n")
        if command[:2] == ("git", "ls-remote"):
            return release.subprocess.CompletedProcess(command, 0, stdout="remote\trefs/heads/main\n")
        raise AssertionError(f"Unexpected command: {command}")

    monkeypatch.setattr(release, "_command_result", fake_command_result)
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release.main() == 1
    assert commands == []


def test_remote_tag_is_fetched_and_verified(release, monkeypatch):
    """A remote-only tag is fetched before the release is resumed."""
    commands = []
    show_ref_calls = 0

    def fake_command_result(*command):
        nonlocal show_ref_calls
        if command[:2] == ("git", "show-ref"):
            show_ref_calls += 1
            return release.subprocess.CompletedProcess(command, 1 if show_ref_calls == 1 else 0)
        if command[:3] == ("git", "ls-remote", "--exit-code"):
            return release.subprocess.CompletedProcess(command, 0, stdout="same\trefs/tags/v1.2.3\n")
        if command[:2] == ("git", "rev-list"):
            return release.subprocess.CompletedProcess(command, 0, stdout="same\n")
        if command[:2] == ("git", "rev-parse"):
            return release.subprocess.CompletedProcess(command, 0, stdout="same\n")
        raise AssertionError(f"Unexpected command: {command}")

    monkeypatch.setattr(release, "_command_result", fake_command_result)
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release._ensure_tag_state("v1.2.3") == release.TagState(True, True)
    assert commands == [("git", "fetch", "origin", "tag", "v1.2.3")]


def test_pre_release_tag_does_not_block_a_new_final_tag(release, monkeypatch):
    """Only exact remote tag refs affect the current release tag state."""

    def fake_command_result(*command):
        if command[:2] == ("git", "show-ref"):
            return release.subprocess.CompletedProcess(command, 1)
        if command[:3] == ("git", "ls-remote", "--exit-code"):
            assert command[-2:] == ("refs/tags/v1.2.3", "refs/tags/v1.2.3^{}")
            return release.subprocess.CompletedProcess(command, 0, stdout="pre-release\trefs/tags/v1.2.3rc1\n")
        raise AssertionError(f"Unexpected command: {command}")

    monkeypatch.setattr(release, "_command_result", fake_command_result)

    assert release._ensure_tag_state("v1.2.3") == release.TagState(False, False)


def test_tag_on_another_commit_is_rejected(release, monkeypatch):
    """A tag pointing elsewhere cannot be reused for the current release."""

    def fake_command_result(*command):
        if command[:2] == ("git", "show-ref"):
            return release.subprocess.CompletedProcess(command, 0)
        if command[:3] == ("git", "ls-remote", "--exit-code"):
            return release.subprocess.CompletedProcess(command, 0, stdout="tag\trefs/tags/v1.2.3\n")
        if command[:2] == ("git", "rev-list"):
            return release.subprocess.CompletedProcess(command, 0, stdout="tag\n")
        if command[:2] == ("git", "rev-parse"):
            return release.subprocess.CompletedProcess(command, 0, stdout="head\n")
        raise AssertionError(f"Unexpected command: {command}")

    monkeypatch.setattr(release, "_command_result", fake_command_result)

    with pytest.raises(release.ReleaseError, match="does not point to the current HEAD"):
        release._ensure_tag_state("v1.2.3")


def test_remote_tag_on_another_commit_is_rejected(release, monkeypatch):
    """A remote tag that differs from the local tag cannot be reused."""

    def fake_command_result(*command):
        if command[:2] == ("git", "show-ref"):
            return release.subprocess.CompletedProcess(command, 0)
        if command[:3] == ("git", "ls-remote", "--exit-code"):
            return release.subprocess.CompletedProcess(command, 0, stdout="remote\trefs/tags/v1.2.3\n")
        if command[:2] == ("git", "rev-list"):
            return release.subprocess.CompletedProcess(command, 0, stdout="local\n")
        if command[:2] == ("git", "rev-parse"):
            return release.subprocess.CompletedProcess(command, 0, stdout="local\n")
        raise AssertionError(f"Unexpected command: {command}")

    monkeypatch.setattr(release, "_command_result", fake_command_result)

    with pytest.raises(release.ReleaseError, match="differs between local and origin"):
        release._ensure_tag_state("v1.2.3")


def test_missing_executable_returns_a_readable_command_error(release, monkeypatch):
    """Missing tools are represented as command failures instead of crashing."""

    def missing_executable(*command, **kwargs):
        raise FileNotFoundError("gh")

    monkeypatch.setattr(release.subprocess, "run", missing_executable)

    result = release._command_result("gh", "release", "view", "v1.2.3")

    assert result.returncode == 127
    assert result.stderr == "gh"


@pytest.mark.parametrize(
    ("versioned", "unreleased"),
    [(True, True), (False, False)],
)
def test_invalid_changelog_states_abort_before_writing(release, tmp_path, monkeypatch, versioned, unreleased):
    """Ambiguous or missing release notes fail without invoking Git."""
    write_pyproject(tmp_path)
    changelog = tmp_path / "CHANGELOG"
    if versioned:
        (changelog / "1.2.3.md").write_text("# Existing\n", encoding="utf-8")
    if unreleased:
        (changelog / "unreleased.md").write_text("# Unreleased\n\n- Draft notes.\n", encoding="utf-8")
    commands = []
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))
    with pytest.raises(release.ReleaseError):
        release._prepare_release_notes("example-package", "1.2.3")
    assert commands == []


def test_empty_unreleased_notes_abort_before_writing(release, tmp_path, monkeypatch):
    """A placeholder changelog cannot accidentally create an empty release."""
    write_pyproject(tmp_path)
    changelog = tmp_path / "CHANGELOG"
    (changelog / "unreleased.md").write_text(release.UNRELEASED_TEMPLATE, encoding="utf-8")
    commands = []
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    with pytest.raises(release.ReleaseError):
        release._prepare_release_notes("example-package", "1.2.3")
    assert commands == []


def test_empty_legacy_notes_abort_before_writing(release, tmp_path, monkeypatch):
    """A legacy versioned file must still contain actual release notes."""
    write_pyproject(tmp_path)
    (tmp_path / "CHANGELOG" / "1.2.3.md").write_text("# example-package 1.2.3\n", encoding="utf-8")
    commands = []
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    with pytest.raises(release.ReleaseError):
        release._prepare_release_notes("example-package", "1.2.3")
    assert commands == []


def test_dirty_worktree_aborts_before_release_commands(release, monkeypatch):
    """A dirty worktree stops the release before any write command runs."""
    commands = []
    monkeypatch.setattr(
        release,
        "_command_result",
        lambda *command: release.subprocess.CompletedProcess(command, 0, stdout=" M pyproject.toml\n", stderr=""),
    )
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    with pytest.raises(release.ReleaseError):
        release._ensure_clean_worktree()
    assert commands == []


def test_outer_and_generated_release_scripts_stay_aligned():
    """The generated release workflow must match the outer workflow exactly."""
    assert SCRIPT_PATH.read_text(encoding="utf-8") == TEMPLATE_SCRIPT_PATH.read_text(encoding="utf-8")
