# Cookiecutter PyPackage

[![PyPI version](https://img.shields.io/pypi/v/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)
[![PyPI downloads](https://img.shields.io/pypi/dm/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package.

*   GitHub repo: [https://github.com/audreyfeldroy/cookiecutter-pypackage/](https://github.com/audreyfeldroy/cookiecutter-pypackage/)
*   Documentation: [https://cookiecutter-pypackage.readthedocs.io/](https://cookiecutter-pypackage.readthedocs.io/)
*   Free software: BSD license
*   Discord: [https://discord.gg/PWXJr3upUE](https://discord.gg/PWXJr3upUE)

## Features

*   Testing setup with pytest
*   GitHub Actions testing: Setup to easily test for Python 3.12 and 3.13
*   [bump2version](https://github.com/c4urself/bump2version): Pre-configured version bumping with a single command
*   Auto-release to [PyPI](https://pypi.python.org/pypi) when you push a new tag to master (optional)
*   Command line interface using Typer

## Quickstart

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher):

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

For more details, see the [cookiecutter-pypackage tutorial](https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html).

## Not Exactly What You Want?

Don't worry, you have options:

### Similar Cookiecutter Templates

*   [Nekroze/cookiecutter-pypackage](https://github.com/Nekroze/cookiecutter-pypackage): A fork of this with a PyTest test runner,
    strict flake8 checking with Travis/Tox, and some docs and `setup.py` differences.
*   [tony/cookiecutter-pypackage-pythonic](https://github.com/tony/cookiecutter-pypackage-pythonic): Fork with py2.7+3.3 optimizations.
    Flask/Werkzeug-style test runner, `_compat` module and module/doc conventions.
    See `README.rst` or the [github comparison view](https://github.com/tony/cookiecutter-pypackage-pythonic/compare/audreyr:master...master) for exhaustive list of
    additions and modifications.
*   [ardydedase/cookiecutter-pypackage](https://github.com/ardydedase/cookiecutter-pypackage): A fork with separate requirements files rather than a requirements list in the `setup.py` file.
*   [lgiordani/cookiecutter-pypackage](https://github.com/lgiordani/cookiecutter-pypackage): A fork of Cookiecutter that uses [Punch](https://github.com/lgiordani/punch) instead of [bump2version](https://github.com/c4urself/bump2version) and with separate requirements files.
*   [briggySmalls/cookiecutter-pypackage](https://github.com/briggySmalls/cookiecutter-pypackage): A fork using [Poetry](https://python-poetry.org/) for neat package management and deployment, with linting, formatting, no makefiles and more.
*   [veit/cookiecutter-namespace-template](https://github.com/veit/cookiecutter-namespace-template): A cookiecutter template for python modules with a namespace
*   [zillionare/cookiecutter-pypackage](https://zillionare.github.io/cookiecutter-pypackage/): A template containing [Poetry](https://python-poetry.org/), [Mkdocs](https://pypi.org/project/mkdocs/), Github CI and many more. It's a template and a package also (can be installed with `pip`)
*   [waynerv/cookiecutter-pypackage](https://waynerv.github.io/cookiecutter-pypackage/): A fork using [Poetry](https://python-poetry.org/), [Mkdocs](https://pypi.org/project/mkdocs/), [Pre-commit](https://pre-commit.com/), [Black](https://black.readthedocs.io/en/stable/) and [Mypy](https://mypy.readthedocs.io/en/stable/). Run test, staging and release workflows with GitHub Actions, automatically generate release notes from CHANGELOG.
*   [x-pt/template](https://github.com/x-pt/template): A CookieCutter-based template designed to serve as a robust starting point for most startup projects hosted on GitHub, supporting `Python`, `C++/CUDA`, `Rust`, `Golang`, `TypeScript`.
*   Also see the [network](https://github.com/audreyr/cookiecutter-pypackage/network) and [family tree](https://github.com/audreyr/cookiecutter-pypackage/network/members) for this repo. (If you find
    anything that should be listed here, please add it and send a pull request!)

### Fork This / Create Your Own

If you have differences in your preferred setup, I encourage you to fork this
to create your own version. Or create your own; it doesn't strictly have to
be a fork.

*   Once you have your own version working, add it to the Similar Cookiecutter
    Templates list above with a brief description.
*   It's up to you whether or not to rename your fork/own version. Do whatever
    you think sounds good.

### Or Submit a Pull Request

I also accept pull requests on this, if they're small, atomic, and if they
make my own packaging experience better.
