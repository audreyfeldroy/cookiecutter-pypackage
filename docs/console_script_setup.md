# Console Script Setup

Your package will include a console script using Typer.

## How It Works

Cookiecutter will add a file `cli.py` in the project_slug subdirectory. An entry point is added to `setup.py` that points to the main function in `cli.py`.

## Usage

To use the console script in development:

```bash
pip install -e projectdir
```

'projectdir' should be the top level project directory with the `setup.py` file.

The script will be generated with output for no arguments and `--help`.

- `--help`: show help menu and exit
