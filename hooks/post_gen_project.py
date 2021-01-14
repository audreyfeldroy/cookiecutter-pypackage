#!/usr/bin/env python
import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_folder(folderpath):
    for file in os.listdir(folderpath):
        if os.path.isfile(file):
            os.remove(os.path.join(PROJECT_DIRECTORY, folderpath, file))
            continue
        try:
            os.rmdir(os.path.join(PROJECT_DIRECTORY, folderpath, file))
        except OSError:
            pass
    os.rmdir(os.path.join(PROJECT_DIRECTORY, folderpath))


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')

    if '{{ cookiecutter.make_docs }}' != 'y':
        remove_file('requirements_docs.txt')
        remove_folder('docs')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'cli.py')
        remove_file(cli_file)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')
