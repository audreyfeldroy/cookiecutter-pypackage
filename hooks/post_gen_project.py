#!/usr/bin/env python
from pathlib import Path

PROJECT_DIRECTORY = Path().cwd().absolute()


def remove_file(filepath):
    Path(PROJECT_DIRECTORY).joinpath(filepath).unlink()


def remove_folder(folderpath):
    for file in Path(PROJECT_DIRECTORY).joinpath(folderpath).iterdir():
        if not file.is_dir():
            file.unlink()
            continue
        file.rmdir()
    Path(PROJECT_DIRECTORY).joinpath(folderpath).rmdir()


if __name__ == "__main__":

    if "{{ cookiecutter.create_author_file }}" != "y":
        remove_file("AUTHORS.rst")
        remove_file("docs/authors.rst")

    if "{{ cookiecutter.make_docs }}" != "y":
        remove_file("requirements_docs.txt")
        remove_folder("docs")

    if "no" in "{{ cookiecutter.command_line_interface|lower }}":
        cli_file = Path("{{ cookiecutter.project_slug }}").joinpath("cli.py")
        remove_file(cli_file)

    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE")
