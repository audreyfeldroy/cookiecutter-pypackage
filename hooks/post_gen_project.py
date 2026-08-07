#!/usr/bin/env python
"""Post-generation hooks for cookiecutter-pypackage."""

import json
import os
import shutil
import subprocess
from typing import NamedTuple

OWNER = json.loads(
    r"""
{{ cookiecutter.github_repo_owner | tojson }}
""".strip()
)
REPO = json.loads(
    r"""
{{ cookiecutter.package_name | tojson }}
""".strip()
)
DESCRIPTION = json.loads(
    r"""
{{ cookiecutter.project_short_description | tojson }}
""".strip()
)

GITHUB_SETUP_ENV = "COOKIECUTTER_PYPACKAGE_GITHUB"
GITHUB_SETUP_MODES = {"ask", "skip", "private", "public"}
GITHUB_HOST = "github.com"
DOCS_DEPLOYMENT_VARIABLE = "DOCS_DEPLOYMENT_ENABLED"


class GitHubSetupPlan(NamedTuple):
    """A confirmed plan for creating or connecting to a GitHub repository."""

    existing: bool
    visibility: str
    enable_pages: bool
    git_protocol: str


class GitHubSetupDecision(NamedTuple):
    """The result of collecting consent and checking GitHub state."""

    plan: GitHubSetupPlan | None
    failed: bool = False


class GitHubRepositoryState(NamedTuple):
    """The existence, contents, and visibility of the target repository."""

    status: str
    visibility: str | None = None


def run_command(*command):
    """Run a command without raising so the hook can report useful failures."""
    environment = None
    if command and command[0] == "gh":
        environment = os.environ.copy()
        environment["GH_HOST"] = GITHUB_HOST

    try:
        return subprocess.run(
            list(command),
            capture_output=True,
            text=True,
            check=False,
            env=environment,
        )
    except OSError as error:
        return subprocess.CompletedProcess(
            args=list(command),
            returncode=1,
            stdout="",
            stderr=str(error),
        )


def command_error(result):
    """Return the most useful captured error text for a failed command."""
    return (result.stderr or result.stdout).strip() or "unknown error"


def prompt_yes_no(message, *, default=False):
    """Prompt until the user enters an unambiguous yes or no."""
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        answer = input(f"{message} {suffix}: ").strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("  Please answer yes or no.")


def prompt_visibility():
    """Ask for repository visibility, defaulting safely to private."""
    while True:
        answer = input("Repository visibility [private/public] (private): ")
        visibility = answer.strip().lower()
        if not visibility:
            return "private"
        if visibility in {"private", "public"}:
            return visibility
        print("  Please enter private or public.")


def github_setup_mode():
    """Read and validate the setup mode supplied by the package CLI."""
    mode = os.environ.get(GITHUB_SETUP_ENV, "ask").strip().lower()
    if mode not in GITHUB_SETUP_MODES:
        print(
            f"  Ignoring invalid {GITHUB_SETUP_ENV} value {mode!r}; "
            "GitHub setup will be skipped."
        )
        return "skip"
    return mode


def github_cli_ready():
    """Check that GitHub CLI is installed and authenticated."""
    if not shutil.which("gh"):
        print("  GitHub CLI not found; GitHub setup will be skipped.")
        print(
            "  Install it from https://cli.github.com/ and run "
            f"`gh auth login --hostname {GITHUB_HOST}`."
        )
        return False

    result = run_command(
        "gh",
        "auth",
        "status",
        "--hostname",
        GITHUB_HOST,
        "--active",
    )
    if result.returncode == 0:
        return True

    print("  GitHub CLI is not authenticated; GitHub setup will be skipped.")
    print(
        f"  Run `gh auth login --hostname {GITHUB_HOST}`, "
        "then generate the project again."
    )
    return False


def github_repository_state():
    """Return the target repository's contents and visibility."""
    result = run_command(
        "gh",
        "repo",
        "view",
        f"{OWNER}/{REPO}",
        "--json",
        "isEmpty,visibility",
    )
    if result.returncode != 0:
        error = command_error(result)
        missing_markers = (
            "Could not resolve to a Repository",
            "HTTP 404",
            "Not Found",
        )
        if any(marker in error for marker in missing_markers):
            return GitHubRepositoryState("missing")
        print(f"  Could not check GitHub repository {OWNER}/{REPO}: {error}")
        return GitHubRepositoryState("error")

    try:
        data = json.loads(result.stdout)
        is_empty = data["isEmpty"]
        raw_visibility = data["visibility"]
    except (KeyError, TypeError, json.JSONDecodeError):
        print(f"  GitHub returned an unexpected response for {OWNER}/{REPO}.")
        return GitHubRepositoryState("error")

    if not isinstance(raw_visibility, str):
        print(f"  GitHub returned an unexpected response for {OWNER}/{REPO}.")
        return GitHubRepositoryState("error")

    visibility = raw_visibility.lower()
    if not isinstance(is_empty, bool) or visibility not in {
        "internal",
        "private",
        "public",
    }:
        print(f"  GitHub returned an unexpected response for {OWNER}/{REPO}.")
        return GitHubRepositoryState("error")

    status = "empty" if is_empty else "nonempty"
    return GitHubRepositoryState(status, visibility)


def github_git_protocol():
    """Return the authenticated GitHub CLI's configured Git transport."""
    result = run_command(
        "gh",
        "config",
        "get",
        "git_protocol",
        "--host",
        GITHUB_HOST,
    )
    if result.returncode != 0:
        print(f"  Could not read GitHub's Git protocol: {command_error(result)}")
        return None

    protocol = result.stdout.strip().lower()
    if protocol in {"https", "ssh"}:
        return protocol

    print(f"  GitHub CLI returned an unsupported Git protocol: {protocol or 'empty'}.")
    print(f"  Set it with `gh config set git_protocol ssh --host {GITHUB_HOST}`.")
    return None


def github_remote_url(protocol):
    """Build a GitHub remote URL using the user's configured transport."""
    if protocol == "ssh":
        return f"git@{GITHUB_HOST}:{OWNER}/{REPO}.git"
    return f"https://{GITHUB_HOST}/{OWNER}/{REPO}.git"


def github_repository_url():
    """Build the canonical web URL for the target GitHub repository."""
    return f"https://{GITHUB_HOST}/{OWNER}/{REPO}"


def choose_pages_setup(visibility, *, interactive):
    """Choose whether to publish documentation through GitHub Pages."""
    if visibility == "public":
        if interactive:
            return prompt_yes_no("Enable GitHub Pages?", default=True)
        return True

    if not interactive:
        print(f"  GitHub Pages will remain disabled for the {visibility} repository.")
        return False

    print()
    print(
        f"  Warning: GitHub Pages can publish a public website from a "
        f"{visibility} repository."
    )
    print("  Pages for a non-public repository may also require a paid GitHub plan.")
    return prompt_yes_no("Enable GitHub Pages anyway?")


def print_github_plan(plan):
    """Show every external and local action before confirmation."""
    print()
    print("GitHub setup plan:")
    if plan.existing:
        print(
            f"  - connect to the empty {plan.visibility} repository "
            f"{github_repository_url()}"
        )
    else:
        print(f"  - create {github_repository_url()} as a {plan.visibility} repository")
    if plan.git_protocol == "https":
        print("  - configure Git to use GitHub CLI credentials for HTTPS")
    print("  - initialize Git and create the first commit")
    if plan.enable_pages:
        print("  - enable GitHub Pages (publishes a website)")
        print("  - enable the documentation deployment workflow")
    else:
        print("  - leave GitHub Pages disabled")
        print("  - keep the documentation deployment workflow paused")
    print("  - create the pypi environment")
    print(f"  - push main over {plan.git_protocol.upper()}")
    print()


def choose_github_setup(mode):
    """Collect explicit consent and return a safe GitHub setup plan."""
    if mode == "skip":
        print("  GitHub setup skipped.")
        return GitHubSetupDecision(None)

    interactive = mode == "ask"
    if interactive:
        if not os.isatty(0):
            print("  Non-interactive run: GitHub setup skipped.")
            print(
                "  Use `--github private` or `--github public` "
                "to opt in during automation."
            )
            return GitHubSetupDecision(None)
        if not prompt_yes_no("Set up a GitHub repository now?"):
            print("  GitHub setup skipped.")
            return GitHubSetupDecision(None)

    if not github_cli_ready():
        return GitHubSetupDecision(None, failed=True)

    repository_state = github_repository_state()
    if repository_state.status == "error":
        return GitHubSetupDecision(None, failed=True)
    if repository_state.status == "nonempty":
        print(f"  GitHub repository {OWNER}/{REPO} already exists and is not empty.")
        print("  For safety, the generator will not modify it automatically.")
        return GitHubSetupDecision(None, failed=True)

    git_protocol = github_git_protocol()
    if git_protocol is None:
        return GitHubSetupDecision(None, failed=True)

    if repository_state.status == "empty":
        if not interactive:
            print(
                f"  GitHub repository {OWNER}/{REPO} already exists, is empty, "
                f"and is {repository_state.visibility}."
            )
            print(
                "  Run interactively to confirm connecting to an existing repository."
            )
            return GitHubSetupDecision(None, failed=True)
        if not prompt_yes_no(
            f"GitHub repository {OWNER}/{REPO} is empty and "
            f"{repository_state.visibility}. Connect to it?"
        ):
            print("  Existing GitHub repository left unchanged.")
            return GitHubSetupDecision(None)
        visibility = repository_state.visibility
        if visibility is None:
            print(f"  GitHub returned an unexpected response for {OWNER}/{REPO}.")
            return GitHubSetupDecision(None, failed=True)
        existing = True
    else:
        visibility = prompt_visibility() if interactive else mode
        existing = False

    enable_pages = choose_pages_setup(visibility, interactive=interactive)
    plan = GitHubSetupPlan(
        existing=existing,
        visibility=visibility,
        enable_pages=enable_pages,
        git_protocol=git_protocol,
    )

    print_github_plan(plan)
    if interactive and not prompt_yes_no("Continue?"):
        print("  GitHub setup cancelled. No repository or Git commit was created.")
        return GitHubSetupDecision(None)
    return GitHubSetupDecision(plan)


def prepare_github_repository(plan):
    """Create the confirmed GitHub repository or select an empty one."""
    if plan.existing:
        print(f"  Using existing empty repository: {github_repository_url()}")
        return True

    result = run_command(
        "gh",
        "repo",
        "create",
        f"{OWNER}/{REPO}",
        f"--{plan.visibility}",
        "--description",
        DESCRIPTION,
    )
    if result.returncode == 0:
        print(f"  GitHub repository created: {github_repository_url()}")
        return True

    print(f"  Could not create GitHub repository: {command_error(result)}")
    print("  The generated project remains in its local Git repository.")
    return False


IMPORT_NAME = json.loads(
    r"""
{{ cookiecutter.import_name | tojson }}
""".strip()
)

COMMIT_MESSAGE = f"""\
https://github.com/audreyfeldroy/cookiecutter-pypackage scaffolding

- src/{IMPORT_NAME} package with __init__, __main__, cli, utils, py.typed
- tests/test_{IMPORT_NAME}.py
- docs/ with index, installation, usage, api pages
- GitHub CI workflows: ci, codeql, docs, publish, zizmor
- GitHub issue templates: bug report, feature request
- GitHub pull request template
- Dependabot configuration
- justfile with development tasks
- scripts/release.py
- pyproject.toml with uv build configuration
- CHANGELOG/unreleased.md
- LICENSE (MIT)
- README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
- .editorconfig, .gitignore
- zensical.toml
"""


def initialize_git():
    """Initialize Git and make the confirmed first commit locally."""
    steps = (
        (
            ("git", "init", "-b", "main"),
            "initialize the local Git repository",
        ),
        (("git", "add", "."), "stage the generated project"),
        (
            ("git", "commit", "-m", COMMIT_MESSAGE),
            "create the first Git commit",
        ),
    )

    for command, description in steps:
        result = run_command(*command)
        if result.returncode != 0:
            print(f"  Could not {description}: {command_error(result)}")
            print(
                "  GitHub setup stopped before creating or modifying "
                "a GitHub repository."
            )
            return False

    print("  Git initialized with first commit")
    return True


def configure_git_credentials(protocol):
    """Configure Git to use the authenticated GitHub CLI for HTTPS pushes."""
    if protocol != "https":
        return True

    result = run_command("gh", "auth", "setup-git", "--hostname", GITHUB_HOST)
    if result.returncode == 0:
        print(f"  Git configured to use GitHub CLI credentials for {GITHUB_HOST}")
        return True

    print(f"  Could not configure Git credentials for HTTPS: {command_error(result)}")
    print(f"  Run `gh auth setup-git --hostname {GITHUB_HOST}`, then generate again.")
    return False


def add_remote_and_push(protocol):
    """Connect the confirmed GitHub repository and push its first commit."""
    remote_url = github_remote_url(protocol)
    steps = (
        (
            (
                "git",
                "remote",
                "add",
                "origin",
                remote_url,
            ),
            "add the GitHub remote",
        ),
        (
            ("git", "push", "-u", "origin", "main"),
            "push main to GitHub",
        ),
    )

    for command, description in steps:
        result = run_command(*command)
        if result.returncode != 0:
            print(f"  Could not {description}: {command_error(result)}")
            print(
                "  The repository may need manual setup before the first push succeeds."
            )
            return False

    print(f"  Pushed to {github_repository_url()}")
    return True


def enable_github_pages():
    """Enable GitHub Pages with Actions as the deployment source."""
    create_result = run_command(
        "gh",
        "api",
        f"repos/{OWNER}/{REPO}/pages",
        "-X",
        "POST",
        "-f",
        "build_type=workflow",
    )
    if create_result.returncode == 0:
        print(f"  GitHub Pages enabled for {OWNER}/{REPO}")
        return True

    update_result = run_command(
        "gh",
        "api",
        f"repos/{OWNER}/{REPO}/pages",
        "-X",
        "PUT",
        "-f",
        "build_type=workflow",
    )
    if update_result.returncode == 0:
        print(f"  GitHub Pages configured for {OWNER}/{REPO}")
        return True

    print(
        "  Could not configure GitHub Pages: "
        f"{command_error(update_result) or command_error(create_result)}"
    )
    print("  Configure it manually: Settings > Pages > Source > GitHub Actions")
    return False


def configure_docs_deployment(enabled):
    """Record whether the GitHub Pages deployment workflow should run."""
    value = "true" if enabled else "false"
    result = run_command(
        "gh",
        "variable",
        "set",
        DOCS_DEPLOYMENT_VARIABLE,
        "--repo",
        f"{OWNER}/{REPO}",
        "--body",
        value,
    )
    if result.returncode == 0:
        status = "enabled" if enabled else "paused"
        print(f"  Documentation deployment workflow {status} for {OWNER}/{REPO}")
        return True

    print(
        "  Could not configure the documentation deployment workflow: "
        f"{command_error(result)}"
    )
    print(
        f"  Set it manually: gh variable set {DOCS_DEPLOYMENT_VARIABLE} "
        f"--repo {OWNER}/{REPO} --body {value}"
    )
    return False


def create_pypi_environment():
    """Create the GitHub environment used for PyPI trusted publishing."""
    result = run_command(
        "gh",
        "api",
        f"repos/{OWNER}/{REPO}/environments/pypi",
        "-X",
        "PUT",
    )
    if result.returncode == 0:
        print(f"  GitHub environment 'pypi' created for {OWNER}/{REPO}")
        return True

    print(f"  Could not create the pypi environment: {command_error(result)}")
    print("  Create it manually: Settings > Environments > New environment > pypi")
    return False


def print_pypi_trusted_publisher_instructions():
    """Print the exact values needed to add a pending publisher on PyPI."""
    print()
    print("To publish to PyPI, add a pending publisher at:")
    print("https://pypi.org/manage/account/publishing/")
    print()
    print("Fill in these values:")
    print(f"  PyPI project name:  {REPO}")
    print(f"  Owner:              {OWNER}")
    print(f"  Repository:         {REPO}")
    print("  Workflow:           publish.yml")
    print("  Environment:        pypi")
    print()
    print("Then release with:")
    print("  just release")
    print()


def main():
    """Run the confirmed setup flow after Cookiecutter renders the project."""
    mode = github_setup_mode()
    decision = choose_github_setup(mode)
    plan = decision.plan
    failed = decision.failed

    if plan is None:
        print("  Project generated locally without creating a Git commit.")
    elif not configure_git_credentials(plan.git_protocol):
        print("  Project generated, but Git credential setup did not complete.")
        failed = True
    elif not initialize_git():
        print("  Project generated, but Git setup did not complete.")
        failed = True
    elif not prepare_github_repository(plan):
        print("  Project generated with a local commit, but no GitHub repository.")
        failed = True
    else:
        pages_ready = True
        if plan.enable_pages:
            pages_ready = enable_github_pages()
        else:
            print("  GitHub Pages setup skipped.")

        docs_deployment_ready = configure_docs_deployment(
            plan.enable_pages and pages_ready
        )
        environment_ready = create_pypi_environment()
        push_succeeded = add_remote_and_push(plan.git_protocol)
        if push_succeeded:
            print_pypi_trusted_publisher_instructions()
        else:
            print("  Project generated, but the first GitHub push did not complete.")
        failed = not (
            pages_ready
            and docs_deployment_ready
            and environment_ready
            and push_succeeded
        )

    if failed:
        print("Project files were generated, but GitHub setup did not complete.")
        return 1

    print("Your Python package project has been created successfully!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
