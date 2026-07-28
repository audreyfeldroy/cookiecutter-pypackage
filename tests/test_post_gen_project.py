"""Tests for the post-generation GitHub setup flow."""

import importlib.util
import subprocess
from pathlib import Path

import pytest

HOOK_PATH = Path(__file__).parents[1] / "hooks" / "post_gen_project.py"


@pytest.fixture
def hook(monkeypatch):
    """Load the hook as a module with predictable rendered values."""
    spec = importlib.util.spec_from_file_location("post_gen_project_test", HOOK_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "OWNER", "example-owner")
    monkeypatch.setattr(module, "REPO", "example-repo")
    monkeypatch.setattr(module, "DESCRIPTION", "Example project")
    monkeypatch.setattr(module.shutil, "which", lambda _: "/usr/bin/gh")
    return module


def completed(command, returncode=0, *, stdout="", stderr=""):
    """Build a subprocess result for a mocked command."""
    return subprocess.CompletedProcess(
        args=command,
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def test_declining_setup_has_no_git_or_github_side_effects(hook, monkeypatch, capsys):
    """The default answer leaves the generated files entirely local."""
    monkeypatch.setattr(hook.os, "isatty", lambda _: True)
    monkeypatch.setattr("builtins.input", lambda _: "")

    def fail_run_command(*command):
        raise AssertionError(f"Unexpected command: {command}")

    monkeypatch.setattr(hook, "run_command", fail_run_command)
    hook.main()

    output = capsys.readouterr().out
    assert "GitHub setup skipped." in output
    assert "without creating a Git commit" in output


def test_visibility_reprompts_and_defaults_to_private(hook, monkeypatch, capsys):
    """Invalid visibility cannot accidentally create a public repository."""
    answers = iter(["yes", "privte", "", "yes"])
    monkeypatch.setattr(hook.os, "isatty", lambda _: True)
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    commands = []

    def fake_run_command(*command):
        commands.append(command)
        if command[:3] == ("gh", "repo", "view"):
            return completed(
                command,
                returncode=1,
                stderr="Could not resolve to a Repository",
            )
        return completed(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    hook.main()

    create_command = next(
        command for command in commands if command[:3] == ("gh", "repo", "create")
    )
    assert "--private" in create_command
    assert "--public" not in create_command
    assert "Please enter private or public." in capsys.readouterr().out


def test_final_confirmation_cancels_before_any_write(hook, monkeypatch, capsys):
    """The plan remains read-only until the final confirmation."""
    answers = iter(["yes", "", "no"])
    monkeypatch.setattr(hook.os, "isatty", lambda _: True)
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    commands = []

    def fake_run_command(*command):
        commands.append(command)
        if command[:3] == ("gh", "repo", "view"):
            return completed(
                command,
                returncode=1,
                stderr="Could not resolve to a Repository",
            )
        return completed(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    hook.main()

    assert not any(command[:3] == ("gh", "repo", "create") for command in commands)
    assert not any(command[0] == "git" for command in commands)
    assert "No repository or Git commit was created" in capsys.readouterr().out


def test_empty_existing_repository_requires_separate_consent(hook, monkeypatch, capsys):
    """An empty repository is connected only after a second explicit yes."""
    answers = iter(["yes", "yes", "yes"])
    monkeypatch.setattr(hook.os, "isatty", lambda _: True)
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    commands = []

    def fake_run_command(*command):
        commands.append(command)
        if command[:3] == ("gh", "repo", "view"):
            return completed(command, stdout='{"isEmpty": true}')
        return completed(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    hook.main()

    assert not any(command[:3] == ("gh", "repo", "create") for command in commands)
    assert ("git", "push", "-u", "origin", "main") in commands
    output = capsys.readouterr().out
    assert "Using existing empty repository" in output


def test_nonempty_existing_repository_is_never_modified(hook, monkeypatch, capsys):
    """The automatic flow refuses to push to a nonempty repository."""
    answers = iter(["yes"])
    monkeypatch.setattr(hook.os, "isatty", lambda _: True)
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    commands = []

    def fake_run_command(*command):
        commands.append(command)
        if command[:3] == ("gh", "repo", "view"):
            return completed(command, stdout='{"isEmpty": false}')
        return completed(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    hook.main()

    assert not any(command[0] == "git" for command in commands)
    assert not any(command[:3] == ("gh", "repo", "create") for command in commands)
    assert "will not modify it automatically" in capsys.readouterr().out


def test_explicit_public_mode_supports_noninteractive_automation(hook, monkeypatch):
    """The CLI flag itself is sufficient consent during automation."""
    monkeypatch.setenv(hook.GITHUB_SETUP_ENV, "public")
    monkeypatch.setattr(hook.os, "isatty", lambda _: False)
    commands = []

    def fake_run_command(*command):
        commands.append(command)
        if command[:3] == ("gh", "repo", "view"):
            return completed(
                command,
                returncode=1,
                stderr="Could not resolve to a Repository",
            )
        return completed(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    hook.main()

    create_command = next(
        command for command in commands if command[:3] == ("gh", "repo", "create")
    )
    assert "--public" in create_command


def test_remote_settings_precede_first_push_and_push_failure_is_reported(
    hook, monkeypatch, capsys
):
    """The first workflow starts configured, and a rejected push stays visible."""
    answers = iter(["yes", "", "yes"])
    monkeypatch.setattr(hook.os, "isatty", lambda _: True)
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    commands = []

    def fake_run_command(*command):
        commands.append(command)
        if command[:3] == ("gh", "repo", "view"):
            return completed(
                command,
                returncode=1,
                stderr="Could not resolve to a Repository",
            )
        if command[:2] == ("git", "push"):
            return completed(command, returncode=1, stderr="push rejected")
        return completed(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    hook.main()

    push_index = commands.index(("git", "push", "-u", "origin", "main"))
    api_indexes = [
        index for index, command in enumerate(commands) if command[:2] == ("gh", "api")
    ]
    assert api_indexes
    assert all(index < push_index for index in api_indexes)
    output = capsys.readouterr().out
    assert "Could not push main to GitHub: push rejected" in output
    assert "To publish to PyPI" not in output


def test_pages_failure_is_reported_without_false_success(hook, monkeypatch, capsys):
    """Failed Pages API calls do not claim that Pages was enabled."""

    def fake_run_command(*command):
        return completed(command, returncode=1, stderr="permission denied")

    monkeypatch.setattr(hook, "run_command", fake_run_command)

    assert hook.enable_github_pages() is False
    output = capsys.readouterr().out
    assert "Could not configure GitHub Pages" in output
    assert "Pages enabled" not in output
