# Unreleased

This file records user-visible changes since Cookiecutter PyPackage 0.5.0. It
is not a release announcement; finalize it as `CHANGELOG/X.Y.Z.md` during
release preparation.

### Migration for the next release: renamed template variables

The next release gives the project's human-readable name, PyPI package name,
Python import name, and GitHub owner distinct roles.

If you automate project generation or maintain a custom Cookiecutter context, update these variables:

| Before | Next release | Used for |
|---|---|---|
| `pypi_package_name` | `package_name` | PyPI package, GitHub repository, and generated directory |
| `project_slug` | `import_name` | Python imports and the generated CLI command |
| GitHub owner inferred from `github_username` | `github_repo_owner` | Personal or organization-owned repositories |

For example:

```bash
# Before
uvx cookiecutter-pypackage --no-input \
    pypi_package_name=my-package \
    project_slug=my_package

# Next release
uvx cookiecutter-pypackage --no-input \
    package_name=my-package \
    import_name=my_package
```

`github_repo_owner` defaults to `github_username`, so personal projects require no extra configuration. Set it explicitly when the repository belongs to an organization:

```bash
uvx cookiecutter-pypackage --no-input \
    github_username=yourhandle \
    github_repo_owner=your-organization \
    project_name="My Package"
```

Custom forks that referenced the private `__gh_slug` variable should construct the repository path from `github_repo_owner` and `package_name` instead.

These changes affect future generation commands and custom contexts only. Projects you have already generated are not renamed or modified.

### What's new

- **From prompt to pushed repository—with you in control.** GitHub setup defaults to no. If you opt in, visibility defaults to private and the generator shows every planned action before asking for final confirmation. It then creates the repository under the selected owner, initializes Git, makes a descriptive first commit, and pushes `main` using the SSH or HTTPS transport already configured in GitHub CLI.

- **GitHub Pages ready from the first push—when you want it.** Public repositories enable Pages and documentation deployment by default. Private repositories leave both off unless you separately accept a warning that the site can still be public and that private-repository Pages may require a paid plan. When Pages stays off, the docs workflow stays quietly paused instead of turning the first push red.

- **PyPI trusted-publishing setup with fewer detours.** Confirmed GitHub setups create a `pypi` environment before the first push, and the generator prints the exact owner, repository, workflow, environment, and package values needed to register a pending publisher on PyPI.

- **See every template variable before generating.** Run `uvx cookiecutter-pypackage --list-variables` to inspect the current variables and their defaults—particularly useful when building scripts or non-interactive workflows. Thanks [@iamamystery](https://github.com/iamamystery)! ([#931](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/931))

- **A working changelog for generated projects.** New projects start with
  `CHANGELOG/unreleased.md`; `just release` finalizes those notes into the
  versioned file before tagging the release.

### What's better

- **Names that match how Python projects work.** `project_name` is for people, `package_name` is for PyPI and GitHub, and `import_name` is for Python. Package and import names are derived automatically in the common case, while remaining independently customizable.

- **Organization-owned repositories are first-class.** Your personal attribution can remain tied to `github_username` while repository URLs, documentation, security reporting, and automation use `github_repo_owner`.

- **CLI overrides are documented for interactive and automated use.** The README explains `key=value` overrides, `--no-input`, shell quoting, and how to discover the authoritative variable list. ([#932](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/932))

- **Explicit, detectable GitHub automation.** Non-interactive generation skips GitHub by default. Automation can opt in intentionally with `--github private` or `--github public`, while `--github skip` suppresses the setup question during interactive runs. Public automation enables Pages; private automation leaves it disabled. Requested setup failures exit nonzero and preserve the generated directory for recovery.

- **A cleaner first commit.** The generated commit records the package, tests, documentation, workflows, project policies, release tooling, and configuration included in the scaffold, giving the new repository a useful starting history.

- **A verified starter project.** Generated packages pass Ruff and pytest out of the box, use consistent test discovery, and target Python 3.12, 3.13, and 3.14 across their local and CI workflows.

- **Private repositories start cleanly.** Checkout permissions are granted only to the jobs that need them. CodeQL waits for an explicit `CODE_SECURITY_ENABLED=true` opt-in on private repositories, while zizmor keeps auditing in its workflow log without requiring a paid GitHub Code Security feature.

- **Refreshed workflow foundations.** The generated and template-repository workflows use updated SHA-pinned releases of setup-uv, CodeQL, Pages configuration, artifact handling, and zizmor.

Declining or cancelling before final confirmation leaves only the generated project files—no Git commit or remote repository. After confirmation, a command failure can leave a clearly reported, recoverable partial state such as a local commit or an empty remote repository. The package CLI and documented direct Cookiecutter command exit nonzero and keep the generated directory. Existing nonempty repositories are never modified automatically.

### Contributors

[@audreyfeldroy](https://github.com/audreyfeldroy) ([Audrey M. Roy Greenfeld](https://audrey.feldroy.com/)) designed and built the GitHub launch flow, repository-owner model, generated changelog, first-commit experience, and streamlined onboarding documentation.

Thanks to [@iamamystery](https://github.com/iamamystery) (Muhammad Jawad) for adding template-variable discovery and helping shape the CLI examples, and to [@klouds27](https://github.com/klouds27) for the original documentation of `key=value` overrides.
