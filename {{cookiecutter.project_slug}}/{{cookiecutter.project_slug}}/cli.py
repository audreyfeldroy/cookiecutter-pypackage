import click

@click.command()
def main(args=None):
    """Console script for {{cookiecutter.project_slug}}"""
    click.echo("Add a console script for {{cookiecutter.project_slug}}")
    click.echo("See click documentation at http://http://click.pocoo.org/")

if __name__ == "__main__":
    main()
