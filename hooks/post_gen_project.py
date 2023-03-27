#!/usr/bin/env python

import shutil
from pathlib import Path

PROJECT_DIRECTORY = Path.cwd()


def move_files():
    files = PROJECT_DIRECTORY.glob("*")
    parent = PROJECT_DIRECTORY.parent
    for file in files:
        shutil.move(str(file), str(parent.joinpath(file.name)))


def remove_file(filepath):
    PROJECT_DIRECTORY.joinpath(filepath).unlink()


if __name__ == "__main__":
    if "{{ cookiecutter.create_author_file }}" != "y":
        remove_file("AUTHORS.rst")
        remove_file("docs/authors.rst")

    if "no" in "{{ cookiecutter.command_line_interface|lower }}":
        cli_file = "/".join(
            ("src", "{{ cookiecutter.project_slug }}", "cli.py")
        )
        remove_file(cli_file)

    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE")

    move_files()
    PROJECT_DIRECTORY.rmdir()
