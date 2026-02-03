# Cookiecutter PyPackage

[![PyPI version](https://img.shields.io/pypi/v/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)
[![PyPI downloads](https://img.shields.io/pypi/dm/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package.

*   GitHub repo: [https://github.com/audreyfeldroy/cookiecutter-pypackage/](https://github.com/audreyfeldroy/cookiecutter-pypackage/)
*   Free software: MIT license
*   Discord: [https://discord.gg/PWXJr3upUE](https://discord.gg/PWXJr3upUE)

## Features

*   Modern tooling: [uv](https://docs.astral.sh/uv/) for dependency management, [justfile](https://github.com/casey/just) for task running
*   Testing with pytest, GitHub Actions for Python 3.10, 3.11, 3.12, 3.13, and 3.14
*   Auto-release to [PyPI](https://pypi.python.org/pypi) via Trusted Publishers when you push a tag
*   Command line interface using [Typer](https://typer.tiangolo.com/)

## Quickstart

First, install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you haven't already.

Generate a new Python package:

```bash
uvx cookiecutter-pypackage
```

You'll be prompted for some values:

```
[1/9] full_name (Audrey M. Roy Greenfeld): Your Name
[2/9] email (audreyfeldroy@example.com): you@example.com
[3/9] github_username (audreyfeldroy): your-github-username
[4/9] pypi_package_name (python-boilerplate): my-package
[5/9] project_name (Python Boilerplate): My Package
[6/9] project_slug (my_package):
[7/9] project_short_description (...): A short description of your package.
[8/9] pypi_username (your-github-username):
[9/9] first_version (0.1.0):
```

<details>
<summary>Traditional way (without uvx)</summary>

```bash
uv venv
source .venv/bin/activate
uv pip install cookiecutter
cookiecutter gh:audreyfeldroy/cookiecutter-pypackage
```

</details>

Then:

*   Create a GitHub repo and push your code
*   Set up [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) for your repo
*   Release your package by pushing a tag: `git tag v0.1.0 && git push --tags`

## Not Exactly What You Want?

Don't worry, you have options:

### Fork This / Create Your Own

If you have differences in your preferred setup, I encourage you to fork this
to create your own version. Or create your own; it doesn't strictly have to
be a fork.

### Similar Cookiecutter Templates

Explore other forks to get ideas. See the [network](https://github.com/audreyfeldroy/cookiecutter-pypackage/network) and [family tree](https://github.com/audreyfeldroy/cookiecutter-pypackage/network/members) for this repo.

### Or Submit a Pull Request

I also accept pull requests on this, if they're small, atomic, and if they
make my own packaging experience better.
