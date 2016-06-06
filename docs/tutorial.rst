Tutorial
========

.. note:: Did you find any of these instructions confusing? `Edit this file`_
          and submit a pull request with your improvements!

.. _`Edit this file`: https://github.com/audreyr/cookiecutter-pypackage/blob/master/docs/tutorial.rst

Step 1: Install Cookiecutter
----------------------------

First, you need to create and activate a virtualenv for the package project. Use your favorite method, or create a virtualenv for your new package like this:

.. code-block:: bash

    virtualenv ~/.virtualenvs/mypackage


Here, `mypackage` is the name of the package that you'll create.

Activate your environment:

.. code-block:: bash

    source bin/activate

On Windows, activate it like this. You may find that using a Command Prompt window works better than gitbash.

.. code-block:: bash

    > \path\to\env\Scripts\activate


Install cookiecutter

.. code-block:: bash

    pip install cookiecutter


Step 2: Generate Your Package
-----------------------------

Now it's time to generate your Python package.

Use cookiecutter, pointing it at the cookiecutter-pypackage repo:

.. code-block:: bash

    cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git

You'll be asked to enter a bunch of values to set the package up.
If you don't know what to enter, stick with the defaults.

Step 3: Create a GitHub Repo
----------------------------

Go to your GitHub account and create a new repo named ``mypackage``.

**If your ``virtualenv`` folder is within your project folder, be sure to add the ``virtualenv`` folder name to the ``.gitignore`` file.**

You will find one folder named after the `[project_slug]` from your answers to running cookiecutter. Move into this folder, and then setup git to use your GitHub repo and upload the code:

.. code-block:: bash

    cd mypackage
    git init .
    git add .
    git commit -m "Initial skeleton."
    git remote add origin git@github.com:myusername/mypackage.git
    git push -u origin master

Where ``myusername`` and ``mypackage`` are adjusted for your username and package name.

You'll need a ssh key to push the repo. You can `Generate`_ a key or `Add`_ an existing one.

.. _`Generate`: https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/
.. _`Add`: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/


Step 4: Install Dev Requirements
--------------------------------

You should now be in the folder containing the ``requirements_dev.txt`` file.

Your virtualenv should still be activated. If it isn't, activate it now. Install the new project's local development requirements:

.. code-block:: bash

    pip install -r requirements_dev.txt

If you have issues building the wheel for cryptography. Make sure that the required dependencies are installed. Follow the `Cryptography Instruction`_ for your OS

.. _ `Cryptography Instruction `:https://cryptography.io/en/latest/installation/


Step 5: Set Up Travis CI
------------------------

`Travis CI org`_ is a continuous integration tool used to prevent integration problems. Every commit to the master branch will trigger automated builds to create the necessary files to run the application.

Login using your Github credentials.

Add the public repo to your Travis CI account.

[#] For private projects got to `Travis CI com`_

Go to your terminal and run the script ``travis_pypi_setup.py``. It will:

* Encrypt your PyPI password in your Travis config.
* Activate automated deployment on PyPI when you push a new tag to master branch.

See :ref:`travis-pypi-setup`.

.. _`Travis CI org`: https://travis-ci.org/
.. _`Travis CI com`: https://travis-ci.com/

Step 6: Set Up ReadTheDocs
--------------------------

`ReadTheDocs`_ hosts documentation for the open source community. Think of it as Continuous Documentation.

Log into your account at `ReadTheDocs`_ .

Import the repository

In your GitHub repo settings > Webhooks & services, turn on the ReadTheDocs service hook.

.. _ `ReadTheDocs`: https://readthedocs.io/

Step 7: Release on PyPI
------------------------

The Python Package Index or `PyPI`_ is the official third-party software repository for the Python programming language. Python developers intend it to be a comprehensive catalog of all open source Python packages.[1]

Release your package the standard Python way.

`PyPI Help`_ submitting a package.

Here's a release checklist: https://gist.github.com/audreyr/5990987

.. _ `PyPI`: https://pypi.python.org/pypi
.. _ `PyPI Help`: http://peterdowns.com/posts/first-time-with-pypi.html
