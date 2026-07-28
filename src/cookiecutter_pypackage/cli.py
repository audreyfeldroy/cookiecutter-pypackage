"""CLI for cookiecutter-pypackage.

Usage:
    uvx cookiecutter-pypackage
    uvx cookiecutter-pypackage --no-input
    uvx cookiecutter-pypackage --list-variables
    uvx cookiecutter-pypackage --github private
    uvx cookiecutter-pypackage --no-input --github private
    uvx cookiecutter-pypackage -o /path/to/output
    uvx cookiecutter-pypackage full_name="Audrey M. Roy Greenfeld" github_username=audreyfeldroy
    uvx cookiecutter-pypackage --no-input full_name="Audrey M. Roy Greenfeld" email="audreyfeldroy@example.com"
"""

import json
import os
from enum import Enum
from pathlib import Path

import typer
from cookiecutter.main import cookiecutter

GITHUB_SETUP_ENV = "COOKIECUTTER_PYPACKAGE_GITHUB"


class GitHubSetupMode(str, Enum):
    """How the post-generation hook should handle GitHub setup."""

    ASK = "ask"
    SKIP = "skip"
    PRIVATE = "private"
    PUBLIC = "public"


app = typer.Typer(
    help="Generate a Python package from the cookiecutter-pypackage template.",
    add_completion=False,
)


def _find_template_dir() -> Path:
    """Locate the template in an installed package or source checkout."""
    package_dir = Path(__file__).parent
    candidates = (package_dir / "template", package_dir.parent.parent)
    for candidate in candidates:
        if (candidate / "cookiecutter.json").is_file():
            return candidate
    raise FileNotFoundError("Could not locate the cookiecutter template")


@app.command(
    context_settings={"allow_extra_args": True, "allow_interspersed_args": False}
)
def main(
    ctx: typer.Context,
    output_dir: Path | None = typer.Option(
        None, "--output-dir", "-o", help="Where to output the generated project"
    ),
    no_input: bool = typer.Option(
        False, "--no-input", help="Do not prompt for parameters, use defaults"
    ),
    list_variables: bool = typer.Option(
        False,
        "--list-variables",
        help="List available template variables and their defaults",
    ),
    github: GitHubSetupMode = typer.Option(
        GitHubSetupMode.ASK,
        "--github",
        case_sensitive=False,
        help="GitHub setup: ask, skip, private, or public",
    ),
) -> None:
    """Generate a new Python package from the cookiecutter-pypackage template.

    You can pass extra key=value pairs to override template variables:
        uvx cookiecutter-pypackage full_name="Audrey M. Roy Greenfeld" github_username=audreyfeldroy
    """
    template_dir = _find_template_dir()

    if list_variables:
        cookiecutter_json = template_dir / "cookiecutter.json"
        variables = json.loads(cookiecutter_json.read_text(encoding="utf-8"))
        typer.echo("Available template variables:")
        for key, value in variables.items():
            if not key.startswith("_"):
                typer.echo(f"  {key} (default: {value!r})")
        raise typer.Exit()

    extra_context = {}
    for arg in ctx.args:
        if "=" not in arg:
            typer.echo(
                f"Error: extra argument '{arg}' must be in key=value format", err=True
            )
            raise typer.Exit(code=1)
        key, value = arg.split("=", 1)
        extra_context[key] = value

    github_mode = github
    if no_input and github_mode is GitHubSetupMode.ASK:
        github_mode = GitHubSetupMode.SKIP

    previous_github_mode = os.environ.get(GITHUB_SETUP_ENV)
    os.environ[GITHUB_SETUP_ENV] = github_mode.value
    try:
        cookiecutter(
            str(template_dir),
            output_dir=str(output_dir) if output_dir else ".",
            no_input=no_input,
            extra_context=extra_context or None,
        )
    finally:
        if previous_github_mode is None:
            os.environ.pop(GITHUB_SETUP_ENV, None)
        else:
            os.environ[GITHUB_SETUP_ENV] = previous_github_mode


if __name__ == "__main__":
    app()
