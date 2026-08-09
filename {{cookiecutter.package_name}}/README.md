# {{ cookiecutter.project_name }}

[![PyPI version](https://img.shields.io/pypi/v/{{ cookiecutter.package_name }}.svg)](https://pypi.org/project/{{ cookiecutter.package_name }}/)
[![PyPI downloads](https://static.pepy.tech/badge/{{ cookiecutter.package_name }}/month)](https://pepy.tech/projects/{{ cookiecutter.package_name }})

{{ cookiecutter.project_short_description }}

* [GitHub](https://github.com/{{ cookiecutter.github_repo_owner }}/{{ cookiecutter.package_name }}/) | [PyPI](https://pypi.org/project/{{ cookiecutter.package_name }}/) | [Documentation](https://{{ cookiecutter.github_repo_owner }}.github.io/{{ cookiecutter.package_name }}/)
* Created by [{{ cookiecutter.full_name }}]({{ cookiecutter.author_website if cookiecutter.author_website else 'https://github.com/' + cookiecutter.github_username }}) | {% if cookiecutter.author_website %}GitHub [@{{ cookiecutter.github_username }}](https://github.com/{{ cookiecutter.github_username }}) | {% endif %}PyPI [@{{ cookiecutter.pypi_username }}](https://pypi.org/user/{{ cookiecutter.pypi_username }}/)
* MIT License

## Features

* TODO

## Installation

```bash
uv add {{ cookiecutter.package_name }}
```

## Usage

```python
import {{ cookiecutter.import_name }}
```

## Documentation

Full documentation is available on
[GitHub Pages](https://{{ cookiecutter.github_repo_owner }}.github.io/{{ cookiecutter.package_name }}/).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, testing, and
documentation instructions.

## Author

{{ cookiecutter.project_name }} was created in {% now 'local', '%Y' %} by {{ cookiecutter.full_name }}.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
