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
- **github_username**: Your GitHub username. Used for the "Created by" link in the README and the PyPI profile link. Defaults `github_repo_owner` to this value.
- **github_repo_owner**: The GitHub account or organization that owns the repo. Defaults to `github_username`. Override this when your repo lives under an organization (e.g. `feldroy` instead of `audreyfeldroy`). Used in all repo URLs, GitHub Pages docs URL, and security advisory links.
- **project_name**: The human-readable name of your project. Used in documentation headings and the README. Spaces and any characters are fine.
- **package_name**: The name of your package on PyPI, GitHub repo, and top-level directory. Defaults to `project_name` with spaces replaced by hyphens.
- **import_name**: The Python import name (`import my_cool_parser`). Also used as the CLI command name. Must be a valid Python identifier. Defaults to `package_name` lowercased with hyphens replaced by underscores.
- **project_short_description**: A one-sentence description. Used in `pyproject.toml` and the README.
- **pypi_username**: Your PyPI account username. Used only for a link to your PyPI profile in the README.
- **author_website**: Your personal website URL (optional). The configured
  default is the template author's website, so replace it with your own. To
  link the "Created by" text to your GitHub profile instead, pass an explicit
  empty override such as `author_website=""` when you start the generator.
- **first_version**: The starting version number of the package. Defaults to `0.1.0`.

## Command-line options

Pass `key=value` arguments to prefill the interactive prompts. You can still
review or change each value:

```bash
uvx cookiecutter-pypackage \
    full_name="Your Name" \
    github_username=yourhandle
```

Quote values that contain spaces so the shell passes each assignment as one
argument:

```bash
full_name="First Last"  # correct
full_name=First Last    # incorrect
```

For non-interactive automation, add `--no-input` before the overrides.
Variables you don't pass use the defaults in
[`cookiecutter.json`](https://github.com/audreyfeldroy/cookiecutter-pypackage/blob/main/cookiecutter.json):

```bash
uvx cookiecutter-pypackage --no-input \
    full_name="Your Name" \
    email="you@example.com"
```

Non-interactive generation skips GitHub setup unless you explicitly request a
private or public repository:

```bash
uvx cookiecutter-pypackage --no-input --github private \
    full_name="Your Name" \
    email="you@example.com" \
    github_username=yourhandle \
    author_website="" \
    project_name="My Package" \
    package_name=my-package
```

`--github public` also enables Pages and docs deployment. `--github private`
leaves both disabled; run interactively if you want to acknowledge the
visibility warning and enable them. If requested GitHub setup fails, the
command exits nonzero and keeps the generated directory for recovery.

Use `--github skip` to suppress the GitHub question during interactive
generation.

List the available variables and their configured defaults without generating
a project:

```bash
uvx cookiecutter-pypackage --list-variables
```

## GitHub setup

After the template prompts, the generator separately asks whether to set up a
GitHub repository. Pressing Enter selects no and leaves the generated project
without a Git commit or remote repository.

If you opt in, visibility defaults to private. The generator shows the full
plan and asks for final confirmation before it creates or connects to an empty
repository, initializes Git, pushes `main`, enables Pages, or creates the
`pypi` environment. The plan also shows whether the docs deployment workflow
will be enabled or paused. Existing nonempty repositories are never modified
automatically.

Pages is a separate decision. It defaults to on for public repositories. For
private or internal repositories, it defaults to off and warns that the
published site can still be public and that the feature may require a paid
GitHub plan. The generator displays the actual visibility before asking to
connect to an existing empty repository. The docs deployment workflow follows
the confirmed Pages choice, avoiding a failed deployment when Pages is off.

For non-interactive use, `--no-input` skips GitHub setup unless you add
`--github private` or `--github public`. Public automation enables Pages;
private automation leaves it and docs deployment disabled. A requested setup
failure exits nonzero while preserving the generated project directory.

For a confirmed HTTPS setup, the generator configures Git to use the GitHub CLI
credential helper for `github.com`, so an authenticated `gh` session can also
complete the first push. SSH setup does not change Git credential helpers.
