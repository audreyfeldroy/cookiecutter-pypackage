"""CLI for cookiecutter-pypackage.

Usage:
    uvx cookiecutter-pypackage
    uvx cookiecutter-pypackage --no-input
    uvx cookiecutter-pypackage -o /path/to/output
"""

from pathlib import Path
from typing import Optional

import typer
from cookiecutter.main import cookiecutter

app = typer.Typer(
    help="Generate a Python package from the cookiecutter-pypackage template.",
    add_completion=False,
)


@app.command()
def main(
    output_dir: Optional[Path] = typer.Option(
        None, "--output-dir", "-o", help="Where to output the generated project"
    ),
    no_input: bool = typer.Option(
        False, "--no-input", help="Do not prompt for parameters, use defaults"
    ),
) -> None:
    """Generate a new Python package from the cookiecutter-pypackage template."""
    # Template is bundled inside the package
    template_dir = Path(__file__).parent / "template"

    # Run cookiecutter with the bundled template
    cookiecutter(
        str(template_dir),
        output_dir=str(output_dir) if output_dir else ".",
        no_input=no_input,
    )


if __name__ == "__main__":
    app()
