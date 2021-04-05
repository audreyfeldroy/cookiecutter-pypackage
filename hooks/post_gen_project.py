#!/usr/bin/env python

import os
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':
    if '{{ cookiecutter.create_author_file }}' != 'y':
        remove_file('AUTHORS.rst')
        remove_file('docs/authors.rst')

    if 'no' in '{{ cookiecutter.command_line_interface|lower }}':
        cli_file = os.path.join('{{ cookiecutter.project_slug }}', 'cli.py')
        remove_file(cli_file)

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')

    if os.environ.get('IN_COOKIECUTTER_PROJECT_UPGRADER', '0') == '1':
        os.environ['SKIP_GIT_CREATION'] = '1'
        os.environ['SKIP_GITHUB_AND_CIRCLECI_CREATION'] = '1'

    if os.environ.get('SKIP_FIX_SCRIPT', '0') != '1':
        subprocess.check_call('./fix.sh')

    if os.environ.get('SKIP_GIT_CREATION', '0') != '1':
        # Don't run these non-idempotent things when in
        # cookiecutter_project_upgrader, which will run this hook
        # multiple times over its lifetime.
        subprocess.check_call(['git', 'init'])
        subprocess.check_call(['git', 'add', '-A'])

    if (os.environ.get('SKIP_FIX_SCRIPT', '0') != '1' and
       os.environ.get('SKIP_GIT_CREATION', '0') != '1'):
        subprocess.check_call(['bundle', 'exec', 'overcommit', '--install'])
        subprocess.check_call(['bundle', 'exec', 'overcommit', '--sign'])
        subprocess.check_call(['bundle', 'exec', 'overcommit', '--sign', 'pre-commit'])
        subprocess.check_call(['git', 'commit', '-m',
                               'Initial commit from boilerplate'])

    if os.environ.get('SKIP_GITHUB_AND_CIRCLECI_CREATION', '0') != '1':
        if 'none' != '{{ cookiecutter.type_of_github_repo }}':
            if 'private' == '{{ cookiecutter.type_of_github_repo }}':
                visibility_flag = '--private'
            elif 'public' == '{{ cookiecutter.type_of_github_repo }}':
                visibility_flag = '--public'
            else:
                raise RuntimeError('Invalid argument to '
                                   'cookiecutter.type_of_github_repo: '
                                   '{{ cookiecutter.type_of_github_repo }}')
            description = "{{ cookiecutter.project_short_description.replace('\"', '\\\"') }}"
            subprocess.check_call(['gh', 'repo', 'create',
                                   visibility_flag,
                                   '-y',
                                   '--description',
                                   description,
                                   '{{ cookiecutter.github_username }}/'
                                   '{{ cookiecutter.project_slug }}'])
            subprocess.check_call(['circleci', 'follow'])
            subprocess.check_call(['git', 'push'])
            subprocess.check_call(['git', 'branch', '--set-upstream-to=origin/main', 'main'])
