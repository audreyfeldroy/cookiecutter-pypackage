Tutorial
========

.. note:: Did you find any of these instructions confusing? `Edit this file`_
          and submit a pull request with your improvements!

.. _`Edit this file`: https://github.com/audreyfeldroy/cookiecutter-pypackage/blob/master/docs/tutorial.rst

To start with, you will need a `GitHub account`_ and an account on `PyPI`_. Create these before you get started on this tutorial. If you are new to Git and GitHub, you should probably spend a few minutes on some of the tutorials at the top of the page at `GitHub Help`_.

.. _`GitHub account`: https://github.com/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`GitHub Help`: https://help.github.com/


Step 1: Install Cookiecutter
----------------------------

First, you need to create and activate a virtualenv for the package project. Use your favorite method, or create a virtualenv for your new package like this:

.. code-block:: bash

    virtualenv ~/.virtualenvs/mypackage

Here, ``mypackage`` is the name of the package that you'll create.

Activate your environment:

.. code-block:: bash

    source bin/activate

On Windows, activate it like this. You may find that using a Command Prompt window works better than gitbash.

.. code-block:: powershell

    > \path\to\env\Scripts\activate

.. note::

    If you create your virtual environment folder in a different location within your project folder, be sure to add that path to your .gitignore file.

Install cookiecutter:

.. code-block:: bash

    pip install cookiecutter


Step 2: Generate Your Package
-----------------------------

Now it's time to generate your Python package.

Use cookiecutter, pointing it at the cookiecutter-pypackage repo:

.. code-block:: bash

    cookiecutter https://github.com/audreyfeldroy/cookiecutter-pypackage.git

You'll be asked to enter various values to set the package up.
If you don't know what to enter, press Enter to stick with the defaults.


Step 3: Create a GitHub Repo
----------------------------

Go to your GitHub account and create a new repo named ``mypackage``, where ``mypackage`` matches the ``[project_slug]`` from your answers to running cookiecutter. This is so that pyup.io can find it when we get to Step 7.

You will find one folder named after the ``[project_slug]``. Move into this folder, and then setup git to use your GitHub repo and upload the code:

.. code-block:: bash

    cd mypackage
    git init .
    git add .
    git commit -m "Initial skeleton."
    git remote add origin git@github.com:myusername/mypackage.git
    git push -u origin main

Where ``myusername`` and ``mypackage`` are adjusted for your username and package name.

You'll need a ssh key to push the repo. You can `Generate`_ a key or `Add`_ an existing one.

.. _`Generate`: https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/
.. _`Add`: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/


Step 4: Install Dev Requirements
--------------------------------

You should still be in the folder containing the ``requirements_dev.txt`` file.

Your virtualenv should still be activated. If it isn't, activate it now. Install the new project's local development requirements:

.. code-block:: bash

    pip install -r requirements_dev.txt


Step 5: Set Up GitHub Actions CI
--------------------------------

`GitHub Actions`_ is a continuous integration tool used to prevent integration problems. Every pull request or commit to the master branch will trigger a workflow that runs automated tests.

Files describing the workflow are stored in the ``.github/workflows`` directory. See the documentation link at the top of the workflow file for more information.

.. _`GitHub Actions`: https://docs.github.com/en/actions


Step 6: Set Up Read the Docs
--------------------------

`Read the Docs`_ hosts documentation for the open source community. Think of it as Continuous Documentation.

Log into your account at `Read the Docs`_ . If you don't have one, create one and log into it.

If you are not at your dashboard, choose the pull-down next to your username in the upper right, and select "My Projects". Choose the button to Import the repository and follow the directions.

Now your documentation will get rebuilt when you make documentation changes to your package.

.. _`Read the Docs`: https://readthedocs.org/



Step 7: Release on PyPI
-----------------------

The Python Package Index or `PyPI`_ is the official third-party software repository for the Python programming language. Python developers intend it to be a comprehensive catalog of all open source Python packages.

When you are ready, release your package the standard Python way.

See `PyPI Help`_ for more information about submitting a package.

Here's a release checklist you can use: https://github.com/audreyfeldroy/cookiecutter-pypackage/blob/master/docs/pypi_release_checklist.rst

.. _`PyPI`: https://pypi.python.org/pypi
.. _`PyPI Help`: https://pypi.org/help/#publishing


Having problems?
----------------

Visit our :ref:`troubleshooting` page for help. If that doesn't help, go to our `Issues`_ page and create a new Issue. Be sure to give as much information as possible.

.. _`Issues`: https://github.com/audreyfeldroy/cookiecutter-pypackage/issues
