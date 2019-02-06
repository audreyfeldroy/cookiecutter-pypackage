#!/usr/bin/env python
import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'cli.py')
        utils_file = os.path.join('{{ cookiecutter.project_slug }}', 'utils.py')
        test_cli_file = os.path.join('tests', 'test_cli.py')
        test_utils_file = os.path.join('tests', 'test_utils.py')
        remove_file(cli_file)
        remove_file(utils_file)
        remove_file(test_cli_file)
        remove_file(test_utils_file)
