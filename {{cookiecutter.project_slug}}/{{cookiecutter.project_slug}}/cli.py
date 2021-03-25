"""Console script for {{cookiecutter.project_slug}}."""

{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
import argparse
{%- endif %}
import sys
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
from typing import List{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'click' %}
import click
{%- endif %}

{% if cookiecutter.command_line_interface|lower == 'click' %}
@click.command()
def main(args=None):
    """Console script for {{cookiecutter.project_slug}}."""
    click.echo("Replace this message by putting your code into "
               "{{cookiecutter.project_slug}}.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
def parse_argv(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    return parser.parse_args(argv[1:])


def process_args(args: argparse.Namespace) -> int:
    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "{{cookiecutter.project_slug}}.cli.process_args")
    return 0


def main(argv: List[str] = sys.argv) -> int:
    """Console script for {{cookiecutter.project_slug}}."""

    args = parse_argv(argv)

    return process_args(args)
{%- endif %}


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
