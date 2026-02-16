# Troubleshooting

> **Note:** Can you help improve this file? [Edit this file](https://github.com/audreyfeldroy/cookiecutter-pypackage/blob/main/docs/troubleshooting.md) and submit a pull request with your improvements!

## `just: command not found`

[just](https://github.com/casey/just#installation) is the task runner used by the generated project. It needs to be installed separately from uv. On macOS: `brew install just`. See the [just installation docs](https://github.com/casey/just#installation) for other platforms.

## Docs site shows 404

Make sure GitHub Pages is configured to deploy from **GitHub Actions** (not a branch). Go to your repo's Settings > Pages and set the source to **GitHub Actions**. If the docs workflow already ran before you enabled Pages, go to Actions, find the "Documentation" workflow, and click "Re-run all jobs."

## Tag push didn't publish to PyPI

The most common causes:

- **Trusted Publisher not configured.** You need to register your repo as a trusted publisher on PyPI before the first release. See the [PyPI Release Checklist](pypi_release_checklist.md).
- **`pypi` environment not created.** Go to your repo's Settings > Environments and create an environment named `pypi`.
- **Tag format wrong.** Tags must match `v*` (e.g., `v0.1.0`). The `just tag` command handles this for you.

If you got the Trusted Publisher configuration wrong, you can delete it on PyPI and create it again.

## Type checker reports errors

[ty](https://docs.astral.sh/ty/) runs with all rules enabled as errors by default. If you see errors from third-party library types, you can relax specific rules in `pyproject.toml`:

```toml
[tool.ty]
rules.TY015 = "warn"  # Change from error to warning
```

See the [ty documentation](https://docs.astral.sh/ty/) for the full list of rules.

## Windows issues

- Some people have reported issues using git bash. Try using the Command Terminal instead.
- If you run into environment issues, make sure [uv](https://docs.astral.sh/uv/) is installed and run `uv sync` from your project directory. uv handles virtual environments automatically.
