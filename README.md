# Cookiecutter PyPackage

[![PyPI version](https://img.shields.io/pypi/v/cookiecutter-pypackage.svg)](https://pypi.org/project/cookiecutter-pypackage/)
[![PyPI downloads](https://static.pepy.tech/badge/cookiecutter-pypackage/month)](https://pepy.tech/projects/cookiecutter-pypackage)

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python package with production-ready CI and automated PyPI publishing.

* [GitHub](https://github.com/audreyfeldroy/cookiecutter-pypackage/) | [PyPI](https://pypi.org/project/cookiecutter-pypackage/) | [Documentation](https://audreyfeldroy.github.io/cookiecutter-pypackage/)
* Created by [Audrey M. Roy Greenfeld](https://audrey.feldroy.com/) | GitHub [@audreyfeldroy](https://github.com/audreyfeldroy) | PyPI [@audreyr](https://pypi.org/user/audreyr/)
* MIT License

## What you get

### Tooling

| | Tool | |
|---|---|---|
| Package manager | [uv](https://docs.astral.sh/uv/) | Fast, handles venvs automatically |
| Task runner | [just](https://github.com/casey/just) | `just fix` applies safe fixes, `just check` verifies, and `just fix-and-check` does both |
| Linting | [ruff](https://docs.astral.sh/ruff/) | Format + lint in one tool |
| Type checking | [ty](https://docs.astral.sh/ty/) | All rules enabled, watch mode with `just type-check-watch` |
| Testing | [pytest](https://docs.pytest.org/) | `just check` tests Python 3.14; `just testall` and CI cover 3.12, 3.13, and 3.14 |
| CLI framework | [Typer](https://typer.tiangolo.com/) | Entry point + `__main__.py` included |
| Docs | [Zensical](https://zensical.org/) + [mkdocstrings](https://mkdocstrings.github.io/) | GitHub Pages deployment, API docs from docstrings |

### CI/CD (GitHub Actions, [security-hardened](https://audreyfeldroy.github.io/cookiecutter-pypackage/github_actions/))

| Workflow | Trigger | What happens |
|---|---|---|
| **CI** | Push to main, PRs | Lint, type check, test across 3 Python versions |
| **Publish** | `v*` tag | Build, [Sigstore](https://docs.pypi.org/attestations/) attestation, PyPI via [Trusted Publishers](https://docs.pypi.org/trusted-publishers/) (no tokens) |
| **Docs** | Push to main | Build and deploy to GitHub Pages |
| **Dependabot** | Weekly | PRs to update Python dependencies and SHA-pinned actions |

All actions pinned by SHA, minimal permissions, no persisted credentials.

## Quickstart

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```bash
uvx cookiecutter-pypackage
```

You'll be prompted for your package name, GitHub username, and a few other
values ([full list](https://audreyfeldroy.github.io/cookiecutter-pypackage/prompts/)).
Follow the [tutorial](https://audreyfeldroy.github.io/cookiecutter-pypackage/tutorial/)
to generate, verify, and release your package.

<details>
<summary>Without uvx</summary>

```bash
uv venv
source .venv/bin/activate
uv pip install cookiecutter
cookiecutter --keep-project-on-failure gh:audreyfeldroy/cookiecutter-pypackage
```

</details>

## Override template variables

Pass `key=value` arguments to prefill prompts, or add `--no-input` for
automation:

```bash
uvx cookiecutter-pypackage full_name="Your Name"
```

See [Template prompts and command-line options](https://audreyfeldroy.github.io/cookiecutter-pypackage/prompts/)
for all variables, defaults, and automation options.

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

## Cookiecutter PyPackage and WriterStead

I maintain Cookiecutter PyPackage as part of how I build software. When
[WriterStead](https://writerstead.com/from/cc-py)
needs new Air packages, I improve the shared foundation here first so other
Python developers can benefit too.

If Cookiecutter PyPackage has helped you, I’d love it if you helped me sustain
my efforts here by showing WriterStead some love: join the early-access list, or
introduce it to a writer friend who wants a website or blog.

**[Meet WriterStead ->](https://writerstead.com/from/cc-py)**

---

[Discord](https://discord.gg/PWXJr3upUE) | MIT license
