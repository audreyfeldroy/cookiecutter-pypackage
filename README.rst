==========================
Cookiecutter for Birdhouse
==========================

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
   :target: http://cookiecutter-birdhouse.readthedocs.org/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/bird-house/cookiecutter-birdhouse.svg?branch=master
   :target: https://travis-ci.org/bird-house/cookiecutter-birdhouse
   :alt: Travis Build

.. image:: https://img.shields.io/github/license/bird-house/cookiecutter-birdhouse.svg
    :target: https://github.com/bird-house/cookiecutter-birdhouse/blob/master/LICENSE
    :alt: GitHub license

.. image:: https://badges.gitter.im/bird-house/birdhouse.svg
    :target: https://gitter.im/bird-house/birdhouse?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
    :alt: Join the chat at https://gitter.im/bird-house/birdhouse

*A Cookiecutter template for a Birdhouse bird package*

Cookiecutter_ is a command-line utility to create projects from templates. This `cookiecutter-birdhouse`
template creates a barebone PyWPS server adhering to Birdhouse conventions. It comes complete with a
framework for installation, configuration, deployment, documentation and tests. It even includes a
:file:`Dockerfile` for containerization! Create your project then get started writing new WPS
processes in minutes.

* GitHub repo: https://github.com/bird-house/cookiecutter-birdhouse/
* Documentation: http://cookiecutter-birdhouse.readthedocs.io/en/latest/
* Free software: BSD license


.. warning::

   This is the cookiecutter template for PyWPS *without* the Buildout deployment.
   The template for the Buildout deployment is on branch `0.2.x`_.

Features
--------

* Ready-made PyWPS server (a bird)
* Pre-configured :file:`.travis.yml` for Travis-CI_ automated deployment and testing
* Pre-configured :file:`.codacy.yml` for automated Codacy_ code review
* A :file:`Dockerfile` and :file:`docker-compose.yml` for containerization
* Preconfigured Sphinx_ documentation that can be hosted on ReadTheDocs_
* A :file:`Makefile` to install the code, start, stop and poll the server and more

Installation
------------

Prior to installing cookiecutter-birdhouse, the cookiecutter package must be installed in your environment.
This is achieved via the following command:

.. code-block:: console

    $ conda install -c conda-forge cookiecutter

With cookiecutter installed, the cookiecutter-birdhouse template can be installed with:

.. code-block:: console

    $ cookiecutter https://github.com/bird-house/cookiecutter-birdhouse.git

Once cookiecutter clones the template, you will be asked a series of questions related to your project:

.. code-block:: console

    $ full_name [Full Name]: Enter your full name.

    $ email [Email Address]: Enter your email address.

    $ github_username [bird-house]: Accept the default or enter your github username.

    $ project_name [Babybird]: The name of your new bird.

    $ project_slug [babybird]: The name of your bird used as Python package.

    $ project_short_description [Short description]: Enter a short description about your project.

    $ version [0.1.0]: Enter the version number for your application.

    $ http_port [5000]: The HTTP port on which your service will be accessible.

    $ https_port [25000]: The HTTPS port on which your service will be accessible.

    $ output_port [8090]: The HTTP port on which your service outputs will be accessible.

Usage
-----

After answering the questions asked during installation, a *bird* Python package will be
created in your current working directory. This package will contain a configurable PyWPS
service with some initial test processes.

Then:

* Create a repo and put it there.
* Add the repo to your Travis-CI_ account.
* Add the repo to your ReadTheDocs_ account + turn on the ReadTheDocs service hook.

For more details, see the `cookiecutter-pypackage tutorial`_.

See the `babybird <http://babybird.rtfd.io/>`_ example of a generated bird.

Development
-----------

If you want to extend the cookiecutter template then prepare your development
environment as follows:

.. code-block:: console

  # clone repo
  $ git clone git@github.com:bird-house/cookiecutter-birdhouse.git

  # change into repo
  $ cd cookiecutter-birdhouse

  # create conda environment
  $ conda env create -f environment.yml

  # activate conda environment
  $ source activate cookiecutter-birdhouse

  # run tests
  $ make test

  # bake a new bird with default settings
  $ make bake

  # the new "baked" bird is created in the cookies folder
  $ ls -l cookies/
  babybird

  # well ... you know what to do with a bird :)

  # finally you may clean it all up
  $ make clean

Bump a new version
------------------

Make a new version of this Cookiecutter in the following steps:

  * Make sure everything is commit to GitHub.
  * Update ``CHANGES.rst`` with the next version.
  * Dry Run: ``bumpversion --dry-run --verbose --new-version 0.3.1 patch``
  * Do it: ``bumpversion --new-version 0.3.1 patch``
  * ... or: ``bumpversion --new-version 0.4.0 minor``
  * Push it: ``git push --tags``

See the bumpversion_ documentation for details.


.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage tutorial`: https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html
.. _Travis-CI: http://travis-ci.org/
.. _Codacy: http://codacy.com
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.io/
.. _bumpversion: https://pypi.org/project/bumpversion/
.. _0.2.x: https://github.com/bird-house/cookiecutter-birdhouse/tree/0.2.x
