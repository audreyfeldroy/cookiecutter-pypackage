#!/usr/bin/env python
"""Post-generation hooks for cookiecutter-pypackage."""

import shutil
import subprocess

OWNER = "{{ cookiecutter.github_repo_owner }}"
REPO = "{{ cookiecutter.package_name }}"


def enable_github_pages():
    """Enable GitHub Pages with Actions source if gh CLI is available.

    The docs workflow deploys to GitHub Pages via actions/deploy-pages,
    which requires Pages to be configured with build_type=workflow.
    """
    if not shutil.which("gh"):
        print("  gh CLI not found, skipping GitHub Pages setup.")
        print("  Enable manually: Settings > Pages > Source > GitHub Actions")
        return

    try:
        subprocess.run(
            [
                "gh",
                "api",
                f"repos/{OWNER}/{REPO}/pages",
                "-X",
                "POST",
                "-f",
                "build_type=workflow",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        # If already enabled with a different source, switch it
        subprocess.run(
            [
                "gh",
                "api",
                f"repos/{OWNER}/{REPO}/pages",
                "-X",
                "PUT",
                "-f",
                "build_type=workflow",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        print(f"  GitHub Pages enabled for {OWNER}/{REPO} (source: GitHub Actions)")
    except Exception:
        print("  Could not configure GitHub Pages automatically.")
        print("  Enable manually: Settings > Pages > Source > GitHub Actions")


def print_pypi_trusted_publisher_instructions():
    """Print instructions for adding a PyPI trusted publisher.

    PyPI has no API for this, it must be done through the web UI.
    Print the exact URL and values so the user can set it up quickly.
    """
    print()
    print("  PyPI trusted publisher (required for automated releases):")
    print(f"  https://pypi.org/manage/project/{REPO}/settings/publishing/")
    print()
    print("  Add a new GitHub publisher with these values:")
    print(f"    Owner:        {OWNER}")
    print(f"    Repository:   {REPO}")
    print(f"    Workflow:     publish.yml")
    print(f"    Environment:  pypi")
    print()


if __name__ == "__main__":
    enable_github_pages()
    print_pypi_trusted_publisher_instructions()
    print("Your Python package project has been created successfully!")
