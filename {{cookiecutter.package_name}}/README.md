# {{ cookiecutter.project_name }}

[![PyPI version](https://img.shields.io/pypi/v/{{ cookiecutter.package_name }}.svg)](https://pypi.org/project/{{ cookiecutter.package_name }}/)
[![PyPI downloads](https://static.pepy.tech/badge/{{ cookiecutter.package_name }}/month)](https://pepy.tech/projects/{{ cookiecutter.package_name }})

{{ cookiecutter.project_short_description }}

* [GitHub](https://github.com/{{ cookiecutter.github_repo_owner }}/{{ cookiecutter.package_name }}/) | [PyPI](https://pypi.org/project/{{ cookiecutter.package_name }}/) | [Documentation](https://{{ cookiecutter.github_repo_owner }}.github.io/{{ cookiecutter.package_name }}/)
* Created by [{{ cookiecutter.full_name }}]({{ cookiecutter.author_website if cookiecutter.author_website else 'https://github.com/' + cookiecutter.github_username }}) | {% if cookiecutter.author_website %}GitHub [@{{ cookiecutter.github_username }}](https://github.com/{{ cookiecutter.github_username }}) | {% endif %}PyPI [@{{ cookiecutter.pypi_username }}](https://pypi.org/user/{{ cookiecutter.pypi_username }}/)
* MIT License

## Features

* TODO

## Documentation

Documentation is built with [Zensical](https://zensical.org/) and deployed to GitHub Pages.

* **Live site:** https://{{ cookiecutter.github_repo_owner }}.github.io/{{ cookiecutter.package_name }}/
* **Preview locally:** `just docs-serve` (serves at http://localhost:8000)
* **Build:** `just docs-build`

API documentation is auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Docs deploy automatically on push to `main` after GitHub Pages is enabled. If
the generator did not enable it, review the visibility implications first:
[Pages sites can be public even when their repositories are private](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site),
and the feature may require a paid GitHub plan for private repositories. Then
go to Settings > Pages, set the source to **GitHub Actions**, and enable the
deployment workflow:

```bash
gh variable set DOCS_DEPLOYMENT_ENABLED \
    --repo {{ cookiecutter.github_repo_owner }}/{{ cookiecutter.package_name }} \
    --body true
```

Until then, deployment stays paused and local preview and builds still work.

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:your_username/{{ cookiecutter.package_name }}.git
cd {{ cookiecutter.package_name }}

# Install in editable mode with live updates
uv tool install --editable .
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `{{ cookiecutter.import_name }}`.

Run tests:

```bash
uv run pytest
```

Use the quality commands:

```bash
just fix             # apply Ruff formatting and safe lint fixes
just check           # verify formatting, linting, types, and Python 3.14 tests
just fix-and-check   # apply fixes, then verify
```

Use `just testall` to run tests on Python 3.12, 3.13, and 3.14. GitHub CI runs that test matrix on pushes to `main` and on pull requests.

## Author

{{ cookiecutter.project_name }} was created in {% now 'local', '%Y' %} by {{ cookiecutter.full_name }}.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
