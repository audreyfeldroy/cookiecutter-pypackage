# Prompts

When you create a package, you are prompted to enter these values.

## Quick example

If your package is called "My Cool Parser":

| Prompt | You enter | Result |
|---|---|---|
| `project_name` | `My Cool Parser` | human-readable name for docs |
| `package_name` | *(press Enter)* | `My-Cool-Parser`, what people `pip install` |
| `import_name` | *(press Enter)* | `my_cool_parser`, what people `import` |

The package name is auto-generated from the project name by replacing spaces with hyphens. The import name is auto-generated from the package name by lowercasing and replacing hyphens with underscores. Most of the time you just press Enter for both.

## All prompts

- **full_name**: Your full name. Used in `pyproject.toml` author field and the LICENSE file.
- **email**: Your email address. Used in `pyproject.toml` author field.
- **github_username**: Your GitHub username. Used to build repo URLs, the GitHub Pages docs URL, and the PyPI profile link.
- **project_name**: The human-readable name of your project. Used in documentation headings and the README. Spaces and any characters are fine.
- **package_name**: The name of your package on PyPI, GitHub repo, and top-level directory. Defaults to `project_name` with spaces replaced by hyphens.
- **import_name**: The Python import name (`import my_cool_parser`). Also used as the CLI command name. Must be a valid Python identifier. Defaults to `package_name` lowercased with hyphens replaced by underscores.
- **project_short_description**: A one-sentence description. Used in `pyproject.toml` and the README.
- **pypi_username**: Your PyPI account username. Used only for a link to your PyPI profile in the README.
- **author_website**: Your personal website URL (optional). When provided, the "Created by" link in the README points here. When left blank, it defaults to your GitHub profile URL.
- **first_version**: The starting version number of the package. Defaults to `0.1.0`.
