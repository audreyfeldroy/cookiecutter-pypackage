===========================
MeteoSwiss Python Blueprint
===========================

Cookiecutter_ template for a Python package.

* GitHub repo: https://github.com/donatperler/mch-python-blueprint/
* Free software: BSD license

Features
--------

* Testing setup with ``python setup.py test`` and ``py.test``
* Tox_ testing: Setup to easily test for Python 2.7, 3.4, 3.5, 3.6
* Sphinx_ docs: Documentation ready for generation with, for example, ReadTheDocs_
* Bumpversion_: Pre-configured version bumping with a single command
* Auto-release to PyPI_ when you push a new tag to master (optional)
* Command line interface using Click (optional)

.. _Cookiecutter: https://github.com/audreyr/cookiecutter


Quickstart
----------

At CSCS, you can load the Python module with following command. It will load the Python environment 
and the needed script to start a new project::

    module load python/3.7

Generate a Python package project::

    cookiecutter https://github.com/donatperler/mch-python-blueprint.git

Then:

* Create a repo and put it there 
    * Move to your project folder (``cd you_project``)
    * Create localy a repository (``git init``) 
    * Add and commit the current content (``git add .`` and ``git commit``)
    * Create an empty repository with the same name on `Github`_ 
    * Set the remote repository to Github (``git remote add origin git@github.com:username/new_repo``)
    * Push the content of the local repository to Github (``git push -u origin master``)
* Create a virtual Python environment for your project (see `pipenv`_, `virtualenv`_ or `virtualenvwrapper`_)
* Install the dev requirements into a virtualenv. (``pipenv install -r requirements_dev.txt 
  --dev`` or ``pip install -r requirements_dev.txt``)
* Release your package by pushing a new tag to master.
* Add a `requirements.txt` file if you are working with virtualenv or virtualenvwrapper or use 
  ``pipenv look`` to create a `Pipfile.lock` that specifies the packages you will need for
  your project and their versions. For more info see the `pip docs for requirements files`_.
* Add the `requirements.txt` or the `Pipfile.lock` file to your repository

.. _`pipenv`: https://realpython.com/pipenv-guide/
.. _`virtualenv`: https://virtualenv.pypa.io/en/stable/userguide/
.. _`virtualenvwrapper`: https://virtualenvwrapper.readthedocs.io/en/latest/index.html
.. _`pip docs for requirements files`: https://pip.pypa.io/en/stable/user_guide/#requirements-files
.. _`Github`: https://github.com/new


