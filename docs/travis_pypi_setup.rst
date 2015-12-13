Travis/PyPI Setup
=================

Optionally, your package can automatically be released on PyPI whenever you
push a new tag to the master branch.

How It Works
------------

Your project comes with a script called `travis_pypi_setup.py`.

This script does the following:

* Encrypt your PyPI password in your Travis config.
* Activate automated deployment on PyPI when you push a new tag to master.

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

TODO
