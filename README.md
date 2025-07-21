# Cookiecutter PyPackage

[![PyPI version](https://img.shields.io/pypi/v/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)
[![PyPI downloads](https://img.shields.io/pypi/dm/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package.

*   GitHub repo: [https://github.com/audreyfeldroy/cookiecutter-pypackage/](https://github.com/audreyfeldroy/cookiecutter-pypackage/)
*   Free software: MIT license
*   Discord: [https://discord.gg/PWXJr3upUE](https://discord.gg/PWXJr3upUE)

## Features

*   Testing setup with pytest
*   GitHub Actions testing: Setup to easily test for Python 3.10, 3.11, 3.12, and 3.13
*   Auto-release to [PyPI](https://pypi.python.org/pypi) when you push a new tag to master (optional)
*   Command line interface using Typer

## Quickstart

Install the latest Cookiecutter if you haven't installed it yet:

```bash
pip install -U cookiecutter
```

Generate a Python package project:

```bash
cookiecutter https://github.com/audreyfeldroy/cookiecutter-pypackage.git
```

Then:

*   Create a repo and put it there.
*   [Register](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives) your project with PyPI.
*   Add the repo to your [Read the Docs](https://readthedocs.io/) account + turn on the Read the Docs service hook.
*   Release your package by pushing a new tag to master.

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
