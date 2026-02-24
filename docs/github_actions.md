# GitHub Actions Workflows

Your generated project comes with six workflow files and a Dependabot config, all security-hardened out of the box.

## CI (`ci.yml`)

Runs on every push to `main` and on pull requests. Five jobs:

- **Lint** - checks formatting (`ruff format --check`) and lint rules (`ruff check`)
- **Type check** - runs [ty](https://docs.astral.sh/ty/) for static type checking
- **Test** - runs pytest with coverage across Python 3.12, 3.13, and 3.14
- **Coverage** - combines coverage data from all Python versions and posts the report to the GitHub Actions step summary
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

## CodeQL (`codeql.yml`)

Runs on pushes to `main`, pull requests, and a weekly schedule. Uses GitHub's [CodeQL](https://codeql.github.com/) engine with the `security-extended` query suite, which adds medium-precision security checks (taint tracking, injection detection) on top of the default high-precision set. Results appear in your repo's Security > Code scanning tab.

CodeQL does dataflow analysis that linters can't: it traces user input across function calls and files to find SQL injection, command injection, SSRF, path traversal, and similar vulnerabilities.

If your package includes compiled code, the workflow has inline comments showing how to add `c-cpp`, `go`, `java-kotlin`, or `swift` and switch to `autobuild`.

## Zizmor (`zizmor.yml`)

Runs on pushes and pull requests that touch `.github/workflows/`. [Zizmor](https://woodruffw.github.io/zizmor/) audits your GitHub Actions workflows for security issues: excessive permissions, unpinned actions, credential exposure, cache poisoning risks, and other patterns that tools like CodeQL don't cover (since CodeQL analyzes your code, not your CI configuration).

## Dependabot (`dependabot.yml`)

Checks weekly for newer versions of the GitHub Actions used in your workflows and opens PRs to update them. Since all actions are pinned by SHA, Dependabot is how they stay current.

A 7-day cooldown prevents Dependabot from proposing updates the moment a new version drops. This gives the community time to discover regressions or compromised releases before your project pulls them in.

## Security hardening

All workflows follow these practices:

- **SHA-pinned actions** - every `uses:` references a full commit SHA, not a mutable tag. This prevents a compromised action from injecting code into your builds.
- **Minimal permissions** - `permissions: {}` at the workflow level, with specific permissions granted only to jobs that need them.
- **No persisted credentials** - `persist-credentials: false` on all checkouts, so the `GITHUB_TOKEN` isn't left in the git config after checkout.
- **No cache in release builds** - the publish workflow disables uv's cache. GitHub Actions caches aren't isolated between workflows, so a compromised low-privilege workflow could [poison the cache](https://adnanthekhan.com/2024/05/06/the-monsters-in-your-build-cache-github-actions-cache-poisoning/) and inject code into your release artifacts. Building from scratch on every release eliminates this vector.
- **Concurrency controls** - CI cancels redundant runs on the same PR. Publish uses a concurrency group to prevent overlapping releases. Docs deployments don't cancel in-flight runs to avoid a half-deployed site.
