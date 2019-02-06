.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/MeteoSwiss-APN/{{ cookiecutter.project_slug }}/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

{{ cookiecutter.project_name }} could always use more documentation, whether as part of the
official {{ cookiecutter.project_name }} docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/MeteoSwiss-APN/{{ cookiecutter.project_slug }}/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `{{ cookiecutter.project_slug }}` for local development.

1. Fork the `{{ cookiecutter.project_slug }}` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/{{ cookiecutter.project_slug }}.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv {{ cookiecutter.project_slug }}
    $ cd {{ cookiecutter.project_slug }}/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, format them with yapf, check that your
   changes pass the static code analyses with flake8 and the tests with py.test, including testing other Python versions
   with tox::

    $ yapf -ir {{ cookiecutter.project_slug }}
    $ flake8 {{ cookiecutter.project_slug }} tests
    $ py.test
    $ tox  # optional, currently only flake8 and Python 3.7 configured and thus not necessary

   To get yapf, flake8 and tox, just pip install them into your virtualenv (``pipenv install --dev``).

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.6 and 3.7, and for PyPy. Make sure
   that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

    $ py.test tests.test_{{ cookiecutter.project_slug }}

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bumpversion patch # possible: major / minor / patch
$ git push
$ git push --tags

Jenkins will then deploy to PyPI if tests pass.

Project Structure
-----------------

.. list-table:: Structure
   :widths: 25 75
   :header-rows: 1
   
   * - File / Directory
     - Description
   * - docs
     - Directory containing the documentation
   * - tests
     - Directory containing the tests. The directory structure in this folder is the same as in the source folder ({{ cookiecutter.project_slug }}). For each file in the source folder, there is a file with the same name, but, with the prefix ``text_``.
   * - {{ cookiecutter.project_slug }}
     - Source folder
   * - AUTHORS.rst
     - Contains information about the lead developer and contributors
   * - CONTRIBUTION.rst
     - Contains all the information you need when you contribute to this project
   * - HISTORY.rst
     - Lists the releases and their new features
   * - LICENSE
     - License of this project
   * - MANIFEST.in
     - Specifies the files and directories which will be added to the Pip package
   * - Makefile
     - Build file for cleaning, creating and releasing packages, for testing and linting code, and for creating the documentation
   * - Pipefile
     - Contains all pip packages used in the virtual environment for development (section ``dev-packages``) or needed by the library/application (section ``packages``). The packages listed in the section ``packages`` must be the same as in the file ``requirements.txt`` and the variable ``requirements`` in the file ``setup.py``. The file is used and managed by ``pipenv``. 
   * - README.rst
     - Short documentation about this package. It lists features and contains a quick start.
   * - requirements.txt
     - Containts all pip packages needed by the library/application. The packages listed in this file must be the same as in the section ``packages`` of the file ``Pipefile`` and in the variable ``requirements`` in the file ``setup.py``
   * - requirements_dev.txt
     - Contains all pip packages used in the virtual environment for development. The packages listed must be the same as the ones in the section ``dev-packages`` in the file ``Pipefile``.
   * - setup.cfg
     - Configuration file for different build tools such as bumpversion bdist, flake8, pytest, and yapf
   * - setup.py
     - Script used to build the package. It specifies the dependencies of the library/application and the Python verions which are compatible with this library/application. These two things are usually the only things to adapt in this file. The Python version listed here should be the same as in the file ``tox.ini``.
   * - tox.ini
     - A configuration file for tox carring out the test for different Python verions. The listed versions should be the same as in the file ``setup.py``.
