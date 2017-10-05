#!/usr/bin/env python
import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':
    if '{{ cookiecutter.use_pypi_deployment_with_travis }}' != 'y':
        remove_file('travis_pypi_setup.py')

    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('src','{{ cookiecutter.package_name }}', 'cli.py')
        remove_file(cli_file)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')

def boostrap_venv():
    print("### Bootstrapping virtual environment")
    from subprocess import call
    call(["python3", "-m", "venv", "--clear", ".pve"])
    call([".pve/bin/python", "-m", "pip", "install", "-U", "pip", "setuptools"])
    call([".pve/bin/python", "-m", "pip", "install", "-r", "requirements/local.txt"])


if '{{ cookiecutter.create_virtual_environment }}'.lower() == 'y':
    boostrap_venv()


def git_init():
    print("### Initializing git repo")
    from subprocess import call
    call(["git", "init"])
    call(["git", "add", "--all"])
    call(["git", "commit", "-am", "init"])
    call(["git", "flow", "init", "-d"])
    call(["git", "remote", "add", "origin", "git://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git"])


if '{{ cookiecutter.git_init }}'.lower() == 'y':
    git_init()
