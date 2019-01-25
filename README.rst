======================
Cookiecutter PyPackage
======================

.. image:: https://pyup.io/repos/github/briggySmalls/cookiecutter-pypackage/shield.svg
     :target: https://pyup.io/repos/github/briggySmalls/cookiecutter-pypackage/
     :alt: Updates

.. image:: https://travis-ci.org/audreyr/cookiecutter-pypackage.svg?branch=master
    :target: https://travis-ci.org/audreyr/cookiecutter-pypackage

Cookiecutter_ template for a Python package, forked from original_pypackage_<audreyr/cookiecutter-pypackage>.

* GitHub repo: https://github.com/briggySmalls/cookiecutter-pypackage/
* Documentation: https://cookiecutter-pypackage.readthedocs.io/
* Free software: BSD license

.. _Cookiecutter: https://github.com/audreyr/cookiecutter

Features
--------

This template has all of the features of the original original_pypackage_<audreyr/cookiecutter-pypackage>, plus the following:

* Dependency tracking using pipenv_
* Linting provided by both pylint_ and flake8_ [executed by Tox]
* Formatting provided by yapf_ and isort_ [checked by Tox]
* Autodoc your code from Google docstring style (optional)
* All development tasks (lint, format, test, etc) wrapped up in a python CLI by invoke_

Build Status
-------------

Linux:

.. image:: https://img.shields.io/travis/briggySmalls/cookiecutter-pypackage.svg
    :target: https://travis-ci.org/briggySmalls/cookiecutter-pypackage
    :alt: Linux build status on Travis CI

Windows:

.. image:: https://ci.appveyor.com/api/projects/status/github/briggySmalls/cookiecutter-pypackage?branch=master&svg=true
    :target: https://ci.appveyor.com/project/briggySmalls/cookiecutter-pypackage/branch/master
    :alt: Windows build status on Appveyor

Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)::

    pip install -U cookiecutter

Generate a Python package project::

    cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git

Then:

* Create a repo and put it there.
* Add the repo to your Travis-CI_ account.
* Install the dev requirements into a virtualenv. (``pip install -r requirements_dev.txt``)
* Register_ your project with PyPI.
* Run the Travis CLI command `travis encrypt --add deploy.password` to encrypt your PyPI password in Travis config
  and activate automated deployment on PyPI when you push a new tag to master branch.
* Add the repo to your ReadTheDocs_ account + turn on the ReadTheDocs service hook.
* Release your package by pushing a new tag to master.
* Add a `requirements.txt` file that specifies the packages you will need for
  your project and their versions. For more info see the `pip docs for requirements files`_.
* Activate your project on `pyup.io`_.

.. _`pip docs for requirements files`: https://pip.pypa.io/en/stable/user_guide/#requirements-files
.. _Register: https://packaging.python.org/distributing/#register-your-project

For more details, see the `cookiecutter-pypackage tutorial`_.

.. _`cookiecutter-pypackage tutorial`: https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html

.. _invoke: http://www.pyinvoke.org/
.. _isort: https://pypi.org/project/isort/
.. _yapf: https://github.com/google/yapf
.. _flake8: https://pypi.org/project/flake8/
.. _pylint: https://www.pylint.org/
.. _pipenv: https://pipenv.readthedocs.io/en/latest/
.. _original_pypackage: https://github.com/briggySmalls/cookiecutter-pypackage/
.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.io/
.. _`pyup.io`: https://pyup.io/
.. _Bumpversion: https://github.com/peritus/bumpversion
.. _Punch: https://github.com/lgiordani/punch
.. _PyPi: https://pypi.python.org/pypi
