"""Console script for {{cookiecutter.import_name}}."""

import typer
from rich.console import Console

from {{cookiecutter.import_name}} import utils

app = typer.Typer()
console = Console()


@app.command()
def main() -> None:
    """Console script for {{cookiecutter.import_name}}."""
    console.print("Replace this message by putting your code into {{cookiecutter.import_name}}.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()
