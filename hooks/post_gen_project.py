#!/usr/bin/env python
import os
import io

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'cli.py')
        remove_file(cli_file)

    # Patch up .circleci/config.yaml
    with io.open(".circleci/config.yaml", "r", encoding="utf-8") as f:
        circleci = f.read()

    circleci.replace("<{<", "{{")
    circleci.replace(">}>", "}}")

    with io.open(".circleci/config.yaml", "w", encoding="utf-8") as f:
        f.write(circleci)
