======================
cookiecutter-pypackage
======================

Cookiecutter template for a Python package. See https://github.com/audreyr/cookiecutter.

* Free software: BSD license
* Vanilla testing setup with `unittest` and `python setup.py test`
* Travis-CI_: Ready for Travis Continuous Integration testing
* Tox_ testing: Setup to easily test for Python 2.6, 2.7, 3.3
* Sphinx_ docs: Documentation ready for generation with, for example, ReadTheDocs_

Usage
-----

Generate a Python package project::

    cookiecutter https://github.com/Xumeiquer/cookiecutter-pypackage.git

Then:

* Create a repo and put it there.
* Add the repo to your Travis CI account.
* Add the repo to your ReadTheDocs account + turn on the ReadTheDocs service hook.
* Release your package the standard Python way.

Not Exactly What You Want?
--------------------------

Don't worry, you have options:

Similar Cookiecutter Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `audreyr/cookiecutter-pypackage`: The original pypackage, uses unittest
for testing and other minor changes.

Fork This / Create Your Own
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have differences in your preferred setup, I encourage you to fork this
to create your own version. Or create your own; it doesn't strictly have to
be a fork.

* Once you have your own version working, add it to the Similar Cookiecutter
  Templates list above with a brief description. 

* It's up to you whether or not to rename your fork/own version. Do whatever
  you think sounds good.

Or Submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~~~

I also accept pull requests on this, if they're small, atomic, and if they
make my own packaging experience better.


.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.org/
.. _`Nekroze/cookiecutter-pypackage`: https://github.com/Nekroze/cookiecutter-pypackage
.. _`lucuma/cookiecutter-pypackage`: https://github.com/lucuma/cookiecutter-pypackage
.. _`network`: https://github.com/audreyr/cookiecutter-pypackage/network
.. _`family tree`: https://github.com/audreyr/cookiecutter-pypackage/network/members