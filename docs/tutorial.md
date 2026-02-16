# Tutorial

> **Note:** Did you find any of these instructions confusing? [Edit this file](https://github.com/audreyfeldroy/cookiecutter-pypackage/blob/main/docs/tutorial.md) and submit a pull request with your improvements!

## Prerequisites

You will need:

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- A [GitHub account](https://github.com/)
- A [PyPI account](https://pypi.org/) (when you're ready to publish)

## Step 1: Generate your package

```bash
uvx cookiecutter-pypackage
```

You'll be prompted for some values. See [Prompts](prompts.md) for details on each one.

## Step 2: Create a GitHub repo

```bash
cd my-package
git init
git add .
git commit -m "Initial commit"
```

Create a repo on GitHub (or use `gh repo create`), then push:

```bash
git remote add origin git@github.com:your-username/my-package.git
git push -u origin main
```

## Step 3: Install and run tests

```bash
uv sync
just qa
```

This formats, lints, type-checks, and tests your package.

## Step 4: Enable GitHub Pages

Go to your repo's Settings > Pages and set the source to **GitHub Actions**. The docs workflow will deploy your documentation site on every push to `main`.

## Step 5: Preview your docs locally

```bash
just docs-serve
```

This starts a local server at http://localhost:8000 with live reload. Your API reference page auto-generates documentation from your docstrings.

## Step 6: Set up PyPI publishing

Follow the [PyPI Release Checklist](pypi_release_checklist.md) to configure Trusted Publishing. Once set up, release your package:

```bash
uv version patch
git commit -am "Release 0.1.1"
just tag
```

GitHub Actions handles the rest.
