"""
Test cases for the __main__ module.
"""

import pytest
from click.testing import CliRunner

from {{cookiecutter.project_slug}}._cli import command_line_interface


@pytest.fixture
def runner() -> CliRunner:
    """
    Fixture for invoking command-line interfaces.
    """
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """
    It exits with a status code of zero.
    """
    result = runner.invoke(command_line_interface)
    assert result.exit_code == 0
