#!/usr/bin/env python
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(path):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, path))


if __name__ == '__main__':
    if '{{ cookiecutter.use_pypi_deployment_with_travis }}' != 'y':
        remove_file('travis_pypi_setup.py')

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')

    if '{{ cookiecutter.use_pytest }}' == 'y':
        remove_file('tests/__init__.py')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'cli.py')
        remove_file(cli_file)

    if 'n' in '{{ cookiecutter.use_yapf|lower }}':
        remove_file('.style.yapf')

    if 'n' in '{{ cookiecutter.use_vscode|lower }}':
        remove_dir('.vscode')

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')
        remove_file('CONTRIBUTING.rst')
        remove_file('docs/contributing.rst')
        remove_dir('.github')
