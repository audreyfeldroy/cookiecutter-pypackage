#!/usr/bin/env python
import os

import shutil
from subprocess import call

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def boostrap_venv():
    print("-------> Bootstrapping virtual environment")
    call(["python3", "-m", "venv", "--clear", ".pyvenv"])
    call([".pyvenv/bin/python", "-m", "pip", "install", "-U", "pip", "setuptools"])
    call([".pyvenv/bin/python", "-m", "pip", "install", "-r", "requirements/local.txt"])


def git_init():
    print("-------> Initializing git repo")
    call(["git", "init"])
    call(["git", "add", "--all"])
    call(["git", "commit", "-am", "init"])
    call(["git", "flow", "init", "-d"])
    call(["git", "remote", "add", "origin", "{{ cookiecutter.repo_url }}.git"])


if __name__ == '__main__':
    if '{{ cookiecutter.use_pypi_deployment_with_travis }}' != 'y':
        remove_file('travis_pypi_setup.py')

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('src', '{{ cookiecutter.package_name }}', 'cli.py')
        remove_file(cli_file)

    if '{{ cookiecutter.include_sphinx_doc }}' != 'y':
        shutil.rmtree(os.path.join(PROJECT_DIRECTORY, 'docs'))

    if '{{ cookiecutter.git_init }}'.lower() == 'y':
        git_init()

    if '{{ cookiecutter.create_virtual_environment }}'.lower() == 'y':
        boostrap_venv()

    if '{{ cookiecutter.run_tests_on_init }}' == 'y':
        print("-------> Running tests")
        call(["tox"])
