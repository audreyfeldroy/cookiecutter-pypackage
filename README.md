# Cookiecutter PyMod

[![Updates](https://pyup.io/repos/github/ashwinvis/cookiecutter-pymod/shield.svg)](https://pyup.io/repos/github/ashwinvis/cookiecutter-pymod/)

[![image](https://travis-ci.org/ashwinvis/cookiecutter-pymod.svg?branch=master)](https://travis-ci.org/ashwinvis/cookiecutter-pymod)

[Cookiecutter](https://github.com/audreyr/cookiecutter) template for a
**Py**thon package with some **Mod**ern twists:

  - Primarily uses
    [setup.cfg](https://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=setup.cfg#configuring-setup-using-setup-cfg-files)
    for storing packaging metadata instead of relying on
    `setup.py` too much.
  - Relies on [src](https://hynek.me/articles/testing-packaging/) layout
    for the package.
  - Support `setuptools_scm` versioning for development.
  - Uses markdown for the `README.md` etc. instead of reStructured Text.
  - Allows project name, repo name and package name to be different (for
    e.g. having something like "Scikit Learn", `scikit-learn` and
    `sklearn` respectively).
  - Adds optional support for either an `argparse` based command-line
    tool, or a `Click` based one (only the latter was available in the
    original template).
  - By default `python_requires>=3.6` is preferred, since new packages
    should be able to use
    [f-strings](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals).

**TLDR:** you get this:

``` shell
my-project/
├── AUTHORS.md
├── CONTRIBUTING.md
├── docs
│   └── ...
├── HISTORY.md
├── LICENSE
├── Makefile
├── MANIFEST.in
├── README.md
├── setup.cfg
├── setup.py
├── src
│   └── my_project
│       ├── cli.py
│       ├── my_project.py
│       └── __init__.py
├── tests
│   └── ...
└── tox.ini
```

## See Also

  - GitHub repo: <https://github.com/ashwinvis/cookiecutter-pymod/>
  - Documentation: <https://cookiecutter-pypackage.readthedocs.io/>
  - Free software: BSD license

## Features

  - Testing setup with `unittest` and `python setup.py test` or
    `py.test`
  - [Travis-CI](http://travis-ci.org/): Ready for Travis Continuous
    Integration testing
  - [Tox](http://testrun.org/tox/) testing: Setup to easily test for
    Python 2.7, 3.4, 3.5, 3.6
  - [Sphinx](http://sphinx-doc.org/) docs: Documentation ready for
    generation with, for example, [ReadTheDocs](https://readthedocs.io/)
  - [Bumpversion](https://github.com/peritus/bumpversion):
    Pre-configured version bumping with a single command
  - Auto-release to [PyPI](https://pypi.python.org/pypi) when you push a
    new tag to master (optional)
  - Command line interface using Click (optional)

## Build Status

Linux:

[![Linux build status on Travis
CI](https://img.shields.io/travis/ashwinvis/cookiecutter-pymod.svg)](https://travis-ci.org/ashwinvis/cookiecutter-pymod)

Windows:

[![Windows build status on
Appveyor](https://ci.appveyor.com/api/projects/status/github/ashwinvis/cookiecutter-pymod?branch=master&svg=true)](https://ci.appveyor.com/project/ashwinvis/cookiecutter-pymod/branch/master)

## Quickstart

Install the latest Cookiecutter if you haven't installed it yet (this
requires Cookiecutter 1.4.0 or higher):

    pip install -U cookiecutter

Generate a Python package project:

    cookiecutter https://github.com/ashwinvis/cookiecutter-pymod.git

Then:

  - Create a repo and put it there.
  - Add the repo to your [Travis-CI](http://travis-ci.org/) account.
  - Install the package into a virtualenv. (`pip install -e '.[dev]'` or
    `make develop`)
  - [Register](https://packaging.python.org/distributing/#register-your-project)
    your project with PyPI.
  - Run the Travis CLI command `travis encrypt
    --add deploy.password` to encrypt your PyPI password in Travis
    config and activate automated deployment on PyPI when you push a new
    tag to master branch.
  - Add the repo to your [ReadTheDocs](https://readthedocs.io/) account
    + turn on the ReadTheDocs service hook.
  - Release your package by pushing a new tag to master.
  - Add a `requirements.txt` file that
    specifies the packages you will need for your project and their
    versions. For more info see the [pip docs for requirements
    files](https://pip.pypa.io/en/stable/user_guide/#requirements-files).
  - Activate your project on [pyup.io](https://pyup.io/).

For more details, see the [cookiecutter-pypackage
tutorial](https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html).

## Not Exactly What You Want?

Don't worry, you have options:

### Similar Cookiecutter Templates

  - [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage):
    The original cookiecutter template.
  - [Nekroze/cookiecutter-pypackage](https://github.com/Nekroze/cookiecutter-pypackage):
    A fork of this with a PyTest test runner, strict flake8 checking
    with Travis/Tox, and some docs and `setup.py` differences.
  - [tony/cookiecutter-pypackage-pythonic](https://github.com/tony/cookiecutter-pypackage-pythonic):
    Fork with py2.7+3.3 optimizations. Flask/Werkzeug-style test runner,
    `_compat` module and module/doc conventions. See `README.rst` or the
    [github comparison
    view](https://github.com/tony/cookiecutter-pypackage-pythonic/compare/audreyr:master...master)
    for exhaustive list of additions and modifications.
  - [ardydedase/cookiecutter-pypackage](https://github.com/ardydedase/cookiecutter-pypackage):
    A fork with separate requirements files rather than a requirements
    list in the `setup.py` file.
  - [lgiordani/cookiecutter-pypackage](https://github.com/lgiordani/cookiecutter-pypackage):
    A fork of Cookiecutter that uses
    [Punch](https://github.com/lgiordani/punch) instead of
    [Bumpversion](https://github.com/peritus/bumpversion) and with
    separate requirements files.
  - Also see the
    [network](https://github.com/ashwinvis/cookiecutter-pymod/network)
    and [family
    tree](https://github.com/ashwinvis/cookiecutter-pymod/network/members)
    for this repo. (If you find anything that should be listed here,
    please add it and send a pull request\!)

### Fork This / Create Your Own

If you have differences in your preferred setup, I encourage you to fork
this to create your own version. Or create your own; it doesn't strictly
have to be a fork.

  - Once you have your own version working, add it to the Similar
    Cookiecutter Templates list above with a brief description.
  - It's up to you whether or not to rename your fork/own version. Do
    whatever you think sounds good.

### Or Submit a Pull Request

I also accept pull requests on this, if they're small, atomic, and if
they make my own packaging experience better.
