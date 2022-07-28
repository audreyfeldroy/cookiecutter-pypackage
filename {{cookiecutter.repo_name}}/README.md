# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## [Check Out The Docs](https://juftin.com/ridbpy/)

## Contributing

{{ cookiecutter.project_name }} uses [poetry](https://python-poetry.org/docs/) to
manage its Python environment. To get started first install `poetry` (I recommend using a tool like
`brew` or [pipx](https://github.com/pypa/pipx) to install `poetry`) .

### Installation

```shell
poetry install
poetry run {{ cookiecutter.repo_name }}
```

### Testing

```tox
poetry run tox
```

### Tools

{{ cookiecutter.project_name }} makes use of a couple tools to help with contributing: `pre-commit` and `tox`

```shell
pip install pre-commit
pip install tox

pre-commit install
pre-commit run
tox
```

- `pre-commit`
    - [pre-commit](https://pre-commit.com/) is a tool to manage git-hooks scripts, which are useful
      for identifying simple issues before submission to code review.
    - `{{ cookiecutter.project_name }}`'s instance of `pre-commit` uses tools like [black](https://github.com/psf/black)
      and
      [isort](https://pycqa.github.io/isort/) to format your code in a standardized way
    - `pre-commit` can be installed with pip, brew, or conda.
    - After cloning this repo run `pre-commit install`
    - Done, now pre-commit will run automatically on git commit. To run it manually on your changed
      code run `pre-commit run` on your command line
- `tox`
    - [tox](https://tox.wiki/en/latest/) is a tool to standardize and manage testing and routines
      using Python virtual environments
    - `tox` can be installed with pip
    - `{{ cookiecutter.project_name }}`'s instance of `tox` runs Python unit tests, and uses tools like
      [mypy](https://github.com/python/mypy) and [flake8](https://flake8.pycqa.org/en/latest/pre) to
      format
    - To run all `tox` tests (which get run as part of GitHub Actions) locally, just enter `tox`
      into your command line


___________
___________

<br/>

[<p align="center" ><img src="{{ cookiecutter.logo_url }}" width="120" height="120"  alt="logo"> </p>](https://github.com/{{ cookiecutter.github_username }})
