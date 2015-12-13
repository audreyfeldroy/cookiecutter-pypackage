Tutorial
========

.. note:: Did you find any of these instructions confusing? `Edit this file`_
          and submit a pull request with your improvements!

.. _`Edit this file`: https://github.com/audreyr/cookiecutter-pypackage/blob/master/docs/tutorial.rst

Step 1: Install Cookiecutter
----------------------------

First, create a virtualenv for your new package. Install the following:

```
pip install cookiecutter
```

Step 2: Generate Your Package
-----------------------------

Generate a Python package project::

    cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git


Step 3: Create a GitHub Repo
----------------------------

Create a repo and put your package there.

Step 4: Set Up Travis CI
------------------------

Log into `Travis CI`_.

Add the repo to your Travis CI account.

Run the script `travis_pypi_setup.py` to encrypt your PyPI password in Travis config
  and activate automated deployment on PyPI when you push a new tag to master branch.
  
.. _`Travis CI`: https://travis-ci.org/

Step 5: Set Up ReadTheDocs
--------------------------

Add the repo to your ReadTheDocs account.

Turn on the ReadTheDocs service hook.

Step 6: Release on PyPI
------------------------

* Release your package the standard Python way. Here's a release checklist: 
  https://gist.github.com/audreyr/5990987
  