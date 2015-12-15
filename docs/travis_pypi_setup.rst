.. _travis-pypi-setup:


Travis/PyPI Setup
=================

Optionally, your package can automatically be released on PyPI whenever you
push a new tag to the master branch.

How It Works
------------

Your project comes with a script called `travis_pypi_setup.py`.

This script does the following:

* Encrypt your PyPI password and save it in your Travis config
* Activate automated deployment on PyPI when you push a new tag to master.

The encryption is done using RSA encryption, you can `read more
about Travis encryption here <https://docs.travis-ci.com/user/encryption-keys/>`_.
In short, the encrypted password can only be decrypted by Travis,
using the private key it associates with your repo.


Using the Travis command-line tool instead
------------------------------------------

If you have the `travis` command - line tool installed, instead of using
the `travis_pypi_setup.py` script you can do::

    travis encrypt --add deploy.password

Which does essentially the same thing.


Your Release Process
--------------------

If you are using this feature, this is how you would do a patch release:

.. code-block:: bash

    bumpversion patch
    git push --tags

This will result in:

* mypackage 0.1.1 showing up in your GitHub tags/releases page
* mypackage 0.1.1 getting released on PyPI

You can also replace patch with `minor` or `major`.


More Details
------------

You can read more about using Travis for PyPI deployment at:
https://docs.travis-ci.com/user/deployment/pypi/
