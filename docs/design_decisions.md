# Design Decisions

This template is opinionated. Here's why it makes the choices it does.

## No pre-commit hooks

CI is the enforcement layer, not your commit history. `just qa` runs the same checks locally when you want them. The difference is that `just qa` doesn't stand between you and saving your work.

Pre-commit hooks punish frequent committers. If you commit every 5 minutes (good), you pay 12x the hook tax of someone who commits once an hour. They break during interactive rebases, firing on every replayed commit. And they're bypassable with `--no-verify`, so you can't rely on them anyway. CI is where enforcement actually happens.

## justfile, not Makefile

[just](https://github.com/casey/just) is a command runner, not a build system. It doesn't track file timestamps or have implicit rules. `just qa` means "run these commands in order," which is exactly what you want for a development workflow. Makefiles can do this too, but you're fighting the tool's assumptions about build artifacts the whole time.

## ruff, not black + isort + flake8

[Ruff](https://docs.astral.sh/ruff/) replaces three tools with one. It formats (replacing black), sorts imports (replacing isort), and lints (replacing flake8 and its plugin ecosystem). Configuration is one `[tool.ruff]` section in `pyproject.toml` instead of three separate configs.

## ty, not mypy

[ty](https://docs.astral.sh/ty/) is a new type checker from the Astral team (the same people behind ruff and uv). It's fast, has all rules enabled by default, and supports watch mode (`just type-check-watch`). It's newer than mypy and the ecosystem is still catching up, but for a new project starting fresh, it's the right default.

## uv, not pip + virtualenv + pip-tools

[uv](https://docs.astral.sh/uv/) handles virtual environments, dependency resolution, locking, and Python version management in one tool. No more `python -m venv`, `pip install -r requirements-dev.txt`, `pip-compile`. Just `uv sync`.

## No tox

`uv run --python=3.12 pytest` runs tests on a specific Python version. The justfile's `testall` command runs across 3.12, 3.13, and 3.14. CI does the same in a matrix. tox was valuable when managing multiple virtualenvs was hard. uv makes it trivial.

## Zensical, not Sphinx

[Zensical](https://zensical.org/) builds on MkDocs with the Material theme. You write Markdown, not reStructuredText. API docs generate from docstrings via [mkdocstrings](https://mkdocstrings.github.io/). The docs site deploys to GitHub Pages, not Read the Docs.

## Trusted Publishers, not API tokens

PyPI publishing uses [Trusted Publishers](https://docs.pypi.org/trusted-publishers/) with OIDC. GitHub Actions proves its identity to PyPI cryptographically. No API tokens to create, rotate, or accidentally leak. Push a `v*` tag and the package ships.

## SHA-pinned actions, not version tags

Every GitHub Action is pinned by commit SHA, not by version tag like `v4`. Version tags are mutable. A compromised action could move its `v4` tag to point at malicious code, and every repo using `actions/checkout@v4` would run it on the next trigger. SHA pins are immutable. Dependabot keeps them current.

## Built-in coverage, not codecov or coveralls

Coverage runs in CI with branch coverage, parallel mode, and cross-version combining across Python 3.12, 3.13, and 3.14. The report posts to the GitHub Actions summary. No external service to sign up for, no tokens to configure, no third-party access to your repo.

## src layout, not flat layout

Your package code lives under `src/`, not at the repo root. This prevents tests from accidentally importing local source files instead of the installed package. It's a few extra characters in import paths, but it eliminates an entire class of "works on my machine" bugs.

## Focused .gitignore, not the kitchen sink

The generated `.gitignore` covers what a Python package actually produces: `__pycache__`, `.venv`, `dist/`, `*.egg-info`, coverage files, and docs build output. GitHub's default Python `.gitignore` is 200+ lines of entries for tools you might never use.
