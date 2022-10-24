# Cookiecutter PyPackage

Barebones cookiecutter for python packages

## Installation

To create a new package:

1. Create a virtual environment & activate

    `python -m venv .venv && source .venv/bin/activate`

2. Install the cookiecutter package

    `pip install . -r requirements.txt`

    Or for dev mode:

    `pip install -e ".[dev]" -r requirements_dev.txt`

3. Create the package

    `cookiecutter .`

## Features

Todo...

## Testing

Install dev dependencies into virtual environment

`pip install -r requirements_dev.txt`

Test with:

`pytest`
