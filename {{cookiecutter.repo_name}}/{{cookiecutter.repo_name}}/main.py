#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
{{ cookiecutter.repo_name }}.main
-----------------------------------

Main entry point for the `{{ cookiecutter.repo_name }}` command.

The code in this module is also a good example of how to use {{ cookiecutter.project_name }}
as a library rather than a script.
"""

import argparse


def get_{{ cookiecutter.repo_name }}_args():
    """
    Get the command line input/output arguments passed into {{ cookiecutter.project_name }}.
    """

    parser = argparse.ArgumentParser(
        description='{{ cookiecutter.project_short_description }}'
    )

    # TODO: parser.add_argument(...)

    args = parser.parse_args()
    return args


def main():
    args = get_{{ cookiecutter.repo_name }}_args()

    # TODO: call function that does the main work here


if __name__ == '__main__':
    main()
