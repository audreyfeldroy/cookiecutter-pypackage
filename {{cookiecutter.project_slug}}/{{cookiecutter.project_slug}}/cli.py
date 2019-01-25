# -*- coding: utf-8 -*-
"""Console script for {{cookiecutter.project_slug}}."""
import sys
import click
import logging

from {{ cookiecutter.project_slug }} import utils

__version__ = '{{ cookiecutter.version }}'


@click.command()
@click.option(
    '--dry-run',
    '-n',
    flag_value='dry_run',
    default=False,
    help="Perform a trial run with no changes made")
@click.option('--verbose', '-v', count=True, help="Increase verbosity (specify multiple times for more)")
@click.option('--version', '-V', is_flag=True, help="Print version")
def main(*args, **kwargs):
    """Console script for test_cli_project."""

    logging.basicConfig(level=count_to_log_level(kwargs['verbose']))

    logging.warning("This is a warning.")
    logging.info("This is an info message.")
    logging.debug("This is a debug message.")

    if kwargs['version']:
        click.echo(__version__)
        return 0

    if kwargs['dry_run']:
        click.echo("Is dry run")
        return 0

    click.echo(
        "Replace this message by putting your code into test_cli_project.cli.main"
    )
    click.echo("See click documentation at http://click.pocoo.org/")

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
