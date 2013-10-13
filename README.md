# cookiecutter-pypackage

Cookiecutter template for a Python package. See
<https://github.com/audreyr/cookiecutter>.


## Features
-   Optional sample CLI with docopt
-   Testing with unittest2 and nosetests
-   [TravisCCI](http://travis-ci.org/): Ready for Travis Continuous
    Integration testing
-   [Tox](http://testrun.org/tox/) testing: Setup to easily test for
    Python 2.6, 2.7, 3.3
-   [Sphinx](http://sphinx-doc.org/) docs: Documentation ready for
    generation with, for example, [ReadTheDocs](https://readthedocs.org/)

## Usage

Generate a Python package project:

    cookiecutter https://github.com/michaeljoseph/cookiecutter-pypackage.git

Then:

-   Create a repo and put it there.
-   Add the repo to your Travis CI account.
-   Add the repo to your ReadTheDocs account + turn on the ReadTheDocs
    service hook.
-   Release your package the standard Python way.
-   Here's a release checklist:
    <https://gist.github.com/audreyr/5990987> or use
    [changes](https://github.com/michaeljoseph/changes)
