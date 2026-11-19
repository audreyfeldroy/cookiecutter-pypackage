# Tutorial

By the end of the local steps, you'll have a Python package with a working CLI,
tests, and documentation you can preview locally. If you opt into GitHub setup,
you'll also have CI and can publish the documentation with GitHub Pages. Plan
on about 15 minutes for the local foundation; GitHub Pages, trusted-publisher
setup, and a first PyPI release can take longer.

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [just](https://github.com/casey/just#installation) (task runner)
- [git](https://git-scm.com/)
- [gh](https://cli.github.com/) (GitHub CLI, if you want automatic repo setup)
- A [GitHub account](https://github.com/)
- A [PyPI account](https://pypi.org/) (when you're ready to publish)

The generated project supports Python 3.12 and newer, while its local
`just check` command explicitly runs on Python 3.14. If Python 3.14 is not
already installed, uv may download a managed Python installation automatically,
so the first check needs network access.

## Step 1: Generate your package

```bash
uvx cookiecutter-pypackage
```

To test an unreleased branch or pull request, pin the generator to an exact
commit so the result is repeatable:

```bash
uvx \
  --from git+https://github.com/audreyfeldroy/cookiecutter-pypackage.git@<commit> \
  cookiecutter-pypackage
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
[10/11] author_website (https://audrey.feldroy.com/): https://example.com
[11/11] first_version (0.1.0):
```

GitHub setup is optional and defaults to no. If you opt in, repository
visibility defaults to private and the generator shows every action before
making changes:

```
Set up a GitHub repository now? [y/N]: y
Repository visibility [private/public] (private): public
Enable GitHub Pages? [Y/n]:

GitHub setup plan:
  - create https://github.com/your-username/my-package as a public repository
  - initialize Git and create the first commit
  - enable GitHub Pages (publishes a website)
  - enable the documentation deployment workflow
  - create the pypi environment
  - push main over SSH

Continue? [y/N]: y
Git initialized with first commit
GitHub repository created: https://github.com/your-username/my-package
GitHub Pages enabled for your-username/my-package
Documentation deployment workflow enabled for your-username/my-package
GitHub environment 'pypi' created for your-username/my-package
Pushed to https://github.com/your-username/my-package

To publish to PyPI, add a pending publisher at:
https://pypi.org/manage/account/publishing/
...

Your Python package project has been created successfully!
```

The transport in the plan follows `gh`'s `git_protocol` setting, so it may say
SSH or HTTPS. CI runs automatically on push. Check the Actions tab and you
should see it pass: linting, type checking, and tests across three Python
versions. Your docs site will be live at
`https://your-username.github.io/my-package/` within a couple of minutes.

Pressing Enter at the first GitHub question generates the project locally
without creating a repository or Git commit. If you opt in but `gh` is
unavailable, unauthenticated, or another requested action fails, the command
exits nonzero and keeps the generated directory so you can inspect or recover
the partial setup.

For a private repository, Pages defaults to off. GitHub Pages can publish a
public website even when its repository is private, and Pages for a private
repository may require a paid plan. The interactive flow explains this and
requires a separate opt-in before enabling Pages. If you leave Pages off, the
documentation deployment workflow stays paused rather than failing on the
first push; local docs preview and builds still work.

For non-interactive automation, make the opt-in explicit:

```bash
uvx cookiecutter-pypackage --no-input --github private \
    full_name="Your Name" \
    email="you@example.com" \
    github_username=yourhandle \
    author_website="" \
    project_name="My Package" \
    package_name=my-package
```

Use `--github public` when automation should also enable Pages and
documentation deployment.

Record the exact generation command and inputs in your project notes or README,
especially when using an unreleased commit. This makes it possible to identify
the template version and choices that produced the project later.

## Step 2: Look around

```bash
cd my-package
```

If you skipped automatic GitHub setup (the default), initialize Git and create
the first commit now:

```bash
git init -b main
git add .
git commit \
  -m "Initialize My Package with Cookiecutter PyPackage" \
  -m "Generated from https://github.com/audreyfeldroy/cookiecutter-pypackage"
```

If you pinned generation to an unreleased commit, use that exact commit URL in
the message body. A descriptive first commit preserves where the boilerplate
came from and makes later template-specific debugging much easier.

If you opted into GitHub setup, the generator already performed these steps and
pushed the first commit.

Here's what you got:

| Path | What it does |
|---|---|
| `src/my_package/` | Your Python package code |
| `src/my_package/cli.py` | Typer CLI (run with `uv run my_package`) |
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
just fix-and-check
```

`just fix-and-check` applies Ruff's automatic formatting and lint fixes, then runs the local quality gate: formatting and lint checks, ty, and tests on Python 3.14. Use `just check` when you only want read-only verification; use `just testall` for the local Python 3.12, 3.13, and 3.14 test matrix.

`uv sync` creates or updates `uv.lock`. Keep that file under version control and
include it in your next commit so collaborators and CI resolve the same
environment.

Try the CLI:

```bash
uv run my_package
uv run my_package --help
```

You can also run it as a module: `uv run python -m my_package`.

Run `just list` to see all available commands.

## Step 4: Preview docs locally

```bash
just docs-serve
```

This starts a local server at http://localhost:8000 with live reload. It occupies
port 8000 until you stop it with Ctrl+C. Edit a doc, save, and watch it update.
The API reference page auto-generates documentation from your docstrings.

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

Run the checks and commit the change:

```bash
just check
git add src/my_package/utils.py tests/test_my_package.py uv.lock
git commit -m "Add addition helper"
```

If you opted into GitHub setup, push to the remote that the generator created:

```bash
git push
```

If you stayed on the default local-only path, create a GitHub repository when
you are ready and push the existing `main` branch:

```bash
gh repo create my-package --private --source=. --remote=origin --push
```

Use `--public` instead of `--private` if that is what you intend. If you do not
use `gh`, create an empty repository on GitHub, then connect and push it:

```bash
git remote add origin <repository-url>
git push -u origin main
```

Once pushed, CI confirms the full Python-version matrix on GitHub. Pages and
trusted-publisher setup still require the additional configuration described
below.

## Step 6: Publish docs with GitHub Pages

If automatic public GitHub setup completed successfully, Pages and the
documentation workflow are already enabled. Verify the result at
`https://OWNER.github.io/REPOSITORY/` and continue to the next step.

If you created or connected the repository manually, enable Pages with GitHub
Actions as its source, enable the guarded documentation workflow, and trigger
its first run:

```bash
gh api --method POST repos/OWNER/REPOSITORY/pages -f build_type=workflow
gh variable set DOCS_DEPLOYMENT_ENABLED \
  --repo OWNER/REPOSITORY \
  --body true
gh workflow run docs.yml --repo OWNER/REPOSITORY --ref main
```

If the first command reports that a Pages site already exists, run it again
with `--method PUT`. A private repository's Pages site may be public and may
require a paid GitHub plan, so review those visibility implications before
enabling it.

Watch the Documentation workflow in GitHub Actions. Do not treat setup as
complete until the workflow succeeds and the public URL returns the generated
site.

## Step 7: Set up PyPI publishing

If you opted into GitHub setup, the post-generation hook printed the URL and
form values you need:

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

If you skipped automatic GitHub setup, create the environment referenced by the
publishing workflow before submitting the PyPI form:

```bash
gh api --method PUT repos/OWNER/REPOSITORY/environments/pypi
```

## Step 8: Release

As you work, record user-visible changes in `CHANGELOG/unreleased.md`.

For the first release, `pyproject.toml` already contains the `first_version`
chosen during generation. Confirm it and keep it when that is the version you
intend to publish:

```bash
uv version
```

For later releases, bump the existing version and commit it first:

```bash
uv version <version>        # or: uv version --bump minor
git add pyproject.toml uv.lock
git commit -m "Bump version to <version>"
```

Run the local release checks, including a documentation build before the
distribution build:

```bash
just check
just docs-build
just build
```

Then release:

```bash
just release
```

`just release` finalizes the unreleased notes, commits and pushes that notes
commit, creates the `v<version>` tag and GitHub Release, and then GitHub Actions
builds, signs with Sigstore, and publishes to PyPI automatically.

Do not call the release complete when the tag appears. Wait for the Publish to
PyPI workflow to succeed, then verify the GitHub Release and install the exact
registry version in an isolated environment. For the default tutorial values:

```bash
gh run list --workflow publish.yml --limit 1
gh release view v0.1.0
uv run --isolated --no-project --with my-package==0.1.0 \
  python -c "import importlib.metadata; print(importlib.metadata.version('my-package'))"
uv run --isolated --no-project --with my-package==0.1.0 my_package --help
```

The version command must print `0.1.0`, and the CLI help must run from the
published package rather than the local checkout. Also confirm that the PyPI
project page lists both the wheel and source archive.
