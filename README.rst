======================
Cookiecutter PyPackage
======================

.. image:: https://pyup.io/repos/github/inhumantsar/cookiecutter-pypackage/shield.svg
     :target: https://pyup.io/repos/github/inhumantsar/cookiecutter-pypackage/
     :alt: Updates

.. image:: https://travis-ci.org/inhumantsar/cookiecutter-pypackage.svg?branch=master
    :target: https://travis-ci.org/inhumantsar/cookiecutter-pypackage     

Cookiecutter_ template for a Python package. Based on `audreyr/cookiecutter-pypackage`_

* GitHub repo: https://github.com/inhumantsar/cookiecutter-pypackage/
* Documentation: https://cookiecutter-pypackage.readthedocs.io/
* Free software: BSD license

Features
--------

* Test with nox, or pytest.
* Nox_: Nox is configured to test across Python 2.7, 3.6, & 3.7, as well as lint and build docs with Sphinx.
* PyTest_: If you want to dig in manually.
* Sphinx_ docs: Documentation ready for generation with, for example, ReadTheDocs_
* Bumpversion_: Pre-configured version bumping with a single command
* Command line interface using Click_ (optional)


Build Status
-------------

Linux:

.. image:: https://img.shields.io/travis/inhumantsar/cookiecutter-pypackage.svg
    :target: https://travis-ci.org/inhumantsar/cookiecutter-pypackage
    :alt: Linux build status on Travis CI

Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)::

    pip install -U cookiecutter

Generate a Python package project::

    cookiecutter gh:inhumantsar/cookiecutter-pypackage.git

Test with Nox:

    # run everything
    nox
    
    # run tests only
    nox -s tests

    # run everything but tests and linting
    nox -k "not tests and not lint"

    # run tests on py3.6 only
    nox -s "tests(python='3.6')"

Not Exactly What You Want?
--------------------------

Don't worry, you have options:

Similar Cookiecutter Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `audreyr/cookiecutter-pypackage`_: The Original

* `Nekroze/cookiecutter-pypackage`_: A fork of this with a PyTest test runner,
  strict flake8 checking with Travis/Tox, and some docs and `setup.py` differences.

* `tony/cookiecutter-pypackage-pythonic`_: Fork with py2.7+3.3 optimizations.
  Flask/Werkzeug-style test runner, ``_compat`` module and module/doc conventions.
  See ``README.rst`` or the `github comparison view`_ for exhaustive list of
  additions and modifications.

* `ardydedase/cookiecutter-pypackage`_: A fork with separate requirements files rather than a requirements list in the ``setup.py`` file.

* `lgiordani/cookiecutter-pypackage`_: A fork of Cookiecutter that uses Punch_ instead of Bumpversion_ and with separate requirements files.

* Also see the `network`_ and `family tree`_ for this repo. (If you find
  anything that should be listed here, please add it and send a pull request!)
  
Fork This / Create Your Own
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have differences in your preferred setup, I encourage you to fork this
to create your own version. Or create your own; it doesn't strictly have to
be a fork.

* Once you have your own version working, add it to the Similar Cookiecutter
  Templates list above with a brief description.

* It's up to you whether or not to rename your fork/own version. Do whatever
  you think sounds good.

Or Submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~

I also accept pull requests on this, if they're small, atomic, and if they
make my own packaging experience better.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _Nox: https://nox.thea.codes
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.io/
.. _`pyup.io`: https://pyup.io/
.. _Bumpversion: https://github.com/peritus/bumpversion
.. _Punch: https://github.com/lgiordani/punch
.. _PyPi: https://pypi.python.org/pypi
.. _Click: https://click.palletsprojects.com

.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Nekroze/cookiecutter-pypackage`: https://github.com/Nekroze/cookiecutter-pypackage
.. _`tony/cookiecutter-pypackage-pythonic`: https://github.com/tony/cookiecutter-pypackage-pythonic
.. _`ardydedase/cookiecutter-pypackage`: https://github.com/ardydedase/cookiecutter-pypackage
.. _`lgiordani/cookiecutter-pypackage`: https://github.com/lgiordani/cookiecutter-pypackage
.. _github comparison view: https://github.com/tony/cookiecutter-pypackage-pythonic/compare/inhumantsar:master...master
.. _`network`: https://github.com/inhumantsar/cookiecutter-pypackage/network
.. _`family tree`: https://github.com/inhumantsar/cookiecutter-pypackage/network/members
