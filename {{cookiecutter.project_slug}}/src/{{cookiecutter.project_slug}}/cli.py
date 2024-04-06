"""Console script for {{cookiecutter.project_slug}}."""
import {{cookiecutter.project_slug}}
{%- if cookiecutter.command_line_interface|lower == 'typer' %}
import typer

app = typer.Typer()


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
import argparse
import sys

def main():
    """Console script for {{cookiecutter.project_slug}}."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "{{cookiecutter.project_slug}}.cli.main")
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
{%- endif %}
