# Tutorial

By the end of this tutorial, you'll have a Python package with a working CLI, a live documentation site, and CI that tests, lints, type-checks, and publishes to PyPI. The whole thing takes about 15 minutes.

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [just](https://github.com/casey/just#installation) (task runner)
- [git](https://git-scm.com/)
- [gh](https://cli.github.com/) (GitHub CLI, for automatic repo and Pages setup)
- A [GitHub account](https://github.com/)
- A [PyPI account](https://pypi.org/) (when you're ready to publish)

## Step 1: Generate your package

```bash
uvx cookiecutter-pypackage
```

You'll be prompted for some values. See [Prompts](prompts.md) for details on each one.

```
[1/11] full_name (Audrey M. Roy Greenfeld): Your Name
[2/11] email (audreyfeldroy@example.com): you@example.com
[3/11] github_username (audreyfeldroy): your-github-username
[4/11] github_repo_owner (your-github-username):
[5/11] project_name (Python Boilerplate): My Package
[6/11] package_name (My-Package): my-package
[7/11] import_name (my_package):
[8/11] project_short_description (...): A short description of your package.
[9/11] pypi_username (your-github-username):
[10/11] author_website ():
[11/11] first_version (0.1.0):
```

The hook will ask whether to make the GitHub repo public or private, then set everything up:

```
Make the GitHub repo public or private? [public/private] (public): public
GitHub repo created: https://github.com/your-username/my-package
GitHub Pages enabled for your-username/my-package (source: GitHub Actions)
GitHub environment 'pypi' created for your-username/my-package
Git initialized with initial commit
Pushed to https://github.com/your-username/my-package

To publish to PyPI, add a pending publisher at:
https://pypi.org/manage/account/publishing/
...

Your Python package project has been created successfully!
```

CI runs automatically on push. Check the Actions tab and you should see it pass: linting, type checking, and tests across three Python versions. Your docs site will be live at `https://your-username.github.io/my-package/` within a couple of minutes.

If you don't have the `gh` CLI, the hook skips repo creation and prints manual instructions instead.

## Step 2: Look around

```bash
cd my-package
```

Here's what you got:

| Path | What it does |
|---|---|
| `src/my_package/` | Your Python package code |
| `src/my_package/cli.py` | Typer CLI (run with `uv run my-package`) |
| `src/my_package/utils.py` | Placeholder for utility functions (rename or delete) |
| `src/my_package/py.typed` | Marker that tells tools your package has type annotations |
| `tests/` | pytest test suite |
| `docs/` | Documentation source (builds with Zensical) |
| `justfile` | Task runner commands (run `just list` to see them all) |
| `.github/workflows/` | CI, PyPI publishing, and docs deployment |
| `pyproject.toml` | Package metadata, dependencies, and tool configuration |

The project uses a `src` layout, meaning your package code lives under `src/` rather than at the root. This prevents accidentally importing local code during testing.

## Step 3: Install and verify

```bash
uv sync
just qa
```

`just qa` formats your code with ruff, lints it, type-checks with ty, and runs tests. If ruff reformats any files, that's expected. You should see all checks pass.

Try the CLI:

```bash
uv run my-package
uv run my-package --help
```

You can also run it as a module: `uv run python -m my_package`.

Run `just list` to see all available commands.

## Step 4: Preview docs locally

```bash
just docs-serve
```

This starts a local server at http://localhost:8000 with live reload. Edit a doc, save, and watch it update. The API reference page auto-generates documentation from your docstrings.

## Step 5: Write some code

Open `src/my_package/utils.py` and replace the placeholder:

```python
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
```

Add a test in `tests/test_my_package.py`:

```python
from my_package.utils import add

def test_add():
    assert add(1, 2) == 3
```

Run `just qa` to verify everything still passes. Push your changes and watch CI confirm it on GitHub too.

## Step 6: Set up PyPI publishing

The post-generation hook printed the URL and form values you need:

```
To publish to PyPI, add a pending publisher at:
https://pypi.org/manage/account/publishing/

Fill in these values:
  PyPI project name:  my-package
  Owner:              your-username
  Repository:         my-package
  Workflow:           publish.yml
  Environment:        pypi

Then release with:
  just release
```

Go to that URL, fill in those values, and you're done. This uses OIDC (Trusted Publishers) so there are no API tokens to manage. See the [PyPI Release Checklist](pypi_release_checklist.md) for more details.

## Step 7: Release

```bash
just release
```

This bumps the version, tags it, pushes, and GitHub Actions builds, signs with Sigstore, and publishes to PyPI automatically. Check the Actions tab to confirm.
