# Python Package | Cookiecutter Project Template

*Cookiecutter template for a Python package.*

[![Build Status](https://travis-ci.org/CiscoSE/cc-pypackage.svg?branch=master)](https://travis-ci.org/CiscoSE/cc-pypackage)

This [Cookiecutter](https://github.com/audreyr/cookiecutter) template is a fork of the excellent [Cookiecutter-PyPackage](https://github.com/audreyr/cookiecutter-pypackage) project template - adapted for Cisco SE use by licensing the generated project under the [Cisco Sample Code License](./LICENSE).

## Motivation

Starting a new Python Package project, with all the usual bells and whistles, involves a lot of boilerplate code and documentation starters that only vary based on a few input parameters:  project name, slug, usernames, etc.  [Cookiecutter](https://github.com/audreyr/cookiecutter) makes generating these boilerplate files a breeze.

## Features

- Testing setup with ``unittest`` and ``python setup.py test`` or ``py.test``
- [Travis-CI]: Ready for Travis Continuous Integration testing
- [Tox] testing: Setup to easily test for Python 2.7, 3.4, 3.5, 3.6
- [Sphinx] docs: Documentation ready for generation with, for example, [ReadTheDocs]
- [Bumpversion]: Pre-configured version bumping with a single command
- Auto-release to [PyPI] when you push a new tag to master (optional)
- Command line interface using [Click] (optional)

## Quickstart

Install the latest Cookiecutter if you haven't installed it yet (this requires Cookiecutter 1.4.0 or higher):

```bash
pip install -U cookiecutter
```

If you need a bit more help than that, see [Installation](https://cookiecutter.readthedocs.io/en/latest/installation.html) in the Cookiecutter docs.

### Using the PyPackage Template

#### The First Time

```bash
$ cookiecutter https://github.com/CiscoSE/cc-pypackage
```

...or using abbreviated syntax:

```bash
$ cookiecutter gh:CiscoSE/cc-pypackage
```

#### Thereafter

```bash
$ cookiecutter cc-pypackage
```

## Looking for more Information?

Please see the [PyPackage Tutorial](https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html) for the original PyPackage template.  If you have questions about using the Cookiecutter tool itself, please see the [Cookiecutter docs](https://cookiecutter.readthedocs.io).

## Support?

Did we break something?  If you are experiencing an issue with this fork of the PyPackage template, please open an [issue](https://github.com/CiscoSE/cc-pypackage/issues).

## Who is this for?

This project template is for use by **Cisco Systems Engineers** who are creating example and demonstration code *(aka. Cisco Sample Code)* and sharing it with Cisco's customers and partners for use with Cisco products and services.  **The Cisco Sample Code License is for use in Cisco Repositories Only.**  It is not an Open Source license. The license should only be used by Cisco and/or its affiliates to post and share Cisco Sample Code.

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[Travis-CI]: http://travis-ci.org/
[Tox]: http://testrun.org/tox/
[Sphinx]: http://sphinx-doc.org/
[ReadTheDocs]: https://readthedocs.io/
[pyup.io]: https://pyup.io/
[Bumpversion]: https://github.com/peritus/bumpversion
[Punch]: https://github.com/lgiordani/punch
[PyPi]: https://pypi.python.org/pypi
