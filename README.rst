======================
Cookiecutter PyPackage
======================

.. image:: https://img.shields.io/travis/briggySmalls/cookiecutter-pypackage.svg
    :target: https://travis-ci.org/briggySmalls/cookiecutter-pypackage
    :alt: Linux build status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/briggySmalls/cookiecutter-pypackage?branch=master&svg=true
    :target: https://ci.appveyor.com/project/briggySmalls/cookiecutter-pypackage/branch/master
    :alt: Windows build status on Appveyor

Cookiecutter_ template for a Python package, forked from `audreyr/cookiecutter-pypackage`_.

* GitHub repo: https://github.com/briggySmalls/cookiecutter-pypackage/
* Documentation: https://briggysmalls.github.io/cookiecutter-pypackage/
* Free software: BSD license

.. _audreyr/cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
.. _Cookiecutter: https://github.com/audreyr/cookiecutter

Features
--------

This template has all of the features of the original `audreyr/cookiecutter-pypackage`_, plus the following:

* Dependency tracking using poetry_
* Linting provided by both pylint_ and flake8_ [executed by Tox]
* Formatting provided by yapf_ and isort_ [checked by Tox]
* Autodoc your code from Google docstring style (optional)
* All development tasks (lint, format, test, etc) wrapped up in a python CLI by invoke_

Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)::

    pip install -U cookiecutter

Generate a Python package project::

    cookiecutter https://github.com/briggySmalls/cookiecutter-pypackage.git

Then:

* Create a repo and put it there.
* Add the repo to your Travis-CI_ account.
* Install the dev requirements into a virtualenv. (``poetry install``)
* Run the Travis CLI command `travis encrypt --add deploy.password` to encrypt your PyPI password in Travis config
  and activate automated deployment on PyPI when you push a new tag to master branch.
* Add the repo to your `Read the Docs`_ account + turn on the Read the Docs service hook.
* Release your package by pushing a new tag to master.
* Get your code on! 😎 Add your package dependencies as you go, locking them into your virtual environment with ``poetry add``.
* Activate your project on `pyup.io`_.

.. _`pip docs for requirements files`: https://pip.pypa.io/en/stable/user_guide/#requirements-files
.. _Register: https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives

For more details, see the `cookiecutter-pypackage tutorial`_.

.. _`cookiecutter-pypackage tutorial`: https://briggysmalls.github.io/cookiecutter-pypackage/tutorial.html

.. _invoke: http://www.pyinvoke.org/
.. _isort: https://pypi.org/project/isort/
.. _yapf: https://github.com/google/yapf
.. _flake8: https://pypi.org/project/flake8/
.. _pylint: https://www.pylint.org/
.. _poetry: https://python-poetry.org/
.. _original_pypackage: https://github.com/briggySmalls/cookiecutter-pypackage/
.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _Read the Docs: https://readthedocs.io/
.. _`pyup.io`: https://pyup.io/
.. _bump2version: https://github.com/c4urself/bump2version
.. _Punch: https://github.com/lgiordani/punch
.. _Pipenv: https://pipenv.readthedocs.io/en/latest/
.. _PyPi: https://pypi.python.org/pypi
