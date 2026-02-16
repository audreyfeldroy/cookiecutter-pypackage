# Cookiecutter PyPackage

[![PyPI version](https://img.shields.io/pypi/v/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)
[![PyPI downloads](https://img.shields.io/pypi/dm/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package.

*   GitHub repo: [https://github.com/audreyfeldroy/cookiecutter-pypackage/](https://github.com/audreyfeldroy/cookiecutter-pypackage/)
*   Free software: MIT license
*   Discord: [https://discord.gg/PWXJr3upUE](https://discord.gg/PWXJr3upUE)

## Features

*   Modern tooling: [uv](https://docs.astral.sh/uv/) for dependency management, [justfile](https://github.com/casey/just) for task running
*   Testing with [pytest](https://docs.pytest.org/), GitHub Actions CI for Python 3.12, 3.13, and 3.14
*   Auto-publish to [PyPI](https://pypi.org/) when you push a `v*` tag, using [Trusted Publishers](https://docs.pypi.org/trusted-publishers/) (no API tokens needed)
*   [Hardened GitHub Actions workflows](#github-actions-workflows): SHA-pinned actions, minimal permissions, [Dependabot](https://docs.github.com/en/code-security/dependabot) for automated updates
*   Linting with [ruff](https://docs.astral.sh/ruff/), type checking with [ty](https://docs.astral.sh/ty/)
*   Command line interface using [Typer](https://typer.tiangolo.com/)

## Quickstart

First, install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you haven't already.

Generate a new Python package:

```bash
uvx cookiecutter-pypackage
```

You'll be prompted for some values:

```
[1/10] full_name (Audrey M. Roy Greenfeld): Your Name
[2/10] email (audreyfeldroy@example.com): you@example.com
[3/10] github_username (audreyfeldroy): your-github-username
[4/10] pypi_package_name (python-boilerplate): my-package
[5/10] project_name (Python Boilerplate): My Package
[6/10] project_slug (my_package):
[7/10] project_short_description (...): A short description of your package.
[8/10] pypi_username (your-github-username):
[9/10] author_website ():
[10/10] first_version (0.1.0):
```

<details>
<summary>Traditional way (without uvx)</summary>

```bash
uv venv
source .venv/bin/activate
uv pip install cookiecutter
cookiecutter gh:audreyfeldroy/cookiecutter-pypackage
```

</details>

Then:

*   Create a GitHub repo and push your code
*   Set up [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) for your repo
*   Release your package by pushing a tag: `git tag v0.1.0 && git push --tags`

## GitHub Actions Workflows

Your generated project comes with three workflow files and a Dependabot config, all security-hardened out of the box.

### CI (`ci.yml`)

Runs on every push to `main` and on pull requests. Four jobs:

- **Lint** - checks formatting (`ruff format --check`) and lint rules (`ruff check`)
- **Type check** - runs [ty](https://docs.astral.sh/ty/) for static type checking
- **Test** - runs pytest across Python 3.12, 3.13, and 3.14
- **All checks pass** - a single status check for branch protection (uses [alls-green](https://github.com/re-actors/alls-green))

You can also trigger it manually from the Actions tab (`workflow_dispatch`).

### Publish (`publish.yml`)

Runs when you push a tag matching `v*` (e.g., `v0.1.0`). Two jobs:

1. **Build** - builds the sdist and wheel with `uv build`, uploads them as artifacts
2. **Publish** - downloads the artifacts, generates [Sigstore build attestations](https://docs.pypi.org/attestations/), and publishes to PyPI

Publishing uses [Trusted Publishers](https://docs.pypi.org/trusted-publishers/), so there are no API tokens to manage. PyPI verifies the package came from your GitHub repo's workflow via OIDC.

**First-time setup:** You need to register your repo as a trusted publisher on PyPI and create a `pypi` environment in your GitHub repo settings. See [PyPI Release Checklist](docs/pypi_release_checklist.md) for the steps.

### Dependabot (`dependabot.yml`)

Checks weekly for newer versions of the GitHub Actions used in your workflows and opens PRs to update them. Since all actions are pinned by SHA, Dependabot is how they stay current.

### Security hardening

All workflows follow these practices:

- **SHA-pinned actions** - every `uses:` references a full commit SHA, not a mutable tag. This prevents a compromised action from injecting code into your builds.
- **Minimal permissions** - `permissions: {}` at the workflow level, with specific permissions granted only to jobs that need them.
- **No persisted credentials** - `persist-credentials: false` on all checkouts, so the `GITHUB_TOKEN` isn't left in the git config after checkout.
- **Concurrency controls** - CI cancels redundant runs on the same PR. Publish uses a concurrency group to prevent overlapping releases.

## Not Exactly What You Want?

Don't worry, you have options:

### Fork This / Create Your Own

If you have differences in your preferred setup, I encourage you to fork this
to create your own version. Or create your own; it doesn't strictly have to
be a fork.

### Similar Cookiecutter Templates

Explore other forks to get ideas. See the [network](https://github.com/audreyfeldroy/cookiecutter-pypackage/network) and [family tree](https://github.com/audreyfeldroy/cookiecutter-pypackage/network/members) for this repo.

### Or Submit a Pull Request

I also accept pull requests on this, if they're small, atomic, and if they
make my own packaging experience better.
