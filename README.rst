======================
Cookiecutter PyPackage
======================

Cookiecutter_ template for a Python PyPI ready package library.

* GitHub repo: https://github.com/wooyek/cookiecutter-pylib/
* Documentation: https://cookiecutter-pylib.readthedocs.io/
* Free software: BSD license

.. image:: https://img.shields.io/travis/wooyek/cookiecutter-pylib.svg
:target: https://travis-ci.org/wooyek/cookiecutter-pylib
    :alt: Linux build status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/wooyek/cookiecutter-pylib?branch=master&svg=true
:target: https://ci.appveyor.com/project/wooyek/cookiecutter-pylib/branch/master
    :alt: Windows build status on Appveyor


Features
--------

* Testing setup with ``unittest`` and ``python setup.py test`` or ``py.test``
* Travis-CI_: Ready for Travis Continuous Integration testing
* Tox_ testing: Setup to easily test for Python 2.6, 2.7, 3.3, 3.4, 3.5
* Sphinx_ docs: Documentation ready for generation with, for example, ReadTheDocs_
* Bumpversion_: Pre-configured version bumping with a single command
* Auto-release to PyPI_ when you push a new tag to master (optional)
* Split file requirements management with inheritance
* Command line interface using Click (optional)
* Initialization of GIT repo, github origin remote and git-flow
* Python virtual environment bootstrapping

.. _Cookiecutter: https://github.com/audreyr/cookiecutter


Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet::

    pip install -U cookiecutter

Generate a Python package project::

    cookiecutter https://github.com/wooyek/cookiecutter-pylib.git

Then:

* Add the repo to your Travis-CI_ account.
* Install the dev requirements into a virtualenv. (``pip install -r requirements.txt``)
* Run the script `travis_pypi_setup.py` to encrypt your PyPI password in Travis config
  and activate automated deployment on PyPI when you push a new tag to master branch.
* Add the repo to your ReadTheDocs_ account + turn on the ReadTheDocs service hook.
* Release your package by pushing a new tag to master.
* Update `requirements/base.txt` file that specifies the packages you will need for
  your project and their versions. For more info see the `pip docs for requirements files`_.

.. _`pip docs for requirements files`: https://pip.pypa.io/en/stable/user_guide/#requirements-files

For more details, see the `cookiecutter-pylib tutorial`_.

.. _`cookiecutter-pylib tutorial`: https://cookiecutter-pylib.readthedocs.io/en/latest/tutorial.html

Not Exactly What You Want?
--------------------------

Don't worry, you have options:

Similar Cookiecutter Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `available cookiecutters`_: View curated list of cookiecutters

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


.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.io/
.. _`pyup.io`: https://pyup.io/
.. _Bumpversion: https://github.com/peritus/bumpversion
.. _PyPi: https://pypi.python.org/pypi

.. _`available cookiecutters`: http://cookiecutter.readthedocs.io/en/latest/readme.html#available-cookiecutters
.. _`tony/cookiecutter-pylib-pythonic`: https://github.com/tony/cookiecutter-pylib-pythonic
.. _`ardydedase/cookiecutter-pylib`: https://github.com/ardydedase/cookiecutter-pylib
.. _github comparison view: https://github.com/tony/cookiecutter-pylib-pythonic/compare/audreyr:master...master
.. _`network`: https://github.com/wooyek/cookiecutter-pylib/network
.. _`family tree`: https://github.com/wooyek/cookiecutter-pylib/network/members
