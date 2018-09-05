.. _devguide:

Developer Guide
===============

.. contents::
    :local:
    :depth: 1

Building the docs
-----------------

First install dependencies for the documentation:

.. code-block:: sh

  $ make bootstrap_dev
  $ make docs

.. _testing:

Running tests
-------------

Run tests using `pytest`_.

First activate the ``{{ cookiecutter.project_slug }}`` Conda environment and install ``pytest``.

.. code-block:: sh

   $ source activate {{ cookiecutter.project_slug }}
   $ conda install pytest flake8  # if not already installed

Run quick tests (skip slow and online):

.. code-block:: sh

    $ pytest -m 'not slow and not online'"

Run all tests:

.. code-block:: sh

    $ pytest

Check pep8:

.. code-block:: sh

    $ flake8

Run tests the lazy way
----------------------

Do the same as above using the ``Makefile``.

.. code-block:: sh

    $ make test
    $ make testall
    $ make pep8

Bump a new version
------------------

Make a new version of {{ cookiecutter.project_name }} in the following steps:

* Make sure everything is commit to GitHub.
* Update ``CHANGES.rst`` with the next version.
* Dry Run: ``bumpversion --dry-run --verbose --new-version 0.8.1 patch``
* Do it: ``bumpversion --new-version 0.8.1 patch``
* ... or: ``bumpversion --new-version 0.9.0 minor``
* Push it: ``git push --tags``

See the bumpversion_ documentation for details.

.. _bumpversion: https://pypi.org/project/bumpversion/
.. _pytest: https://docs.pytest.org/en/latest/
