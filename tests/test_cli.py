"""Tests for extra_context argument forwarding.

These tests verify that extra_context values are properly forwarded
and applied when generating projects. The CLI feature allows passing
these as key=value arguments.
"""
from contextlib import contextmanager

from cookiecutter.utils import rmtree


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def test_extra_context_single_value(cookies):
    """Test that a single extra_context value overrides defaults."""
    with bake_in_temp_dir(
        cookies, extra_context={"pypi_package_name": "test-package"}
    ) as result:
        assert result.exit_code == 0
        assert result.project.basename == "test-package"
        assert result.project.isdir()


def test_extra_context_multiple_values(cookies):
    """Test that multiple extra_context values work together."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "pypi_package_name": "my-package",
            "full_name": "Audrey M. Roy Greenfeld",
            "email": "audreyfeldroy@example.com",
        },
    ) as result:
        assert result.exit_code == 0
        assert result.project.basename == "my-package"

        # Verify values in pyproject.toml
        pyproject_path = result.project.join("pyproject.toml")
        content = pyproject_path.read()
        assert 'name = "my-package"' in content
        assert "Audrey M. Roy Greenfeld" in content
        assert "audreyfeldroy@example.com" in content


def test_extra_context_with_equals_in_value(cookies):
    """Test that values containing = are handled correctly."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "pypi_package_name": "test-pkg",
            "project_short_description": "A package with = in description",
        },
    ) as result:
        assert result.exit_code == 0
        pyproject_path = result.project.join("pyproject.toml")
        content = pyproject_path.read()
        assert "A package with = in description" in content


def test_extra_context_with_empty_value(cookies):
    """Test that empty string values are accepted."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "pypi_package_name": "empty-test",
            "project_short_description": "",
        },
    ) as result:
        assert result.exit_code == 0
        assert result.project.basename == "empty-test"


def test_extra_context_with_quotes_in_value(cookies):
    """Test that quoted values work correctly in generated TOML."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "pypi_package_name": "quoted-test",
            "full_name": 'Test "Nickname" User',
        },
    ) as result:
        assert result.exit_code == 0
        pyproject_path = result.project.join("pyproject.toml")
        content = pyproject_path.read()
        # The quotes should be escaped in TOML
        assert 'Test \\"Nickname\\" User' in content


def test_extra_context_overrides_defaults(cookies):
    """Test that extra_context values override cookiecutter.json defaults."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "pypi_package_name": "override-test",
            "project_name": "Override Test Project",
            "first_version": "1.0.0",
        },
    ) as result:
        assert result.exit_code == 0

        pyproject_path = result.project.join("pyproject.toml")
        content = pyproject_path.read()
        assert 'version = "1.0.0"' in content

        readme_path = result.project.join("README.md")
        readme_content = readme_path.read()
        assert "Override Test Project" in readme_content


def test_extra_context_preserves_special_chars(cookies):
    """Test that special characters in values are preserved."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "pypi_package_name": "special-test",
            "project_short_description": "Testing: colons, semicolons; and more!",
        },
    ) as result:
        assert result.exit_code == 0
        pyproject_path = result.project.join("pyproject.toml")
        content = pyproject_path.read()
        assert "Testing: colons, semicolons; and more!" in content
