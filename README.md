# Cookiecutter PyPackage

Barebones cookiecutter for python packages

## Installation

1. Create a virtual environment & activate

    `python -m venv .venv && source .venv/bin/activate`

2. Install this package

    `pip install . -r requirements.txt`

    Or for dev mode:

    `pip install -e ".[dev]" -r requirements_dev.txt`

## Usage

Create a package with

`cookiecutter .`

## Features

Todo...

## Testing

Make sure dev dependencies are installed

`pip install -r requirements_dev.txt`

Test with:

`pytest`
