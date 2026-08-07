# Project Structure

After generating your package, you'll have a project that looks like this:

```
my-package/
├── .github/
│   ├── dependabot.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── config.yml
│   │   └── feature_request.yml
│   ├── pull_request_template.md
│   └── workflows/
│       ├── ci.yml          # Lint, type check, test
│       ├── codeql.yml      # Security analysis
│       ├── docs.yml        # Build and deploy docs
│       ├── publish.yml     # Publish to PyPI on tag
│       └── zizmor.yml      # Workflow security audit
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
├── scripts/
│   └── release.py          # Version bump, finalize notes, tag, and push
├── .editorconfig
├── .gitignore
├── CHANGELOG/
│   ├── unreleased.md        # Work-in-progress release notes
│   └── X.Y.Z.md             # Immutable notes for each published release
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── justfile                # Task runner commands
├── LICENSE
├── pyproject.toml          # Package metadata and tool config
├── README.md
├── SECURITY.md
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
| `just fix` | Apply Ruff formatting and safe lint fixes |
| `just check` | Verify formatting, linting, types, and Python 3.14 tests without modifying source files |
| `just fix-and-check` | Apply automatic fixes, then run the local quality gate |
| `just test` | Run tests only |
| `just testall` | Run tests on Python 3.12, 3.13, and 3.14 |
| `just type-check` | Type-check with ty |
| `just type-check-watch` | Type-check in watch mode |
| `just docs-serve` | Preview docs locally at http://localhost:8000 |
| `just docs-build` | Build docs |
| `just coverage` | Run tests with coverage and generate HTML report |
| `just release` | Finalize notes, tag the current version, and push to GitHub |
| `just build` | Build sdist and wheel |

## GitHub Actions workflows

Your project includes CI, publish, documentation, and Dependabot workflows, all security-hardened out of the box. See [GitHub Actions Workflows](github_actions.md) for details.

## Documentation site

The docs site is built with [Zensical](https://zensical.org/) and configured in `zensical.toml`. It uses the Material theme with light/dark mode.

The API reference page (`docs/api.md`) auto-generates documentation from your docstrings using [mkdocstrings](https://mkdocstrings.github.io/). Write docstrings in your code and they'll appear on the docs site automatically.

Public GitHub setup enables Pages by default. Private setup asks separately and
defaults to off because the resulting site can still be public and the feature
may require a paid GitHub plan. If Pages was not enabled, review those
visibility implications, then go to your repository's Settings > Pages and set
the source to **GitHub Actions**. Finally, set the repository variable
`DOCS_DEPLOYMENT_ENABLED` to `true`; until then, the deployment workflow stays
paused and local docs commands continue to work.

## Configuration (`pyproject.toml`)

Tool configuration lives in `pyproject.toml`:

- **Dependency groups**: `dev` (includes lint, test, typecheck), `docs` (zensical, mkdocstrings)
- **Ruff**: line length 120, rules for pycodestyle, Pyflakes, isort, flake8-bugbear, pyupgrade
- **ty**: all rules enabled as errors by default. To relax a rule, uncomment the example in `[tool.ty]`
- **uv**: package mode enabled, dev groups installed by default
