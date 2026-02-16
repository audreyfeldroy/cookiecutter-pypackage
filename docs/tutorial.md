# Tutorial

> **Note:** Did you find any of these instructions confusing? [Edit this file](https://github.com/audreyfeldroy/cookiecutter-pypackage/blob/main/docs/tutorial.md) and submit a pull request with your improvements!

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [just](https://github.com/casey/just#installation) (task runner)
- [git](https://git-scm.com/)
- A [GitHub account](https://github.com/)
- A [PyPI account](https://pypi.org/) (when you're ready to publish)

## Step 1: Generate your package

```bash
uvx cookiecutter-pypackage
```

You'll be prompted for some values. See [Prompts](prompts.md) for details on each one.

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

You should see "Your Python package project has been created successfully!" and a new `my-package/` directory.

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

## Step 4: Create a GitHub repo and push

```bash
git init -b main
git add .
git commit -m "Initial commit"
```

Create a repo on GitHub (or use `gh repo create`), then push:

```bash
git remote add origin git@github.com:your-username/my-package.git
git push -u origin main
```

CI will run automatically on push. You should see it pass in the Actions tab.

## Step 5: Enable GitHub Pages

Go to your repo's Settings > Pages (or visit `https://github.com/your-username/my-package/settings/pages`) and set the source to **GitHub Actions**.

Then re-run the docs workflow that failed on the first push: go to Actions, find "Documentation", and click "Re-run all jobs."

Your docs site will be live at `https://your-username.github.io/my-package/` within a couple of minutes.

## Step 6: Preview docs locally

```bash
just docs-serve
```

This starts a local server at http://localhost:8000 with live reload. The API reference page auto-generates documentation from your docstrings.

## Step 7: Write some code

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

Run `just qa` to verify everything still passes.

## Step 8: Set up PyPI publishing

Follow the [PyPI Release Checklist](pypi_release_checklist.md) to configure Trusted Publishing. This uses OIDC so there are no API tokens to manage. If you get the configuration wrong, you can delete and recreate it on PyPI.

## Step 9: Release

1. Update `HISTORY.md` with your changes.

2. Bump the version and commit:

    ```bash
    uv version patch
    git add -A
    git commit -m "Release $(grep -m1 '^version' pyproject.toml | sed -E 's/version = "(.*)"/\1/')"
    ```

3. Tag and push:

    ```bash
    just tag
    ```

    `just tag` reads the version from `pyproject.toml`, creates an annotated git tag, and pushes it. Make sure your branch is pushed first.

4. GitHub Actions builds and publishes to PyPI automatically. Check the Actions tab to confirm.
