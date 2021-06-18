#!/usr/bin/env python

"""Tests for `{{ cookiecutter.project_slug }}` package."""

# from {{ cookiecutter.project_slug }} import {{ cookiecutter.project_slug }}
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}
import argparse
import os
import subprocess
from unittest.mock import call, patch
{%- endif %}

import pytest
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}

from {{cookiecutter.project_slug}}.cli import main, parse_argv, process_args{%- endif %}


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
{%- if cookiecutter.command_line_interface|lower == 'argparse' %}


@patch('builtins.print', autospec=print)
def test_process_args(print):
    ns = argparse.Namespace()
    setattr(ns, 'foo', '<fake>')
    out = process_args(ns)

    assert out == 0
    print.assert_has_calls([call("Arguments: Namespace(foo='<fake>')"),
                            call('Replace this message by putting '
                                 'your code into {{cookiecutter.project_slug}}.cli.process_args')])


# @pytest.mark.skip(reason="working on main help test first")
def test_parse_argv_run_simple():
    argv = ['{{ cookiecutter.project_slug }}', 'op1', '123']
    args = parse_argv(argv)
    assert vars(args) == {'operation': 'op1', 'arg1': 123}


@patch('{{ cookiecutter.project_slug }}.cli.parse_argv', autospec=parse_argv)
@patch('{{ cookiecutter.project_slug }}.cli.process_args', autospec=process_args)
def test_main(process_args, parse_argv):
    argv = object()
    args = parse_argv.return_value
    assert process_args.return_value == main(argv)
    process_args.assert_called_with(args)


def test_cli_op1_help():
    request_long_lines = {'COLUMNS': '999', 'LINES': '25'}
    env = {}
    env.update(os.environ)
    env.update(request_long_lines)
    expected_help = """usage: {{ cookiecutter.project_slug }} op1 [-h] arg1

Do some kind of operation

positional arguments:
  arg1        arg1 help

options:
  -h, --help  show this help message and exit
"""
    # older python versions show arguments like this:
    actual_help = subprocess.check_output(['{{ cookiecutter.project_slug }}', 'op1', '--help'],
                                          env=env).decode('utf-8')
    assert actual_help == expected_help


def test_cli_no_command():
    request_long_lines = {'COLUMNS': '999', 'LINES': '25'}
    env = {}
    env.update(os.environ)
    env.update(request_long_lines)
    expected_help = """usage: {{ cookiecutter.project_slug }} [-h] {op1} ...
{{ cookiecutter.project_slug }}: error: Please provide a command
"""
    # older python versions show arguments like this:
    result = subprocess.run(['{{ cookiecutter.project_slug }}'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=env)
    actual_help = result.stderr.decode('utf-8')
    assert actual_help == expected_help


def test_cli_help():
    request_long_lines = {'COLUMNS': '999', 'LINES': '25'}
    env = {}
    env.update(os.environ)
    env.update(request_long_lines)
    expected_help = """usage: {{ cookiecutter.project_slug }} [-h] {op1} ...

positional arguments:
  {op1}
    op1       Do some kind of operation

options:
  -h, --help  show this help message and exit
"""
    # older python versions show arguments like this:
    actual_help = subprocess.check_output(['{{ cookiecutter.project_slug }}', '--help'],
                                          env=env).decode('utf-8')
    assert actual_help == expected_help
{%- endif %}
