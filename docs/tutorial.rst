Tutorial
========

.. note:: Did you find any of these instructions confusing? `Edit this file`_
          and submit a pull request with your improvements!

.. _`Edit this file`: https://github.com/audreyr/cookiecutter-pypackage/blob/master/docs/tutorial.rst

Step 1: Install Cookiecutter
----------------------------

First, create a virtualenv for your new package and install cookiecutter:

.. code-block:: bash

    virtualenv ~/.virtualenvs/mypackage
    pip install cookiecutter

Here, `mypackage` is the name of the package that you'll create.

Step 2: Generate Your Package
-----------------------------

Now it's time to generate your Python package.

Use cookiecutter, pointing it at the cookiecutter-pypackage repo:

.. code-block:: bash

    cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git

You'll be asked to enter a bunch of values. If you don't know what to enter, 
stick with the defaults.

Step 3: Create a GitHub Repo
----------------------------

Create a repo and put your package there. This can be accomplished with:

.. code-block:: bash

    git init .
    git add .
    git commit -m "Initial skeleton."
    git remote add origin git@github.com:myname/mypackage.git
    git push -u origin master
    
where `myname` and `mypackage` are the adjusted for the specific project.

Step 4: Install Dev Requirements
--------------------------------

Install the new project's local development requirements into a virtualenv:

.. code-block:: bash

    pip install -r requirements_dev.txt

Step 5: Set Up Travis CI
------------------------

Log into `Travis CI`_.

Add the repo to your Travis CI account.

Run the script `travis_pypi_setup.py`. It will:

* Encrypt your PyPI password in your Travis config.
* Activate automated deployment on PyPI when you push a new tag to master branch.

See :ref:`travis-pypi-setup`.
  
.. _`Travis CI`: https://travis-ci.org/

Step 6: Set Up ReadTheDocs
--------------------------

Add the repo to your ReadTheDocs account.

In your GitHub repo settings, turn on the ReadTheDocs service hook.

Step 7: Release on PyPI
------------------------

Release your package the standard Python way. 

Here's a release checklist: 
  https://gist.github.com/audreyr/5990987
