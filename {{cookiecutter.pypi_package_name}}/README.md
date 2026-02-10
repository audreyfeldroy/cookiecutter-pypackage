# {{ cookiecutter.project_name }}

![PyPI version](https://img.shields.io/pypi/v/{{ cookiecutter.pypi_package_name }}.svg)
[![Documentation Status](https://readthedocs.org/projects/{{ cookiecutter.pypi_package_name }}/badge/?version=latest)](https://{{ cookiecutter.pypi_package_name }}.readthedocs.io/en/latest/?version=latest)

{{ cookiecutter.project_short_description }}

* PyPI package: https://pypi.org/project/{{ cookiecutter.pypi_package_name }}/
* Free software: MIT License
* Documentation: https://{{ cookiecutter.pypi_package_name }}.readthedocs.io.

## Features

* TODO

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:your_username/{{ cookiecutter.pypi_package_name }}.git
cd {{ cookiecutter.pypi_package_name }}

# Install in editable mode with live updates
uv tool install --editable .
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `{{ cookiecutter.project_slug }}`.

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
just qa
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
