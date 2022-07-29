# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

### [Check Out The Docs](https://juftin.com/ridbpy/)

## Contributing

### Requirements

{{ cookiecutter.project_name }} uses [Poetry] to  manage its Python environment. 
To get started first install `poetry`:

```shell
pipx install poetry
```

[pipx] is preferred, but you can also install with `pip install --user`.

### Coding

{{ cookiecutter.project_name }} makes use of a couple tools to help with contributing via 
`pre-commit`. 

- [pre-commit](https://pre-commit.com/) is a tool to manage git-hooks scripts, which are useful
  for identifying simple issues before submission to code review.
- `{{ cookiecutter.project_name }}`'s instance of `pre-commit` uses tools like [black](https://github.com/psf/black)
  and
  [isort](https://pycqa.github.io/isort/) to format your code in a standardized way.
- `pre-commit` can be installed with pip, brew, or conda.
- After cloning this repo run `pre-commit install`.
- Done, now pre-commit will run automatically on git commit. To run it manually on your changed
  code run `pre-commit run` on your command line.


### Running

Run the command-line interface from the source tree:

```shell
poetry install
poetry run {{ cookiecutter.friendly_name }}
```

Run an interactive Python session:

```shell
poetry install
poetry run python
```

### Testing

- [tox](https://tox.wiki/en/latest/) is a tool to standardize and manage testing and routines
  using Python virtual environments
- `{{ cookiecutter.project_name }}`'s instance of `tox` runs Python unit tests, and uses tools like
  [mypy](https://github.com/python/mypy) and [flake8](https://flake8.pycqa.org/en/latest/pre) to
  format.
- To run all `tox` tests (which get run as part of GitHub Actions) locally, just enter `tox`
  into your command line or use poetry.

Run the Full Test Suite:

```tox
poetry run tox
```

Run Just One Testing Tool:

```shell
poetry run tox -e mypy
```

### Releasing

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

___________
___________

<br/>

[<p align="center" ><img src="{{ cookiecutter.logo_url }}" width="120" height="120"  alt="logo"> </p>](https://github.com/{{ cookiecutter.github_username }})

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
