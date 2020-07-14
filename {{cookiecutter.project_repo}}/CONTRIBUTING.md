# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

# Types of Contributions

## Report Bugs

Report bugs at https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

## Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

## Write Documentation

{{ cookiecutter.project_name }} could always use more documentation, whether as part of the
official {{ cookiecutter.project_name }} docs, in docstrings, or even on the web in blog posts,
articles, and such.

## Submit Feedback

The best way to send feedback is to file an issue at https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

# Get Started!

Ready to contribute? Here's how to set up `{{ cookiecutter.project_slug }}` for local development.

1. [Make sure Poetry is installed](https://python-poetry.org/docs/#installation)
2. Fork the `{{ cookiecutter.project_slug }}` repo on GitHub.
3. Clone your fork locally:
    ```
    $ git clone git@github.com:your_name_here/{{ cookiecutter.project_slug }}.git
    ```
4. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:
    ```
    $ mkvirtualenv {{ cookiecutter.project_slug }}
    $ cd {{ cookiecutter.project_slug }}/
    $ python setup.py develop
    ```

5. Create a branch for local development:
    ```
    $ git checkout -b name-of-your-bugfix-or-feature
    ```
   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass
   the checks and tests, including testing other Python versions with
   tox:
    ```shell script
    make lint
    make test
    make test-all # runs tox
    ```
   To get the required tools for running checks and tests, install them
   into your virtual environment:
   ```shell script
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    source $HOME/.poetry/env
    poetry install
   ```

7. Commit your changes and push your branch to GitHub:
    ```
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```
8. Submit a pull request through the GitHub website.

# Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
3. The pull request should work for Python 3.5, 3.6, 3.7 and 3.8, and for PyPy. Check
   and make sure that the tests pass for all supported Python versions.

# Tips

To run a subset of tests:
```
$ pytest tests.test_{{ cookiecutter.project_slug }}
```

# Deploying

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.md).
Then run:
```
$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags
```
GitHub Actions will then deploy to PyPI if tests pass.
