"""Console script for {{cookiecutter.project_slug}}."""
import sys
import click


@click.command()
def main():
    """Console script for {{cookiecutter.project_slug}}.
    "See click documentation at https://click.palletsprojects.com/"
    """
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
