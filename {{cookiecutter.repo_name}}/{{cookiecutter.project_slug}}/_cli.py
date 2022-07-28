"""
{{ cookiecutter.project_name }}: Command Line Interface
"""

import click

from {{cookiecutter.project_slug}} import __application__, __version__


@click.group()
@click.version_option(version=__version__, prog_name=__application__)
@click.pass_context
def command_line_interface(ctx: click.core.Context) -> None:
    r"""
    Welcome to {{ cookiecutter.project_name }}

    \b
    Homepage: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}
    """
    ctx.ensure_object(dict)


if __name__ == "__main__":
    command_line_interface()
