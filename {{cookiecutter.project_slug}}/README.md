# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Install

1. Create virtual environment and activate:

    `python -m venv .venv && source .venv/bin/activate`

2. Install package

    `pip install -e . -r requirements.txt`

    Or with optional dev dependencies:

    `pip install -e ".[dev]" -r requirements.txt -r requirements_dev.txt`

## Developer Notes

### Manage Dependencies

Dependencies are managed with [pip-tools](https://github.com/jazzband/pip-tools/).

1. Install `pip-tools` (globally with [pipx](https://github.com/pypa/pipx) or in local virtual environment with pip)

2. Generate lock file:

    `pip-compile --extra dev -o requirements_dev.txt pyproject.toml --quiet`

To upgrade a dependency, pass the `--upgrade-package` flag along with the name of the package, or to upgrade all packages, pass the `--upgrade` flag to the command.

More information at: <https://github.com/jazzband/pip-tools/>
