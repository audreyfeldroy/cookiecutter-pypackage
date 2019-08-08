#!/usr/bin/env python
import os
from pathlib import Path

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def make_symlink(filename, directory):
    os.symlink(
        str(Path('..') / filename),  # python < 3.6
        filename.lower(),
        dir_fd=directory
    )


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.md')

    if '{{ cookiecutter.use_pytest }}' == 'y':
        remove_file('tests/__init__.py')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('src', '{{ cookiecutter.project_slug }}', 'cli.py')
        remove_file(cli_file)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')

    markdown_files = Path.cwd().glob("*.md")
    docs = os.open('docs', os.O_RDONLY)
    for file in markdown_files:
        symlink = Path('docs') / file.name.lower()
        if symlink.exists():
            symlink.unlink()  # remove

        make_symlink(file.name, docs)

    os.close(docs)

    if '{{ cookiecutter.initialize_git_repo }}' == 'y':

