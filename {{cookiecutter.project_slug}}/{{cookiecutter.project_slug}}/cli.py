"""Console script for {{cookiecutter.project_slug}}."""

{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
import argparse
{%- endif %}
import sys
{%- if cookiecutter.command_line_interface|lower == 'click' %}

import click
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'typer' %}

import typer
{%- endif %}

{% if cookiecutter.command_line_interface|lower == 'click' %}
@click.command()
def main(args=None):
    """Console script for {{cookiecutter.project_slug}}."""
    click.echo("Replace this message by putting your code into {{cookiecutter.project_slug}}.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0
{%- endif %}
{% if cookiecutter.command_line_interface|lower == 'typer' %}

app = typer.Typer()

@app.command()
@click.command()
def main(args=None):
    """Console script for {{cookiecutter.project_slug}}."""
    typer.echo("Replace this message by putting your code into {{cookiecutter.project_slug}}.cli.main")
    typer.echo("See typer documentation at https://typer.tiangolo.com/")
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
def main():
    """Console script for {{cookiecutter.project_slug}}."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "{{cookiecutter.project_slug}}.cli.main")
    return 0
{%- endif %}


if __name__ == "__main__":
    {% if cookiecutter.command_line_interface|lower == 'typer' %}
    sys.exit(app())
    {%- else %}
    sys.exit(main())  # pragma: no cover
    {%- endif %}
