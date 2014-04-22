======================
cookiecutter-pypackage
======================

Cookiecutter template for a Python package. See https://github.com/saulshanabrook/cookiecutter.

* Free software: BSD license
* py.test, pep8 and coveralls suport
* Travis-CI_: Ready for Travis Continuous Integration testing
* Tox_ testing: Setup to easily test for Python 2.7, 3.3, 3.4
* Sphinx_ docs: Supports autodoc and ready for generation with ReadTheDocs_
* Releases_ changelog: Autocreate pretty releases 
Usage
-----

Generate a Python package project::

    cookiecutter https://github.com/saulshanabrook/cookiecutter-pypackage.git

Then:

* Create a repo and put it there.
* Add the repo to your Travis CI account.
* Add the repo to your ReadTheDocs account + turn on the ReadTheDocs service hook.
* Release your package the standard Python way. Here's a release checklist: https://gist.github.com/audreyr/5990987


Submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~

I also accept pull requests on this, if they're small, atomic, and if they
make my own packaging experience better.


.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.org/
.. _Releases: https://github.com/bitprophet/releases
