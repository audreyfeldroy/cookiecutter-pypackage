# -*- coding: utf-8 -*-

"""Console script for {{cookiecutter.repo_name}}."""
import sys
{% if 'Click' == cookiecutter.command_line_interface -%}
import click


@click.command()
def main(args=None):
    """Console script for {{cookiecutter.repo_name}}."""
    click.echo("Replace this message by putting your code into "
               "{{cookiecutter.project_slug}}.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0

{% elif 'argparse' == cookiecutter.command_line_interface -%}
import argparse
from {{cookiecutter.project_slug}} import __version__


def get_parser():
    """Defines options for {{cookiecutter.repo_name}}."""
    parser = argparse.ArgumentParser(
        prog="{{cookiecutter.repo_name}}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="be more verbose"
    )
    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    # Add more arguments as needed here

    return parser


def main(args=None):
    """Console script for {{cookiecutter.repo_name}}."""
    parser = get_parser()
    args = parser.parse_args(args)

    # Process args here
    print(
        "Replace this message by putting your code into "
        "{{cookiecutter.project_slug}}.cli.main"
    )
    print(
        "See argparse tutorial at https://docs.python.org/3/howto/argparse.html"
    )

    return 0


{%- endif %}

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
