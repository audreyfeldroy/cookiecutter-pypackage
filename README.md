# Cookiecutter PyPackage

[![PyPI version](https://img.shields.io/pypi/v/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)
[![PyPI downloads](https://img.shields.io/pypi/dm/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package with production-ready CI and automated PyPI publishing. Push a tag, your package ships, no token management needed.

```bash
uvx cookiecutter-pypackage
```

## What you get

- **Publish to PyPI by pushing a tag.** Your package is built, signed with [Sigstore](https://docs.pypi.org/attestations/), and published via [Trusted Publishers](https://docs.pypi.org/trusted-publishers/). OIDC-based, no API tokens to manage.
- **Security-hardened CI from the start.** Every GitHub Action pinned by SHA, minimal permissions, no persisted credentials, [Dependabot](https://docs.github.com/en/code-security/dependabot) PRs to stay current. Linting with [ruff](https://docs.astral.sh/ruff/), type checking with [ty](https://docs.astral.sh/ty/), tests across Python 3.12, 3.13, and 3.14.
- **Everything else wired up.** [uv](https://docs.astral.sh/uv/) for dependencies, [just](https://github.com/casey/just) for tasks, [Typer](https://typer.tiangolo.com/) CLI, documentation with [Zensical](https://zensical.org/) auto-deployed to GitHub Pages.

## Quickstart

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
uvx cookiecutter-pypackage
```

You'll be prompted for your package name, GitHub username, and a few other values ([full list](https://audreyfeldroy.github.io/cookiecutter-pypackage/prompts/)). Then push to GitHub and follow the [tutorial](https://audreyfeldroy.github.io/cookiecutter-pypackage/tutorial/) to enable Pages and set up PyPI publishing.

<details>
<summary>Without uvx</summary>

```bash
uv venv
source .venv/bin/activate
uv pip install cookiecutter
cookiecutter gh:audreyfeldroy/cookiecutter-pypackage
```

</details>

## Documentation

**[audreyfeldroy.github.io/cookiecutter-pypackage](https://audreyfeldroy.github.io/cookiecutter-pypackage/)**

- [Tutorial](https://audreyfeldroy.github.io/cookiecutter-pypackage/tutorial/) - from generation to first PyPI release
- [Project Structure](https://audreyfeldroy.github.io/cookiecutter-pypackage/project_structure/) - what's in the generated project
- [GitHub Actions](https://audreyfeldroy.github.io/cookiecutter-pypackage/github_actions/) - CI, publish, docs deployment, security hardening
- [Prompts](https://audreyfeldroy.github.io/cookiecutter-pypackage/prompts/) - what each prompt means
- [Troubleshooting](https://audreyfeldroy.github.io/cookiecutter-pypackage/troubleshooting/)

## Alternatives

This template is opinionated. If it doesn't fit:

- Browse the [fork network](https://github.com/audreyfeldroy/cookiecutter-pypackage/network/members) for variants
- [Create your own](https://github.com/cookiecutter/cookiecutter) template from scratch

Pull requests welcome if they're small, atomic, and improve the template.

---

[Discord](https://discord.gg/PWXJr3upUE) | MIT license
