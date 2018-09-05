.. _development:

Development
===========

Bump a new version
------------------

Make a new version of {{ cookiecutter.project_name }} in the following steps:

  * Make sure everything is commit to GitHub.
  * Update ``CHANGES.rst`` with the next version.
  * Dry Run: ``bumpversion --dry-run --verbose --new-version 0.1.1 patch``
  * Do it: ``bumpversion --new-version 0.1.1 patch``
  * ... or: ``bumpversion --new-version 0.2.0 minor``
  * Push it: ``git push --tags``

See the bumpversion_ documentation for details.

Building the docs
-----------------

First install dependencies for the documentation:

.. code-block:: sh

  $ make bootstrap_dev
  $ make docs

.. _bumpversion: https://pypi.org/project/bumpversion/
