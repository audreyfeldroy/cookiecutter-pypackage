# GitHub Actions Workflows

Your generated project comes with four workflow files and a Dependabot config, all security-hardened out of the box.

## CI (`ci.yml`)

Runs on every push to `main` and on pull requests. Four jobs:

- **Lint** - checks formatting (`ruff format --check`) and lint rules (`ruff check`)
- **Type check** - runs [ty](https://docs.astral.sh/ty/) for static type checking
- **Test** - runs pytest across Python 3.12, 3.13, and 3.14
- **All checks pass** - a single status check for branch protection (uses [alls-green](https://github.com/re-actors/alls-green))

You can also trigger it manually from the Actions tab (`workflow_dispatch`).

## Publish (`publish.yml`)

Runs when you push a tag matching `v*` (e.g., `v0.1.0`). Two jobs:

1. **Build** - builds the sdist and wheel with `uv build`, uploads them as artifacts
2. **Publish** - downloads the artifacts, generates [Sigstore build attestations](https://docs.pypi.org/attestations/), and publishes to PyPI

Publishing uses [Trusted Publishers](https://docs.pypi.org/trusted-publishers/), so there are no API tokens to manage. PyPI verifies the package came from your GitHub repo's workflow via OIDC.

**First-time setup:** You need to register your repo as a trusted publisher on PyPI and create a `pypi` environment in your GitHub repo settings. See [PyPI Release Checklist](pypi_release_checklist.md) for the steps.

## Documentation (`docs.yml`)

Runs on push to `main`. Two jobs:

1. **Build** - builds the documentation site with `zensical build`
2. **Deploy** - deploys to GitHub Pages

**First-time setup:** Go to your repo's Settings > Pages and set the source to **GitHub Actions**.

## Dependabot (`dependabot.yml`)

Checks weekly for newer versions of the GitHub Actions used in your workflows and opens PRs to update them. Since all actions are pinned by SHA, Dependabot is how they stay current.

## Security hardening

All workflows follow these practices:

- **SHA-pinned actions** - every `uses:` references a full commit SHA, not a mutable tag. This prevents a compromised action from injecting code into your builds.
- **Minimal permissions** - `permissions: {}` at the workflow level, with specific permissions granted only to jobs that need them.
- **No persisted credentials** - `persist-credentials: false` on all checkouts, so the `GITHUB_TOKEN` isn't left in the git config after checkout.
- **Concurrency controls** - CI cancels redundant runs on the same PR. Publish uses a concurrency group to prevent overlapping releases.
