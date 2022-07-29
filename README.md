# Quickstart Guide

## Requirements

Install [Cookiecutter]:

```shell
pipx install cookiecutter
```

Install [Poetry]:

```shell
pipx install poetry
```

[pipx] is preferred, but you can also install with `pip install --user`.

## Creating a project

Generate a Python project:

```shell
cookiecutter gh:juftin/cookiecutter-pypackage
```

Change to the root directory of your new project, create a Git
repository, and install [pre-commit]

```shell
git init
pre-commit install
pre-commit run --all-files
git add .
git commit
```

## Running

Run the command-line interface from the source tree:

```shell
poetry install
poetry run <project>
```

Run an interactive Python session:

```shell
poetry install
poetry run python
```

## Testing

Run the full test suite:

```shell
poetry run tox
```

## Continuous Integration

### GitHub

1. Sign up at [GitHub].
2. Create an empty repository for your project.
3. Follow the instructions to push an existing repository from the command line.
4. Go to the repository settings on GitHub, and
   add a secret named `PERSONAL_ACCESS_TOKEN` with your GitHub Personal Access Token.

### PyPI

1. Sign up at [PyPI].
2. Go to the Account Settings on PyPI,
   generate an API token, and copy it.
3. Go to the repository settings on GitHub, and
   add a secret named `PYPI_TOKEN` with the token you just copied.

### Read the Docs

1. Sign up at [Read the Docs].
2. Import your GitHub repository, using the button _Import a Project_.
3. Install the GitHub webhook,
   using the button _Add integration_
   on the _Integrations_ tab
   in the _Admin_ section of your project
   on Read the Docs.

## Releasing

Releases are triggered entirely by CI/CD via Pull requests being merged into
the main branch.

The version bump on each release is decided by the labels placed on the Pull Requests.
There must be one, and only one, of the following labels on each pull request to the main branch:
`MAJOR`, `MINOR`, `PATCH`. Pull Requests will be un-mergeable unless the version on
your `pyproject.toml` matches the main branch and the proper version labels are applied.

The Release workflow performs the following automated steps:

- Build and upload the package to PyPI.
- Apply a version tag to the repository.
- Publish a GitHub Release.

Release notes are populated with the titles and authors of merged pull requests.
You can group the pull requests into separate sections
by applying labels to them, like this:

<!-- table-release-drafter-sections-begin -->

| Pull Request Label | Section in Release Notes     |
| ------------------ | ---------------------------- |
| `breaking`         | 💥 Breaking Changes          |
| `enhancement`      | 🚀 Features                  |
| `removal`          | 🔥 Removals and Deprecations |
| `bug`              | 🐞 Fixes                     |
| `performance`      | 🐎 Performance               |
| `testing`          | 🚨 Testing                   |
| `ci`               | 👷 Continuous Integration    |
| `documentation`    | 📚 Documentation             |
| `refactoring`      | 🔨 Refactoring               |
| `style`            | 💄 Style                     |
| `dependencies`     | 📦 Dependencies              |

<!-- table-release-drafter-sections-end -->

[codecov]: https://codecov.io/
[cookiecutter]: https://github.com/audreyr/cookiecutter
[github]: https://github.com/
[install-poetry.py]: https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py
[nox]: https://nox.thea.codes/
[nox-poetry]: https://nox-poetry.readthedocs.io/
[pipx]: https://pipxproject.github.io/pipx/
[poetry]: https://python-poetry.org/
[poetry version]: https://python-poetry.org/docs/cli/#version
[pyenv]: https://github.com/pyenv/pyenv
[pypi]: https://pypi.org/
[read the docs]: https://readthedocs.org/
[testpypi]: https://test.pypi.org/
[pre-commit]: https://pre-commit.com/
