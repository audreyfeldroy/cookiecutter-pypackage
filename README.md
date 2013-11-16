# cookiecutter-pypackage

[Cookiecutter](http://cookiecutter.rtfd.org) template for a Python package.
Based on <https://github.com/audreyr/cookiecutter-pypackage>.

## Features
- Optional sample CLI with docopt
- Testing with unittest2 and nosetests
- [TravisCI](http://travis-ci.org/): Ready for Travis Continuous Integration testing
- [Tox](http://testrun.org/tox/) testing: Setup to easily test for
  Python 2.6, 2.7, 3.3
- [Sphinx](http://sphinx-doc.org/) docs: Documentation ready for
  generation with, for example, [ReadTheDocs](https://readthedocs.org/)
- Used by [changes](http://changes.rtfd.org) to generate new packages

## Usage

Generate a Python package project:

    cookiecutter https://github.com/michaeljoseph/cookiecutter-pypackage.git
