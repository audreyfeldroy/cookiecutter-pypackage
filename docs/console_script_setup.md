# Console Script Setup

Your package will include a console script using Typer.

## How It Works

Cookiecutter will add a file `cli.py` in the project_slug subdirectory. An entry point is configured in `pyproject.toml` under `[project.scripts]` that points to the main function in `cli.py`.

## Usage

To use the console script in development:

```bash
uv sync
```

This installs the package in development mode, making the console script available.

The script will be generated with output for no arguments and `--help`.

- `--help`: show help menu and exit
