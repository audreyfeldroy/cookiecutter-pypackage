#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `{{ cookiecutter.project_slug }}` package."""

{% if cookiecutter.use_pytest == "y" -%}
import pytest
{% else %}
import unittest
{%- endif %}
{%- if cookiecutter.command_line_interface|lower == "click" %}
from click.testing import CliRunner
{%- endif %}

from {{ cookiecutter.project_slug }} import {{ cookiecutter.project_slug }}
{%- if cookiecutter.command_line_interface|lower == "click" %}
from {{ cookiecutter.project_slug }} import cli
{%- endif %}

{%- if cookiecutter.use_pytest == "y" %}


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get("https://github.com/audreyr/cookiecutter-pypackage")


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert "GitHub" in BeautifulSoup(response.content).title.string
{%- if cookiecutter.command_line_interface|lower == "click" %}


def test_cli_root():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert "Console script for {{ cookiecutter.project_slug }}" in result.output
    help_result = runner.invoke(cli.cli, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


def test_cli_command():
    """Test a CLI command."""
    runner = CliRunner()
    result = runner.invoke(cli.command)
    assert result.exit_code == 0
    print(result.output)
    assert "A Command" in result.output
    help_result = runner.invoke(cli.command, ["--help"])
    assert help_result.exit_code == 0
    assert "--option INTEGER  An option" in help_result.output

{%- endif %}
{%- else %}


class Test{{ cookiecutter.project_slug|title }}(unittest.TestCase):
    """Tests for `{{ cookiecutter.project_slug }}` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
{%- if cookiecutter.command_line_interface|lower == "click" %}

    def test_cli_roott(self):
        """Test the root CLI group."""
        runner = CliRunner()
        result = runner.invoke(cli.cli)
        assert result.exit_code == 0
        print(result.output)
        assert "Console script for {{ cookiecutter.project_slug }}" in result.output
        help_result = runner.invoke(cli.cli, ["--help"])
        assert help_result.exit_code == 0
        assert "--help  Show this message and exit." in help_result.output

    def test_cli_command(self):
        """Test a CLI command."""
        runner = CliRunner()
        result = runner.invoke(cli.command)
        assert result.exit_code == 0
        print(result.output)
        assert "A Command" in result.output
        help_result = runner.invoke(cli.command, ["--help"])
        assert help_result.exit_code == 0
        assert "--option INTEGER  An option" in help_result.output

{%- endif %}
{%- endif %}
