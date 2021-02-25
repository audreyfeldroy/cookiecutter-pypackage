#!/usr/bin/env python

"""Tests for `{{ cookiecutter.project_slug }}` package."""

import pytest
{%- if cookiecutter.command_line_interface|lower == 'click' %}
from click.testing import CliRunner
{%- endif %}

# from {{ cookiecutter.project_slug }} import {{ cookiecutter.project_slug }}
{%- if cookiecutter.command_line_interface|lower == 'click' %}
from {{ cookiecutter.project_slug }} import cli
{%- endif %}



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
{%- if cookiecutter.command_line_interface|lower == 'click' %}


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert '{{ cookiecutter.project_slug }}.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
{%- else %}


def test_process_args():
    args = '<fake>'
    with patch('builtins.print') as mock_print:
        out = process_args()

        assert out == 0
        mock_print.assert_called_with('Arguments: <fake>')
        mock_print.assert_called_with('Replace this message by putting '
                                      'your code into {{cookiecutter.project_slug}}.cli.process_args')


def test_parse_argv_run_simple():
    argv = ['{{ cookiecutter.project_slug }}', 'whatever']
    args = parse_argv(argv)
    assert vars(args) == {'_': ['whatever']}


def test_cli_help():
    expected_help = """usage: {{ cookiecutter.project_slug }} [-h] [_ ...]

positional arguments:
  _

optional arguments:
  -h, --help  show this help message and exit
"""
    # older python versions show arguments like this:
    alt_expected_help = expected_help.replace('[_ ...]', '[_ [_ ...]]')
    actual_help = subprocess.check_output(['{{ cookiecutter.project_slug }}', '--help']).decode('utf-8')
    assert actual_help in [expected_help, alt_expected_help]
{%- endif %}
