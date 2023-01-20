"""Main module."""
import sys

{%- if cookiecutter.command_line_interface|lower == 'typer' %}
from .cli import app

app(prog_name="{{cookiecutter.project_slug}}")
{%- else %}
def main():
    pass


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
{%- endif %}
