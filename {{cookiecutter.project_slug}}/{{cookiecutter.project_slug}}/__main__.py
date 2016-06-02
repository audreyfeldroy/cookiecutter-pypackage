import click

@click.command()
def main(args=None):
    """The main routine."""
    click.echo("Add a console script for {{cookiecutter.project_slug}}")
