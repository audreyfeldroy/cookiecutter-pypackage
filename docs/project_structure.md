# Project Structure

After generating your package, you'll have a project that looks like this:

```
my-package/
├── .github/
│   ├── dependabot.yml
│   ├── ISSUE_TEMPLATE.md
│   └── workflows/
│       ├── ci.yml          # Lint, type check, test
│       ├── docs.yml        # Build and deploy docs
│       └── publish.yml     # Publish to PyPI on tag
├── docs/
│   ├── api.md              # Auto-generated API reference
│   ├── index.md            # Docs landing page
│   ├── installation.md
│   └── usage.md
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── __main__.py     # Enables `python -m my_package`
│       ├── cli.py          # Typer CLI
│       ├── py.typed        # Type annotation marker (PEP 561)
│       └── utils.py        # Placeholder, rename or delete
├── tests/
│   └── test_my_package.py
├── .gitignore
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── HISTORY.md
├── justfile                # Task runner commands
├── LICENSE
├── pyproject.toml          # Package metadata and tool config
├── README.md
└── zensical.toml           # Documentation site config
```

## Source code (`src/`)

The project uses a **src layout**, where your package code lives under `src/` rather than at the root. This prevents accidentally importing local code during testing, which is a common source of subtle bugs.

Put your code in `src/my_package/`. The `utils.py` file is a placeholder to get you started. Rename it, delete it, or add new modules alongside it.

## CLI (`cli.py`)

Your package includes a [Typer](https://typer.tiangolo.com/) command-line interface. After `uv sync`, you can run it three ways:

```bash
uv run my-package          # via the entry point
uv run my-package --help   # show help
uv run python -m my_package  # via __main__.py
```

The entry point is configured in `pyproject.toml` under `[project.scripts]`. To add commands, add new functions decorated with `@app.command()` in `cli.py`. See the [Typer docs](https://typer.tiangolo.com/tutorial/) for details.

## Justfile commands

Run `just list` to see all available commands. The key ones:

| Command | What it does |
|---|---|
| `just qa` | Format, lint, type-check, and test (the daily driver) |
| `just test` | Run tests only |
| `just testall` | Run tests on Python 3.12, 3.13, and 3.14 |
| `just type-check` | Type-check with ty |
| `just type-check-watch` | Type-check in watch mode |
| `just docs-serve` | Preview docs locally at http://localhost:8000 |
| `just docs-build` | Build docs |
| `just coverage` | Run tests with coverage and generate HTML report |
| `just tag` | Tag the current version and push to GitHub |
| `just build` | Build sdist and wheel |

## GitHub Actions workflows

All workflows are security-hardened: SHA-pinned actions, minimal permissions, `persist-credentials: false` on checkouts, and Dependabot for automated action updates.

**CI** (`ci.yml`) runs on every push to `main` and on pull requests:

- **Lint** checks formatting (`ruff format --check`) and lint rules (`ruff check`)
- **Type check** runs [ty](https://docs.astral.sh/ty/)
- **Test** runs pytest across Python 3.12, 3.13, and 3.14
- **All checks pass** is a single status check for branch protection (uses [alls-green](https://github.com/re-actors/alls-green))

**Publish** (`publish.yml`) runs when you push a `v*` tag:

1. Builds the sdist and wheel with `uv build`
2. Publishes to PyPI using [Trusted Publishers](https://docs.pypi.org/trusted-publishers/) (no API tokens needed)

**Documentation** (`docs.yml`) runs on push to `main`:

1. Builds the docs site with Zensical
2. Deploys to GitHub Pages

**Dependabot** (`dependabot.yml`) checks weekly for newer versions of the GitHub Actions used in your workflows and opens PRs to update them.

## Documentation site

The docs site is built with [Zensical](https://zensical.org/) and configured in `zensical.toml`. It uses the Material theme with light/dark mode.

The API reference page (`docs/api.md`) auto-generates documentation from your docstrings using [mkdocstrings](https://mkdocstrings.github.io/). Write docstrings in your code and they'll appear on the docs site automatically.

To enable deployment, go to your repo's Settings > Pages and set the source to **GitHub Actions**. See the [Tutorial](tutorial.md#step-5-enable-github-pages) for details.

## Configuration (`pyproject.toml`)

Tool configuration lives in `pyproject.toml`:

- **Dependency groups**: `dev` (includes lint, test, typecheck), `docs` (zensical, mkdocstrings)
- **Ruff**: line length 120, rules for pycodestyle, Pyflakes, isort, flake8-bugbear, pyupgrade
- **ty**: all rules enabled as errors by default. To relax a rule, uncomment the example in `[tool.ty]`
- **uv**: package mode enabled, dev groups installed by default
