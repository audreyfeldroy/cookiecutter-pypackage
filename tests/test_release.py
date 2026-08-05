"""Tests for the release script's changelog lifecycle."""

import ast
import importlib.util
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "release.py"
TEMPLATE_SCRIPT_PATH = (
    Path(__file__).parents[1]
    / "{{cookiecutter.package_name}}"
    / "scripts"
    / "release.py"
)


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


def test_unreleased_notes_are_finalized_before_tagging(release, tmp_path, monkeypatch):
    """A release notes commit is pushed before the release tag is created."""
    write_pyproject(tmp_path)
    (tmp_path / "CHANGELOG" / "unreleased.md").write_text(
        "# Unreleased\n\n## Added\n\n- A feature.\n",
        encoding="utf-8",
    )
    commands = []
    monkeypatch.setattr(release, "_ensure_clean_worktree", lambda: None)
    monkeypatch.setattr(release, "_ensure_tag_available", lambda tag: None)
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release.main() == 0

    changelog = tmp_path / "CHANGELOG"
    assert (
        (changelog / "1.2.3.md")
        .read_text(encoding="utf-8")
        .startswith("# example-package 1.2.3\n")
    )
    assert (changelog / "unreleased.md").read_text(encoding="utf-8") == (
        release.UNRELEASED_TEMPLATE
    )
    commit_index = commands.index(
        ("git", "commit", "-m", "Prepare release notes for v1.2.3")
    )
    tag_index = commands.index(("git", "tag", "-a", "v1.2.3", "-m", "Release v1.2.3"))
    assert commit_index < tag_index
    assert commands[commit_index + 1] == ("git", "push", "origin", "HEAD")


def test_legacy_versioned_notes_are_used_without_a_notes_commit(
    release, tmp_path, monkeypatch
):
    """Older generated projects with versioned notes remain supported."""
    write_pyproject(tmp_path)
    notes_path = tmp_path / "CHANGELOG" / "1.2.3.md"
    notes_path.write_text(
        "# example-package 1.2.3\n\n- Existing notes.\n", encoding="utf-8"
    )
    commands = []
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    assert release._prepare_release_notes("example-package", "1.2.3") == Path(
        "CHANGELOG/1.2.3.md"
    )
    assert commands == []


@pytest.mark.parametrize(
    ("versioned", "unreleased"),
    [(True, True), (False, False)],
)
def test_invalid_changelog_states_abort_before_writing(
    release, tmp_path, monkeypatch, versioned, unreleased
):
    """Ambiguous or missing release notes fail without invoking Git."""
    write_pyproject(tmp_path)
    changelog = tmp_path / "CHANGELOG"
    if versioned:
        (changelog / "1.2.3.md").write_text("# Existing\n", encoding="utf-8")
    if unreleased:
        (changelog / "unreleased.md").write_text(
            "# Unreleased\n\n- Draft notes.\n", encoding="utf-8"
        )
    commands = []
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))
    with pytest.raises(release.ReleaseError):
        release._prepare_release_notes("example-package", "1.2.3")
    assert commands == []


def test_empty_unreleased_notes_abort_before_writing(release, tmp_path, monkeypatch):
    """A placeholder changelog cannot accidentally create an empty release."""
    write_pyproject(tmp_path)
    changelog = tmp_path / "CHANGELOG"
    (changelog / "unreleased.md").write_text(
        release.UNRELEASED_TEMPLATE, encoding="utf-8"
    )
    commands = []
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    with pytest.raises(release.ReleaseError):
        release._prepare_release_notes("example-package", "1.2.3")
    assert commands == []


def test_empty_legacy_notes_abort_before_writing(release, tmp_path, monkeypatch):
    """A legacy versioned file must still contain actual release notes."""
    write_pyproject(tmp_path)
    (tmp_path / "CHANGELOG" / "1.2.3.md").write_text(
        "# example-package 1.2.3\n", encoding="utf-8"
    )
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
        lambda *command: release.subprocess.CompletedProcess(
            command, 0, stdout=" M pyproject.toml\n", stderr=""
        ),
    )
    monkeypatch.setattr(release, "_run", lambda *command: commands.append(command))

    with pytest.raises(release.ReleaseError):
        release._ensure_clean_worktree()
    assert commands == []


def test_outer_and_generated_release_scripts_stay_functionally_aligned():
    """The generated release workflow must match the outer workflow's behavior."""
    outer_tree = ast.parse(SCRIPT_PATH.read_text(encoding="utf-8"))
    template_tree = ast.parse(TEMPLATE_SCRIPT_PATH.read_text(encoding="utf-8"))
    assert ast.dump(outer_tree) == ast.dump(template_tree)
