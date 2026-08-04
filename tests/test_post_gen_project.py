"""Tests for the post-generation GitHub setup flow."""

import importlib.util
import subprocess
from pathlib import Path

import pytest
from cookiecutter.generate import create_env_with_context

HOOK_PATH = Path(__file__).parents[1] / "hooks" / "post_gen_project.py"


def load_hook(tmp_path, **overrides):
    """Render and load the hook exactly as Cookiecutter does."""
    source = HOOK_PATH.read_text(encoding="utf-8")
    values = {
        "github_repo_owner": "example-owner",
        "package_name": "example-repo",
        "project_short_description": "Example project",
        "import_name": "example_repo",
        "first_version": "0.1.0",
    }
    values.update(overrides)
    context = {"cookiecutter": values}
    rendered = create_env_with_context(context).from_string(source).render(**context)
    rendered_path = tmp_path / "post_gen_project.py"
    rendered_path.write_text(rendered, encoding="utf-8")

    spec = importlib.util.spec_from_file_location(
        "rendered_post_gen_project", rendered_path
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def hook(monkeypatch, tmp_path):
    """Load the hook as a module with predictable rendered values."""
    module = load_hook(tmp_path)
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


def successful(command):
    """Return realistic output for commands that the happy path reads."""
    if command[:3] == ("gh", "config", "get"):
        return completed(command, stdout="ssh\n")
    return completed(command)


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
    answers = iter(["yes", "privte", "", "", "yes"])
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
        return successful(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    hook.main()

    create_command = next(
        command for command in commands if command[:3] == ("gh", "repo", "create")
    )
    assert "--private" in create_command
    assert "--public" not in create_command
    assert not any(
        command[:2] == ("gh", "api") and command[2].endswith("/pages")
        for command in commands
    )
    output = capsys.readouterr().out
    assert "Please enter private or public." in output
    assert "can publish a public website from a private repository" in output
    assert "leave GitHub Pages disabled" in output


def test_final_confirmation_cancels_before_any_write(hook, monkeypatch, capsys):
    """The plan remains read-only until the final confirmation."""
    answers = iter(["yes", "", "", "no"])
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
        return successful(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    hook.main()

    assert not any(command[:3] == ("gh", "repo", "create") for command in commands)
    assert not any(command[0] == "git" for command in commands)
    assert "No repository or Git commit was created" in capsys.readouterr().out


def test_empty_existing_repository_requires_separate_consent(hook, monkeypatch, capsys):
    """An empty repository is connected only after a second explicit yes."""
    answers = iter(["yes", "yes", "", "yes"])
    prompts = []
    monkeypatch.setattr(hook.os, "isatty", lambda _: True)

    def fake_input(prompt):
        prompts.append(prompt)
        return next(answers)

    monkeypatch.setattr("builtins.input", fake_input)
    commands = []

    def fake_run_command(*command):
        commands.append(command)
        if command[:3] == ("gh", "repo", "view"):
            return completed(
                command,
                stdout='{"isEmpty": true, "visibility": "PRIVATE"}',
            )
        return successful(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    hook.main()

    assert not any(command[:3] == ("gh", "repo", "create") for command in commands)
    assert ("git", "push", "-u", "origin", "main") in commands
    output = capsys.readouterr().out
    assert "Using existing empty repository" in output
    assert any("empty and private" in prompt for prompt in prompts)
    assert "connect to the empty private repository" in output


def test_nonempty_existing_repository_is_never_modified(hook, monkeypatch, capsys):
    """The automatic flow refuses to push to a nonempty repository."""
    answers = iter(["yes"])
    monkeypatch.setattr(hook.os, "isatty", lambda _: True)
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    commands = []

    def fake_run_command(*command):
        commands.append(command)
        if command[:3] == ("gh", "repo", "view"):
            return completed(
                command,
                stdout='{"isEmpty": false, "visibility": "PUBLIC"}',
            )
        return successful(command)

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
        return successful(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    assert hook.main() == 0

    create_command = next(
        command for command in commands if command[:3] == ("gh", "repo", "create")
    )
    assert "--public" in create_command
    assert any(
        command[:2] == ("gh", "api") and command[2].endswith("/pages")
        for command in commands
    )
    assert (
        "gh",
        "variable",
        "set",
        "DOCS_DEPLOYMENT_ENABLED",
        "--repo",
        "example-owner/example-repo",
        "--body",
        "true",
    ) in commands


def test_github_setup_pins_one_host_when_ambient_host_differs(
    hook, monkeypatch, capsys
):
    """Every GitHub read, write, display, and push targets GitHub.com."""
    monkeypatch.setenv("GH_HOST", "github.corp.example")
    monkeypatch.setenv(hook.GITHUB_SETUP_ENV, "public")
    monkeypatch.setattr(hook.os, "isatty", lambda _: False)
    calls = []

    def fake_subprocess_run(command, **kwargs):
        calls.append((tuple(command), kwargs))
        if command[:3] == ["gh", "repo", "view"]:
            return completed(
                command,
                returncode=1,
                stderr="Could not resolve to a Repository",
            )
        if command[:3] == ["gh", "config", "get"]:
            return completed(command, stdout="ssh\n")
        return completed(command)

    monkeypatch.setattr(hook.subprocess, "run", fake_subprocess_run)

    assert hook.main() == 0

    github_calls = [
        (command, kwargs) for command, kwargs in calls if command[0] == "gh"
    ]
    assert github_calls
    assert {command[1] for command, _ in github_calls} == {
        "api",
        "auth",
        "config",
        "repo",
        "variable",
    }
    assert all(
        kwargs["env"]["GH_HOST"] == hook.GITHUB_HOST for _, kwargs in github_calls
    )
    assert hook.os.environ["GH_HOST"] == "github.corp.example"
    assert (
        "gh",
        "auth",
        "status",
        "--hostname",
        hook.GITHUB_HOST,
        "--active",
    ) in [command for command, _ in github_calls]
    assert (
        "git",
        "remote",
        "add",
        "origin",
        "git@github.com:example-owner/example-repo.git",
    ) in [command for command, _ in calls]
    output = capsys.readouterr().out
    assert "https://github.com/example-owner/example-repo" in output
    assert "github.corp.example" not in output


def test_explicit_private_mode_leaves_pages_disabled(hook, monkeypatch, capsys):
    """Private automation does not silently publish a public Pages site."""
    monkeypatch.setenv(hook.GITHUB_SETUP_ENV, "private")
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
        return successful(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    assert hook.main() == 0

    assert not any(
        command[:2] == ("gh", "api") and command[2].endswith("/pages")
        for command in commands
    )
    assert (
        "gh",
        "variable",
        "set",
        "DOCS_DEPLOYMENT_ENABLED",
        "--repo",
        "example-owner/example-repo",
        "--body",
        "false",
    ) in commands
    output = capsys.readouterr().out
    assert "Pages will remain disabled for the private repository" in output
    assert "leave GitHub Pages disabled" in output
    assert "documentation deployment workflow paused" in output.lower()


@pytest.mark.parametrize(
    ("protocol", "remote_url"),
    [
        ("ssh", "git@github.com:example-owner/example-repo.git"),
        ("https", "https://github.com/example-owner/example-repo.git"),
    ],
)
def test_push_uses_github_cli_git_protocol(hook, monkeypatch, protocol, remote_url):
    """The first push uses the transport already configured in GitHub CLI."""
    commands = []

    def fake_run_command(*command):
        commands.append(command)
        if command[:3] == ("gh", "config", "get"):
            return completed(command, stdout=f"{protocol}\n")
        return completed(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)

    configured_protocol = hook.github_git_protocol()
    assert configured_protocol == protocol
    assert hook.add_remote_and_push(configured_protocol) is True
    assert ("git", "remote", "add", "origin", remote_url) in commands


def test_commit_failure_reports_partial_local_git_state(hook, monkeypatch, capsys):
    """A late local failure does not claim that no local repository was created."""
    commands = []

    def fake_run_command(*command):
        commands.append(command)
        if command[:2] == ("git", "commit"):
            return completed(command, returncode=1, stderr="Author identity unknown")
        return completed(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)

    assert hook.initialize_git() is False
    assert commands[0] == ("git", "init", "-b", "main")
    assert commands[1] == ("git", "add", ".")
    output = capsys.readouterr().out
    assert "Could not create the first Git commit: Author identity unknown" in output
    assert (
        "GitHub setup stopped before creating or modifying a GitHub repository."
        in output
    )


def test_unsupported_git_protocol_stops_before_writes(hook, monkeypatch, capsys):
    """An unexpected GitHub CLI configuration is reported before setup writes."""

    def fake_run_command(*command):
        return completed(command, stdout="file\n")

    monkeypatch.setattr(hook, "run_command", fake_run_command)

    assert hook.github_git_protocol() is None
    output = capsys.readouterr().out
    assert "unsupported Git protocol: file" in output
    assert "gh config set git_protocol ssh" in output


def test_remote_settings_precede_first_push_and_push_failure_is_reported(
    hook, monkeypatch, capsys
):
    """The first workflow starts configured, and a rejected push stays visible."""
    answers = iter(["yes", "", "yes", "yes"])
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
        return successful(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)
    assert hook.main() == 1

    push_index = commands.index(("git", "push", "-u", "origin", "main"))
    settings_indexes = [
        index
        for index, command in enumerate(commands)
        if command[:2] == ("gh", "api") or command[:3] == ("gh", "variable", "set")
    ]
    assert settings_indexes
    assert all(index < push_index for index in settings_indexes)
    output = capsys.readouterr().out
    assert "Could not push main to GitHub: push rejected" in output
    assert "To publish to PyPI" not in output
    assert "GitHub setup did not complete" in output


def test_explicit_automation_failure_returns_nonzero(hook, monkeypatch, capsys):
    """Automation can reliably detect a requested GitHub setup failure."""
    monkeypatch.setenv(hook.GITHUB_SETUP_ENV, "public")
    monkeypatch.setattr(hook.os, "isatty", lambda _: False)

    def fake_run_command(*command):
        if command[:3] == ("gh", "repo", "view"):
            return completed(
                command,
                returncode=1,
                stderr="Could not resolve to a Repository",
            )
        if command[:3] == ("gh", "repo", "create"):
            return completed(command, returncode=1, stderr="permission denied")
        return successful(command)

    monkeypatch.setattr(hook, "run_command", fake_run_command)

    assert hook.main() == 1
    output = capsys.readouterr().out
    assert "Could not create GitHub repository: permission denied" in output
    assert "GitHub setup did not complete" in output


def test_pages_failure_is_reported_without_false_success(hook, monkeypatch, capsys):
    """Failed Pages API calls do not claim that Pages was enabled."""

    def fake_run_command(*command):
        return completed(command, returncode=1, stderr="permission denied")

    monkeypatch.setattr(hook, "run_command", fake_run_command)

    assert hook.enable_github_pages() is False
    output = capsys.readouterr().out
    assert "Could not configure GitHub Pages" in output
    assert "Pages enabled" not in output


def test_docs_deployment_failure_is_reported_with_recovery_command(
    hook, monkeypatch, capsys
):
    """A failed repository-variable write includes an exact recovery command."""

    def fake_run_command(*command):
        return completed(command, returncode=1, stderr="permission denied")

    monkeypatch.setattr(hook, "run_command", fake_run_command)

    assert hook.configure_docs_deployment(False) is False
    output = capsys.readouterr().out
    assert "Could not configure the documentation deployment workflow" in output
    assert (
        "gh variable set DOCS_DEPLOYMENT_ENABLED "
        "--repo example-owner/example-repo --body false"
    ) in output


@pytest.mark.parametrize(
    "description",
    [
        "Ends with a backslash \\",
        "Spans two lines\nwithout breaking the hook",
        r"Uses a Windows path C:\new\tools",
    ],
)
def test_description_is_rendered_as_a_safe_string_literal(tmp_path, description):
    """Rendered descriptions preserve newlines and backslashes without syntax errors."""
    hook = load_hook(tmp_path, project_short_description=description)

    assert hook.DESCRIPTION == description


def test_all_hook_template_values_are_rendered_safely(tmp_path):
    """Quotes, backslashes, and newlines cannot corrupt the rendered hook."""
    values = {
        "github_repo_owner": 'owner"\\\nnext',
        "package_name": 'repo"\\\nnext',
        "import_name": 'module"\\\nnext',
        "first_version": '1.0"\\\nnext',
    }

    hook = load_hook(tmp_path, **values)

    assert hook.OWNER == values["github_repo_owner"]
    assert hook.REPO == values["package_name"]
    assert hook.IMPORT_NAME == values["import_name"]
    assert hook.FIRST_VERSION == values["first_version"]
