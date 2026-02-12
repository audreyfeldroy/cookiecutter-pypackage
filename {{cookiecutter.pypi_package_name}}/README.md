# {{ cookiecutter.project_name }}

![PyPI version](https://img.shields.io/pypi/v/{{ cookiecutter.pypi_package_name }}.svg)

{{ cookiecutter.project_short_description }}

* Created by **[{{ cookiecutter.full_name }}]({{ cookiecutter.author_website if cookiecutter.author_website else 'https://github.com/' + cookiecutter.github_username }})**
{%- if cookiecutter.author_website %}
  * GitHub: https://github.com/{{ cookiecutter.github_username }}
{%- endif %}
  * PyPI: https://pypi.org/user/{{ cookiecutter.pypi_username }}/
* PyPI package: https://pypi.org/project/{{ cookiecutter.pypi_package_name }}/
* Free software: MIT License

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

## Author

{{ cookiecutter.project_name }} was created in {% now 'local', '%Y' %} by {{ cookiecutter.full_name }}.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
