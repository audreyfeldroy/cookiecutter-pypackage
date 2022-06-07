======================
Cookiecutter PyPackage
======================

Vizzuality Cookiecutter_ template for a simple Python package.

Features
--------

* Packaging and dependency management with Poetry_
* Testing setup with ``pytest``
* Sphinx_ docs: Documentation ready for generation with, for example, `Read the Docs`_
* bump2version_: Pre-configured version bumping with a single command (CHECK)
* pre-commit configured that checks formatting with Black_ and flakeheaven_
* Command line interface using Click (optional)

.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter

Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)::

    pip install -U cookiecutter

Install Poetry_ by downloading and running `install-poetry.py`_::
  
    python install-poetry.py

.. _`install-poetry.py`: https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py

Generate a Python package project::

    cookiecutter https://github.com/vizzTools/cookiecutter-pypackage

Then, install the dev requirements (linter, formatter...)::

    poetry install

Install the pre-commit hook::
    
    poetry run pre-commit install

And you are done!

Not Exactly What You Want?
--------------------------

Don't worry, we can change it.


TODO
----

* Convert all the .rst files to .md ?
* Check that linters are working properly (docstring warnings are broken currently!)
* Check that Sphinx is properly configured and the template looks good
* Add Docker support
* Review default values for author, email and usernames and set them to generic Vizzuality account info

.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _Read the Docs: https://readthedocs.io/
.. _`pyup.io`: https://pyup.io/
.. _bump2version: https://github.com/c4urself/bump2version
.. _Punch: https://github.com/lgiordani/punch
.. _Poetry: https://python-poetry.org/
.. _PyPi: https://pypi.python.org/pypi
.. _Mkdocs: https://pypi.org/project/mkdocs/
.. _Pre-commit: https://pre-commit.com/
.. _Black: https://black.readthedocs.io/en/stable/
.. _Mypy: https://mypy.readthedocs.io/en/stable/
.. _flakeheaven: https://flakeheaven.readthedocs.io/en/latest/
