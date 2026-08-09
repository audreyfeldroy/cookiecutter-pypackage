# Unreleased

Good projects are built through ordinary repetitions: starting a repository,
making a change, checking it, releasing it, and returning to it later. This
release makes those repetitions easier to do well.

**Projects you have already generated remain as they are.** These changes apply
when you generate your next project. The migration notes at the end are for
saved contexts, scripts, and custom forks.

## Make the next action clear

- **Names with distinct jobs.** `project_name` is the human name,
  `package_name` is the package and repository identity, and `import_name` is
  the Python identifier. They derive naturally in the common case, while still
  allowing the three to differ when the project needs them to.

- **See the variables before you generate.**
  `uvx cookiecutter-pypackage --list-variables` shows the current prompts and
  defaults before it creates anything. Documented `key=value` overrides make
  interactive and automated generation repeatable. Thanks
  [@iamamystery](https://github.com/iamamystery).

- **Use one repeatable quality loop.** `just fix` applies automatic Ruff fixes.
  `just check` verifies formatting, linting, types, and tests without changing
  files. `just fix-and-check` runs the two in order. `just qa` remains
  available as a compatibility alias.

- **Record changes while they are fresh.** New projects include an unreleased
  changelog. `just release` turns those notes into a versioned file, tags the
  release, and creates the GitHub release.

## Share when you are ready

- **Set up GitHub on your terms.** GitHub setup is off by default and private
  by default. It shows the plan and asks for final confirmation before acting.
  When confirmed, it initializes the local repository and first commit, then
  creates or connects to the selected GitHub repository and pushes `main` using
  your configured SSH or HTTPS transport.

- **GitHub Pages that follow your choice.** Public projects can enable Pages
  and docs deployment. Private projects keep them off unless you explicitly
  accept the visibility and plan implications. When Pages is disabled, its
  deployment remains paused.

- **Prepare trusted publishing as part of setup.** Confirmed GitHub setup
  creates the PyPI environment and gives you the exact values needed to
  register a pending publisher.

## Keep the project dependable

- **Begin with the working pieces in place.** The scaffold includes a typed
  `src` layout, CLI, documentation, tests, and CI across Python 3.12, 3.13,
  and 3.14.

- **Private repository support.** Least-privilege workflows, conditional
  CodeQL, and workflow auditing support private repositories. Paid GitHub
  CodeQL features remain opt-in.

- **See the state of setup clearly.** Declining GitHub setup leaves the
  generated project local. Requested setup reports recoverable partial state if
  a later step fails; existing nonempty repositories remain untouched.

- **One Python style from template to generated project.** Ruff now uses 120
  columns in both layers, so mirrored tooling stays readable and in sync.
  Typer's `Option` and `Argument` declarations are handled precisely without
  weakening other default-argument checks.

- **Keep the tooling current.** Tooling and SHA-pinned workflows are refreshed,
  and Dependabot keeps Python and GitHub Actions dependencies moving.

## Contributors

Created and maintained by [Audrey M. Roy Greenfeld](https://audrey.feldroy.com/)
([@audreyfeldroy](https://github.com/audreyfeldroy)), who designed and built
the GitHub launch flow, repository-owner model, generated changelog,
first-commit experience, and streamlined onboarding documentation.

Thanks to [@klouds27](https://github.com/klouds27) for the original
`key=value` override documentation in [#907](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/907), which became the foundation of [#932](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/932); and to [@iamamystery](https://github.com/iamamystery) (Muhammad Jawad) for the clearer current-variable examples consolidated from [#929](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/929) and [#930](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/930), and for the `--list-variables` feature in [#931](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/931).

## Migration notes for custom contexts and automation

If you generate interactively, there is nothing to do. Existing generated
projects are unchanged. Update only saved Cookiecutter contexts, scripts, and
custom forks.

This is not a one-to-one rename: the next release consolidates the distribution,
repository, and generated directory under `package_name`, while reserving
`import_name` for Python.

| Earlier context | Next release | Responsibility now |
|---|---|---|
| `pypi_package_name` | `package_name` | PyPI distribution, GitHub repository, and generated directory |
| `project_slug` | `import_name` | Python imports and the generated CLI command |
| `github_username` as repository owner | `github_repo_owner` | GitHub user or organization that owns the repository |

Previously, the package and import-style names could both appear in GitHub
references: some links used `pypi_package_name`, while the private `__gh_slug`
was built from `project_slug`. New projects use
`github_repo_owner/package_name` consistently for GitHub, documentation, and
security URLs.

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

`github_repo_owner` defaults to `github_username`, so personal projects need
no extra configuration. Set it explicitly when the repository belongs to an
organization:

```bash
uvx cookiecutter-pypackage --no-input \
    github_username=yourhandle \
    github_repo_owner=your-organization \
    project_name="My Package"
```

Custom forks that referenced the private `__gh_slug` variable should construct
the repository path from `github_repo_owner` and `package_name` instead.
