#!/usr/bin/env python
import pathlib


if __name__ == '__main__':

    if '{{ cookiecutter.create_author_file }}' != 'y':
        pathlib.Path('AUTHORS.rst').unlink()
        pathlib.Path('docs', 'authors.rst').unlink()

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        pathlib.Path('src', '{{ cookiecutter.project_slug }}', 'cli.py').unlink()
        pathlib.Path('src', '{{ cookiecutter.project_slug }}', '__main__.py').unlink()

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        pathlib.Path('LICENSE').unlink()
