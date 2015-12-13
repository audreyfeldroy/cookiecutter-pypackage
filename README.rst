======================
cookiecutter-pypackage
======================

.. image:: https://img.shields.io/travis/audreyr/cookiecutter-pypackage.svg
   :target: https://travis-ci.org/audreyr/cookiecutter-pypackage

Cookiecutter_ template for a Python package.

* GitHub repo: https://github.com/audreyr/cookiecutter-pypackage/
* Free software: BSD license

Features
--------

* Vanilla testing setup with `unittest` and `python setup.py test`
* Travis-CI_: Ready for Travis Continuous Integration testing
* Tox_ testing: Setup to easily test for Python 2.6, 2.7, 3.3, 3.4, 3.5
* Sphinx_ docs: Documentation ready for generation with, for example, ReadTheDocs_
* Bumpversion: Pre-configured version bumping with a single command
* Auto-release to PyPI when you push a new tag to master (optional)

.. _Cookiecutter: https://github.com/audreyr/cookiecutter

Quickstart
----------

Generate a Python package project::

    cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git

Then:

* Create a repo and put it there.
* Add the repo to your Travis CI account.
* Run the script `travis_pypi_setup.py` to encrypt your PyPI password in Travis config
  and activate automated deployment on PyPI when you push a new tag to master branch.
* Add the repo to your ReadTheDocs account + turn on the ReadTheDocs service hook.
* Release your package the standard Python way. Here's a release checklist: 
  https://gist.github.com/audreyr/5990987
* (Optional) If you feel like pinning the requirements for your package, you can
  add a `requirements.txt` that specifies packages and version numbers.

For more details, see the `cookiecutter-pypackage tutorial`_.

.. _`cookiecutter-pypackage tutorial`: http://cookiecutter-pypackage.readthedocs.org/en/latest/tutorial.html

Not Exactly What You Want?
--------------------------

Don't worry, you have options:

Similar Cookiecutter Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `Nekroze/cookiecutter-pypackage`_: A fork of this with a PyTest test runner,
  strict flake8 checking with Travis/Tox, and some docs and `setup.py` differences.
  
* `tony/cookiecutter-pypackage-pythonic`_: Fork with py2.7+3.3 optimizations. 
  Flask/Werkzeug-style test runner, ``_compat`` module and module/doc conventions.
  See ``README.rst`` or the `github comparison view`_ for exhaustive list of 
  additions and modifications.
  
* `ardydedase/cookiecutter-pypackage`_: A fork with separate requirements files rather than a requirements list in the ``setup.py`` file.

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
.. _ReadTheDocs: https://readthedocs.org/
.. _`Nekroze/cookiecutter-pypackage`: https://github.com/Nekroze/cookiecutter-pypackage
.. _`tony/cookiecutter-pypackage-pythonic`: https://github.com/tony/cookiecutter-pypackage-pythonic
.. _`ardydedase/cookiecutter-pypackage`: https://github.com/ardydedase/cookiecutter-pypackage
.. _github comparison view: https://github.com/tony/cookiecutter-pypackage-pythonic/compare/audreyr:master...master
.. _`network`: https://github.com/audreyr/cookiecutter-pypackage/network
.. _`family tree`: https://github.com/audreyr/cookiecutter-pypackage/network/members
