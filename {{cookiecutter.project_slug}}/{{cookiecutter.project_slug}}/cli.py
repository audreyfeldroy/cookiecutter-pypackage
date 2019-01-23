# -*- coding: utf-8 -*-
"""Console script for {{cookiecutter.project_slug}}."""
import sys
import click
import logging
from utils import countToLogLevel


@click.command()
@click.option(
    '--dry-run',
    '-n',
    flag_value='dry_run',
    default=False,
    help="Perform a trial run with no changes made")
@click.option('--verbose', '-v', count=True, help="Increase verbosity")
@click.option('--version', '-V', help="Print version")
def main(is_dry_run, verbose):
    """Console script for {{cookiecutter.project_slug}}."""
    logger = logging.getLogger()
    logger.setLevel(countToLogLevel(verbose))
    logger.error("This is an error message")
    logger.warning("This is a warning")
    logger.info("This is an info message")
    logger.info("This is a debug message")
    click.echo(
        "Replace this message by putting your code into {{cookiecutter.project_slug}}.cli.main"
    )
    click.echo("See click documentation at http://click.pocoo.org/")

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
