"""CLI for cookiecutter-pypackage.

Usage:
    uvx cookiecutter-pypackage
    uvx cookiecutter-pypackage --no-input
    uvx cookiecutter-pypackage -o /path/to/output
    uvx cookiecutter-pypackage full_name="Audrey M. Roy Greenfeld" github_username=audreyfeldroy
    uvx cookiecutter-pypackage --no-input full_name="Audrey M. Roy Greenfeld" email="audreyfeldroy@example.com"
"""

from pathlib import Path
from typing import Optional

import typer
from cookiecutter.main import cookiecutter

app = typer.Typer(
    help="Generate a Python package from the cookiecutter-pypackage template.",
    add_completion=False,
)


@app.command(context_settings={"allow_extra_args": True, "allow_interspersed_args": False})
def main(
    ctx: typer.Context,
    output_dir: Optional[Path] = typer.Option(
        None, "--output-dir", "-o", help="Where to output the generated project"
    ),
    no_input: bool = typer.Option(
        False, "--no-input", help="Do not prompt for parameters, use defaults"
    ),
) -> None:
    """Generate a new Python package from the cookiecutter-pypackage template.

    You can pass extra key=value pairs to override template variables:
        uvx cookiecutter-pypackage full_name="Audrey M. Roy Greenfeld" github_username=audreyfeldroy
    """
    # Template is bundled inside the package
    template_dir = Path(__file__).parent / "template"

    # Parse extra context from additional arguments
    extra_context = {}
    for arg in ctx.args:
        if "=" not in arg:
            typer.echo(f"Error: extra argument '{arg}' must be in key=value format", err=True)
            raise typer.Exit(code=1)
        key, value = arg.split("=", 1)
        extra_context[key] = value

    # Run cookiecutter with the bundled template
    cookiecutter(
        str(template_dir),
        output_dir=str(output_dir) if output_dir else ".",
        no_input=no_input,
        extra_context=extra_context or None,
    )


if __name__ == "__main__":
    app()
