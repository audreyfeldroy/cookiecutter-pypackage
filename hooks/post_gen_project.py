#!/usr/bin/env python
"""Post-generation hooks for cookiecutter-pypackage."""

import json
import os
import shutil
import subprocess
from typing import NamedTuple

OWNER = "{{ cookiecutter.github_repo_owner }}"
REPO = "{{ cookiecutter.package_name }}"
DESCRIPTION = "{{ cookiecutter.project_short_description | replace('\"', '\\\"') }}"

GITHUB_SETUP_ENV = "COOKIECUTTER_PYPACKAGE_GITHUB"
GITHUB_SETUP_MODES = {"ask", "skip", "private", "public"}


class GitHubSetupPlan(NamedTuple):
    """A confirmed plan for creating or connecting to a GitHub repository."""

    existing: bool
    visibility: str | None


def run_command(*command):
    """Run a command without raising so the hook can report useful failures."""
    try:
        return subprocess.run(
            list(command),
            capture_output=True,
            text=True,
            check=False,
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
        print("  Install it from https://cli.github.com/ and run `gh auth login`.")
        return False

    result = run_command("gh", "auth", "status")
    if result.returncode == 0:
        return True

    print("  GitHub CLI is not authenticated; GitHub setup will be skipped.")
    print("  Run `gh auth login`, then generate the project again.")
    return False


def github_repository_state():
    """Return missing, empty, nonempty, or error for the target repository."""
    result = run_command(
        "gh",
        "repo",
        "view",
        f"{OWNER}/{REPO}",
        "--json",
        "isEmpty",
    )
    if result.returncode != 0:
        error = command_error(result)
        missing_markers = (
            "Could not resolve to a Repository",
            "HTTP 404",
            "Not Found",
        )
        if any(marker in error for marker in missing_markers):
            return "missing"
        print(f"  Could not check GitHub repository {OWNER}/{REPO}: {error}")
        return "error"

    try:
        is_empty = json.loads(result.stdout)["isEmpty"]
    except (KeyError, TypeError, json.JSONDecodeError):
        print(f"  GitHub returned an unexpected response for {OWNER}/{REPO}.")
        return "error"

    return "empty" if is_empty else "nonempty"


def print_github_plan(plan):
    """Show every external and local action before confirmation."""
    print()
    print("GitHub setup plan:")
    if plan.existing:
        print(f"  - connect to the empty repository https://github.com/{OWNER}/{REPO}")
    else:
        print(
            f"  - create https://github.com/{OWNER}/{REPO} "
            f"as a {plan.visibility} repository"
        )
    print("  - initialize Git and create the first commit")
    print("  - enable GitHub Pages")
    print("  - create the pypi environment")
    print("  - push main")
    print()


def choose_github_setup():
    """Collect explicit consent and return a safe GitHub setup plan."""
    mode = github_setup_mode()
    if mode == "skip":
        print("  GitHub setup skipped.")
        return None

    interactive = mode == "ask"
    if interactive:
        if not os.isatty(0):
            print("  Non-interactive run: GitHub setup skipped.")
            print(
                "  Use `--github private` or `--github public` "
                "to opt in during automation."
            )
            return None
        if not prompt_yes_no("Set up a GitHub repository now?"):
            print("  GitHub setup skipped.")
            return None

    if not github_cli_ready():
        return None

    repository_state = github_repository_state()
    if repository_state == "error":
        return None
    if repository_state == "nonempty":
        print(f"  GitHub repository {OWNER}/{REPO} already exists and is not empty.")
        print("  For safety, the generator will not modify it automatically.")
        return None

    if repository_state == "empty":
        if not interactive:
            print(f"  GitHub repository {OWNER}/{REPO} already exists and is empty.")
            print(
                "  Run interactively to confirm connecting to an existing repository."
            )
            return None
        if not prompt_yes_no(
            f"GitHub repository {OWNER}/{REPO} is empty. Connect to it?"
        ):
            print("  Existing GitHub repository left unchanged.")
            return None
        plan = GitHubSetupPlan(existing=True, visibility=None)
    else:
        visibility = prompt_visibility() if interactive else mode
        plan = GitHubSetupPlan(existing=False, visibility=visibility)

    print_github_plan(plan)
    if interactive and not prompt_yes_no("Continue?"):
        print("  GitHub setup cancelled. No repository or Git commit was created.")
        return None
    return plan


def prepare_github_repository(plan):
    """Create the confirmed GitHub repository or select an empty one."""
    if plan.existing:
        print(f"  Using existing empty repository: https://github.com/{OWNER}/{REPO}")
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
        print(f"  GitHub repository created: https://github.com/{OWNER}/{REPO}")
        return True

    print(f"  Could not create GitHub repository: {command_error(result)}")
    print("  The generated project remains in its local Git repository.")
    return False


IMPORT_NAME = "{{ cookiecutter.import_name }}"
FIRST_VERSION = "{{ cookiecutter.first_version }}"

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
- CHANGELOG/{FIRST_VERSION}.md
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
            print("  GitHub setup stopped before creating or modifying a repository.")
            return False

    print("  Git initialized with first commit")
    return True


def add_remote_and_push():
    """Connect the confirmed GitHub repository and push its first commit."""
    steps = (
        (
            (
                "git",
                "remote",
                "add",
                "origin",
                f"https://github.com/{OWNER}/{REPO}.git",
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

    print(f"  Pushed to https://github.com/{OWNER}/{REPO}")
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
    plan = choose_github_setup()
    if plan is None:
        print("  Project generated locally without creating a Git commit.")
    elif not initialize_git():
        print("  Project generated, but Git setup did not complete.")
    elif not prepare_github_repository(plan):
        print("  Project generated with a local commit, but no GitHub repository.")
    else:
        enable_github_pages()
        create_pypi_environment()
        if add_remote_and_push():
            print_pypi_trusted_publisher_instructions()
        else:
            print("  Project generated, but the first GitHub push did not complete.")

    print("Your Python package project has been created successfully!")


if __name__ == "__main__":
    main()
