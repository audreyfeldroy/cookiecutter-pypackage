#!/usr/bin/env python
"""Post-generation hooks for cookiecutter-pypackage."""

import shutil
import subprocess


def enable_github_pages():
    """Enable GitHub Pages with Actions source if gh CLI is available.

    The docs workflow deploys to GitHub Pages via actions/deploy-pages,
    which requires Pages to be configured with build_type=workflow.
    """
    if not shutil.which("gh"):
        print("  gh CLI not found, skipping GitHub Pages setup.")
        print("  Enable manually: Settings > Pages > Source > GitHub Actions")
        return

    owner = "{{ cookiecutter.github_repo_owner }}"
    repo = "{{ cookiecutter.package_name }}"

    try:
        subprocess.run(
            ["gh", "api", f"repos/{owner}/{repo}/pages", "-X", "POST", "-f", "build_type=workflow"],
            capture_output=True,
            text=True,
            check=False,
        )
        # If already enabled with a different source, switch it
        subprocess.run(
            ["gh", "api", f"repos/{owner}/{repo}/pages", "-X", "PUT", "-f", "build_type=workflow"],
            capture_output=True,
            text=True,
            check=False,
        )
        print(f"  GitHub Pages enabled for {owner}/{repo} (source: GitHub Actions)")
    except Exception:
        print("  Could not configure GitHub Pages automatically.")
        print("  Enable manually: Settings > Pages > Source > GitHub Actions")


if __name__ == "__main__":
    enable_github_pages()
    print("Your Python package project has been created successfully!")
