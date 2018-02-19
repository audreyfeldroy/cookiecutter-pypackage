# -*- coding: utf-8 -*-

"""Console script for {{cookiecutter.module_name}}."""

import click


@click.command()
def main(args=None):
    """Console script for {{cookiecutter.module_name}}."""
    click.echo("Replace this message by putting your code into "
               "{{cookiecutter.module_name}}.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


if __name__ == "__main__":
    main()
