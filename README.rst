======================
Cookiecutter PyPackage
======================


Cookiecutter_ template for a Python package.

* GitHub repo: https://github.com/audreyfeldroy/cookiecutter-pypackage/
* Documentation: https://cookiecutter-pypackage.readthedocs.io/
* Free software: BSD license

.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter

Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)::

    pip install -U cookiecutter

Generate a Python package project::

    cookiecutter https://github.com/ihumphrey/cookiecutter-pypackage.git

Then:

* Create a new repo on GitHub, `git init` the created python package project, and push it up to the new repo.
* Install versioneer: `pip install -U versioneer`.
* Setup versioneer in the python package project: `versioneer install`.
* Commit and push the changes from versioneer.
* Install the package into a venv / conda env: `pip install -e .[docs, tests]`.
* Login to Codecov and setup repo (copy API token into Settings -> Secrets -> Actions -> New Repository Secret)
* CODECOV_TOKEN
* (Optional) set up CodeClimate Quality (login with GitHub)
* Add the repo to your `Read the Docs`_ account + turn on the Read the Docs service hook.
* When you want to release:
* Register_ your project with PyPI.
* Update ``requirements.txt`` file that specifies the packages you will need for
  your project and their versions. For more info see the `pip docs for requirements files`_.
* Release your package by pushing a new tag to master; this will generate a GitHub release and PyPI release.
* DOI

.. _`pip docs for requirements files`: https://pip.pypa.io/en/stable/user_guide/#requirements-files
.. _Register: https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives

For more details, see the `cookiecutter-pypackage tutorial`_.

.. _`cookiecutter-pypackage tutorial`: https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html


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

