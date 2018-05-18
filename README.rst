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

.. todo::

   * Review all this README.
   * Add Cookiecutter logo with a Bird.

A Cookiecutter_ template for a Birdhouse bird package (PyWPS server).

* GitHub repo: https://github.com/bird-house/cookiecutter-birdhouse/
* Documentation: http://cookiecutter-birdhouse.readthedocs.io/en/latest/
* Free software: BSD license

Features
--------

* Ready-made PyWPS service (a bird).
* Pre-configured ``.travis.yml`` for Travis-CI_
* Sphinx_ docs: Documentation ready for generation with, for example, ReadTheDocs_


Installation
------------

Prior to installing cookiecutter-birdhouse, the cookiecutter package must be installed in your environment.
This is achieved via the following command::

    $ conda install -c conda-forge cookiecutter

With cookiecutter installed, the cookiecutter-birdhouse template can be installed with::

    $ cookiecutter https://github.com/bird-house/cookiecutter-birdhouse.git

Once cookiecutter clones the template, you will be asked a series of questions related to your project::

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

Development
-----------

If you want to extend the cookiecutter template then prepare your development
environment as follows::

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

Make a new version of this Cookiecutter in the following steps::

  * Make sure everything is commit to GitHub.
  * Update `CHANGES.rst` with the next version.
  * Dry Run: `bumpversion --dry-run --verbose --new-version 0.2.1 patch`
  * Do it: `bumpversion --new-version 0.2.1 patch`

See the bumpversion_ documentation for details.


.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage tutorial`: https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html
.. _Travis-CI: http://travis-ci.org/
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.io/
.. _bumpversion: https://pypi.org/project/bumpversion/
