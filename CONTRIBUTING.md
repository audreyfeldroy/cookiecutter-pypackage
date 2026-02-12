# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/audreyfeldroy/cookiecutter-pypackage/issues

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement a fix for it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

Cookiecutter PyPackage could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/audreyfeldroy/cookiecutter-pypackage/issues.

If you are proposing a new feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `cookiecutter-pypackage` for local development. Please note this documentation assumes you already have [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just) installed.

1. Fork the `cookiecutter-pypackage` repo on GitHub.
2. Clone your fork locally:

   ```sh
   git clone git@github.com:your_name_here/cookiecutter-pypackage.git
   ```

3. Install dependencies:

   ```sh
   cd cookiecutter-pypackage/
   uv sync
   ```

4. Create a branch for local development:

   ```sh
   git checkout -b name-of-your-bugfix-or-feature
   ```

   Now you can make your changes locally.

5. The tests use [pytest-cookies](https://pypi.org/project/pytest-cookies/) to "bake" the template (generate a project from it) and verify the output. Run them with:

   ```sh
   just test
   ```

   Or directly:

   ```sh
   uv run pytest tests/
   ```

6. For faster iteration on template changes, use the development watcher. It watches the `{{cookiecutter.pypi_package_name}}/` directory and regenerates the output whenever you save a file:

   ```sh
   uv run python run.py
   ```

7. Commit your changes and push your branch to GitHub:

   ```sh
   git add .
   git commit -m "Your detailed description of your changes."
   git push origin name-of-your-bugfix-or-feature
   ```

8. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests if applicable.
2. If the pull request changes the generated template, make sure `pytest tests/` still passes.
3. Keep commits small and atomic. One logical change per commit.

## Releasing

1. Bump the version:

   ```sh
   uv version --bump patch  # or minor, major
   ```

2. Commit the version bump.
3. Tag and push:

   ```sh
   just tag
   ```

   This creates an annotated git tag from the version in `pyproject.toml` and pushes it. The tag push triggers a GitHub Action that builds and publishes to PyPI.
