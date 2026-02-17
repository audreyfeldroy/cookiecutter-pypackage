# Cookiecutter PyPackage

[![PyPI version](https://img.shields.io/pypi/v/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)
[![PyPI downloads](https://img.shields.io/pypi/dm/cookiecutter-pypackage.svg)](https://pypi.python.org/pypi/cookiecutter-pypackage)

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package with production-ready CI and automated PyPI publishing. Push a tag, your package ships, no token management needed.

```bash
uvx cookiecutter-pypackage
```

## What you get

### Tooling

| | Tool | |
|---|---|---|
| Package manager | [uv](https://docs.astral.sh/uv/) | Fast, handles venvs automatically |
| Task runner | [just](https://github.com/casey/just) | `just qa` formats, lints, type-checks, and tests |
| Linting | [ruff](https://docs.astral.sh/ruff/) | Format + lint in one tool |
| Type checking | [ty](https://docs.astral.sh/ty/) | All rules enabled, watch mode with `just type-check-watch` |
| Testing | [pytest](https://docs.pytest.org/) | Python 3.12, 3.13, 3.14 |
| CLI framework | [Typer](https://typer.tiangolo.com/) | Entry point + `__main__.py` included |
| Docs | [Zensical](https://zensical.org/) + [mkdocstrings](https://mkdocstrings.github.io/) | Auto-deployed to GitHub Pages, API docs from docstrings |

### CI/CD (GitHub Actions, [security-hardened](https://audreyfeldroy.github.io/cookiecutter-pypackage/github_actions/))

| Workflow | Trigger | What happens |
|---|---|---|
| **CI** | Push, PRs | Lint, type check, test across 3 Python versions |
| **Publish** | `v*` tag | Build, [Sigstore](https://docs.pypi.org/attestations/) attestation, PyPI via [Trusted Publishers](https://docs.pypi.org/trusted-publishers/) (no tokens) |
| **Docs** | Push to main | Build and deploy to GitHub Pages |
| **Dependabot** | Weekly | PRs to update SHA-pinned actions |

All actions pinned by SHA, minimal permissions, no persisted credentials.

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
