# Cookiecutter PyPackage

I built this template to give you everything a Python package needs, ready to go from the moment you generate it.

```bash
uvx cookiecutter-pypackage
```

Answer a few [prompts](prompts.md) and you'll have a complete project: source code with a CLI, a test suite, a documentation site, and CI/CD that handles linting, type checking, testing, and publishing to PyPI.

## Your project comes ready with

**A real development workflow.** [uv](https://docs.astral.sh/uv/) manages your dependencies and virtual environments. [just](https://github.com/casey/just) gives you one command for everything: `just qa` formats your code with [ruff](https://docs.astral.sh/ruff/), lints it, type-checks with [ty](https://docs.astral.sh/ty/), and runs your [pytest](https://docs.pytest.org/) suite across Python 3.12, 3.13, and 3.14. A [Typer](https://typer.tiangolo.com/) CLI is wired up and working from the first `uv sync`.

**A documentation site that deploys itself.** [Zensical](https://zensical.org/) builds your docs with the Material theme, light and dark mode, and [mkdocstrings](https://mkdocstrings.github.io/) generates API reference pages from your docstrings. Push to main and it's live on GitHub Pages. Preview locally with `just docs-serve`.

**Automated PyPI publishing with no tokens to manage.** Push a `v*` tag and GitHub Actions builds your package, signs it with [Sigstore](https://docs.pypi.org/attestations/), and publishes via [Trusted Publishers](https://docs.pypi.org/trusted-publishers/). OIDC handles authentication, so there are no API tokens to create, rotate, or leak.

**Security-hardened CI you don't have to think about.** Every GitHub Action is pinned by SHA. Permissions are minimal. Credentials aren't persisted after checkout. [Dependabot](https://docs.github.com/en/code-security/dependabot) opens PRs weekly to keep your actions current. See [GitHub Actions](github_actions.md) for the full details.

**Coverage that works the way coverage.py intends.** Branch coverage, parallel mode, cross-version combining across Python 3.12, 3.13, and 3.14, and a `fail_under` floor you raise as your project grows. CI collects coverage from every Python version and posts a combined report to the GitHub Actions summary.

**A clean project structure.** [src layout](project_structure.md) so you never accidentally import local code during testing. A [py.typed](https://peps.python.org/pep-0561/) marker and type hints on all starter code. `__main__.py` so your package works with `python -m`. A focused .gitignore instead of the 200-line GitHub default.

**Justfile commands for everything.** `just qa` is the daily driver, but there's also `just test`, `just testall`, `just type-check-watch`, `just coverage`, `just docs-serve`, `just tag`, and more. Run `just list` to see them all. See [Project Structure](project_structure.md#justfile-commands) for the full table.

**Your name on it.** The generated README includes a bold "Created by" line linking to your GitHub profile, PyPI profile, and personal website. You built the package, you should get the credit.

## Get started

The [Tutorial](tutorial.md) walks you through everything: generating your package, running the tests, pushing to GitHub, deploying your docs, and publishing your first release to PyPI.

If something goes wrong, check [Troubleshooting](troubleshooting.md).
