# History

## v0.4.0

This is the biggest release since the modern rewrite. Generated projects now ship with a documentation site, type checking, cross-version coverage enforcement, and security-hardened CI, all configured and working out of the box.

### What's new

**Documentation site with Zensical and API autodoc.** Every generated project now includes a [Zensical](https://zensical.org/) documentation site with the Material theme, light/dark mode, and automatic API reference from your docstrings via [mkdocstrings](https://mkdocstrings.github.io/). A GitHub Actions workflow builds the docs and deploys to GitHub Pages. Preview locally with `just docs-serve`. ([#903](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/903))

**Type checking with ty.** Generated packages include a [py.typed](https://peps.python.org/pep-0561/) marker, the "Typing :: Typed" classifier, and type hints on all starter code. CI runs [ty](https://docs.astral.sh/ty/) as a separate job. Locally, `just type-check` runs it once, and `just type-check-watch` re-checks on every save. ([#881](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/881))

**Coverage the coverage.py way.** Branch coverage, parallel mode, cross-version combining (3.12, 3.13, 3.14), and a `fail_under` floor of 50% that users raise as their project grows. CI collects coverage from every Python version, combines the results, and posts a report to the GitHub Actions summary page. Follows the patterns used by coverage.py's own project. ([#904](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/904))

**CLI accepts extra key=value arguments.** Override any template variable from the command line, which is especially useful with `--no-input`:

```bash
uvx cookiecutter-pypackage --no-input full_name="Audrey M. Roy Greenfeld" pypi_package_name=my-package
```

([#877](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/877))

**Creator attribution in generated READMEs.** A bold "Created by" line at the top of the README with links to your GitHub and PyPI profiles. A new `author_website` prompt lets you link to your personal site too. ([#901](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/901))

### What's better

**Security-hardened GitHub Actions.** All workflows use SHA-pinned actions, `persist-credentials: false` on checkouts, minimal permissions, and Dependabot for automated action updates. The publish workflow uses [Trusted Publishers](https://docs.pypi.org/trusted-publishers/) with build provenance attestation and concurrency guards to prevent duplicate publishes. CI workflows include `workflow_dispatch` so you can re-run them manually from the Actions tab.

**Dependency groups (PEP 735).** Generated projects use `[dependency-groups]` instead of `[project.optional-dependencies]` for dev, test, lint, typecheck, and docs. With `default-groups = ["dev"]`, `uv sync` picks up everything automatically. ([#873](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/873))

**Python 3.12+ across the board.** Both the template and the outer repo target Python 3.12, 3.13, and 3.14. The `just testall` recipe and CI matrix match.

**Leaner template.** Removed MANIFEST.in, `.readthedocs.yaml`, empty `slug.py`, empty `tests/__init__.py`, `__author__`/`__email__` dunders, and the ReadTheDocs badge. The starter test file is a clean minimal `test_import`. The .gitignore is focused instead of the 200-line GitHub default. ([#901](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/901))

**Stronger test assertions.** Test comparisons that were evaluated but never asserted are now proper assertions. Thanks [@AndreMiras](https://github.com/AndreMiras)! ([#875](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/875), [#878](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/878))

**Rewritten docs for the template repo itself.** The tutorial walks through all nine steps from generation to PyPI release. The prompts page shows a concrete example. A new project structure page covers every file in the generated project, justfile commands, CI workflows, and configuration. Troubleshooting covers real failure modes. ([#900](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/900))

**Template docs modernized.** Installation docs use `uv sync` instead of `pip install`. CONTRIBUTING.md has full development setup instructions. The changelog URL points to the right file. ([#886](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/886), [#888](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/888), [#894](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/894), [#896](https://github.com/audreyfeldroy/cookiecutter-pypackage/pull/896))

### Made by

[@audreyfeldroy](https://github.com/audreyfeldroy) (Audrey M. Roy Greenfeld) designed and built this release: the Zensical docs system, ty type checking, coverage setup, security-hardened workflows, CLI improvements, creator attribution, dependency groups migration, and the complete docs rewrite.

Thanks to [@AndreMiras](https://github.com/AndreMiras) (Andre Miras) for cleaning up the test file and strengthening test assertions.
