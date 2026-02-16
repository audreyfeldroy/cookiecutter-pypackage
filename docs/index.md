# Cookiecutter PyPackage

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package.

## What you get

- Modern tooling: [uv](https://docs.astral.sh/uv/) for dependency management, [justfile](https://github.com/casey/just) for task running
- Testing with [pytest](https://docs.pytest.org/), GitHub Actions CI for Python 3.12, 3.13, and 3.14
- Auto-publish to [PyPI](https://pypi.org/) when you push a `v*` tag, using [Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- Documentation site built with [Zensical](https://zensical.org/) and auto-deployed to GitHub Pages
- API docs auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/)
- Linting with [ruff](https://docs.astral.sh/ruff/), type checking with [ty](https://docs.astral.sh/ty/)
- Command line interface using [Typer](https://typer.tiangolo.com/)
- Hardened GitHub Actions workflows: SHA-pinned actions, minimal permissions, Dependabot for updates

## Quick start

```bash
uvx cookiecutter-pypackage
```

See the [Tutorial](tutorial.md) for a full walkthrough.
