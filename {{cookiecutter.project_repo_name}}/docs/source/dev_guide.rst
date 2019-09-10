.. _devguide:

Developer Guide
===============

.. contents::
    :local:
    :depth: 1

.. WARNING:: To create new processes look at examples in Emu_.

Building the docs
-----------------

First install dependencies for the documentation:

.. code-block:: console

  $ make develop

Run the Sphinx docs generator:

.. code-block:: console

  $ make docs

.. _testing:

Running tests
-------------

Run tests using pytest_.

First activate the ``{{ cookiecutter.project_slug }}`` Conda environment and install ``pytest``.

.. code-block:: console

   $ source activate {{ cookiecutter.project_slug }}
   $ pip install -r requirements_dev.txt  # if not already installed
   OR
   $ make develop

Run quick tests (skip slow and online):

.. code-block:: console

    $ pytest -m 'not slow and not online'"

Run all tests:

.. code-block:: console

    $ pytest

Check pep8:

.. code-block:: console

    $ flake8

Run tests the lazy way
----------------------

Do the same as above using the ``Makefile``.

.. code-block:: console

    $ make test
    $ make test-all
    $ make lint

Prepare a release
-----------------

Update the Conda specification file to build identical environments_ on a specific OS.

.. note:: You should run this on your target OS, in our case Linux.

.. code-block:: console

  $ conda env create -f environment.yml
  $ source activate {{ cookiecutter.project_slug }}
  $ make clean
  $ make install
  $ conda list -n {{ cookiecutter.project_slug }} --explicit > spec-file.txt

.. _environments: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#building-identical-conda-environments


Bump a new version
------------------

Make a new version of {{ cookiecutter.project_name }} in the following steps:

* Make sure everything is commit to GitHub.
* Update ``CHANGES.rst`` with the next version.
* Dry Run: ``bumpversion --dry-run --verbose --new-version 0.8.1 patch``
* Do it: ``bumpversion --new-version 0.8.1 patch``
* ... or: ``bumpversion --new-version 0.9.0 minor``
* Push it: ``git push``
* Push tag: ``git push --tags``

See the bumpversion_ documentation for details.

.. _bumpversion: https://pypi.org/project/bumpversion/
.. _pytest: https://docs.pytest.org/en/latest/
.. _Emu: https://github.com/bird-house/emu
