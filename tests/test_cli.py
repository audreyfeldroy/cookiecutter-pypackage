"""Tests for extra_context argument forwarding.

These tests verify that extra_context values are properly forwarded
and applied when generating projects. The CLI feature allows passing
these as key=value arguments.
"""


def test_extra_context_single_value(cookies):
    """Test that a single extra_context value overrides defaults."""
    result = cookies.bake(extra_context={"pypi_package_name": "test-package"})
    assert result.exit_code == 0
    assert result.project_path.name == "test-package"
    assert result.project_path.is_dir()


def test_extra_context_multiple_values(cookies):
    """Test that multiple extra_context values work together."""
    result = cookies.bake(
        extra_context={
            "pypi_package_name": "my-package",
            "full_name": "Audrey M. Roy Greenfeld",
            "email": "audreyfeldroy@example.com",
        },
    )
    assert result.exit_code == 0
    assert result.project_path.name == "my-package"

    # Verify values in pyproject.toml
    content = (result.project_path / "pyproject.toml").read_text()
    assert 'name = "my-package"' in content
    assert "Audrey M. Roy Greenfeld" in content
    assert "audreyfeldroy@example.com" in content


def test_extra_context_with_equals_in_value(cookies):
    """Test that values containing = are handled correctly."""
    result = cookies.bake(
        extra_context={
            "pypi_package_name": "test-pkg",
            "project_short_description": "A package with = in description",
        },
    )
    assert result.exit_code == 0
    content = (result.project_path / "pyproject.toml").read_text()
    assert "A package with = in description" in content


def test_extra_context_with_empty_value(cookies):
    """Test that empty string values are accepted."""
    result = cookies.bake(
        extra_context={
            "pypi_package_name": "empty-test",
            "project_short_description": "",
        },
    )
    assert result.exit_code == 0
    assert result.project_path.name == "empty-test"


def test_extra_context_with_quotes_in_value(cookies):
    """Test that quoted values work correctly in generated TOML."""
    result = cookies.bake(
        extra_context={
            "pypi_package_name": "quoted-test",
            "full_name": 'Test "Nickname" User',
        },
    )
    assert result.exit_code == 0
    content = (result.project_path / "pyproject.toml").read_text()
    # The quotes should be escaped in TOML
    assert 'Test \\"Nickname\\" User' in content


def test_extra_context_overrides_defaults(cookies):
    """Test that extra_context values override cookiecutter.json defaults."""
    result = cookies.bake(
        extra_context={
            "pypi_package_name": "override-test",
            "project_name": "Override Test Project",
            "first_version": "1.0.0",
        },
    )
    assert result.exit_code == 0

    content = (result.project_path / "pyproject.toml").read_text()
    assert 'version = "1.0.0"' in content

    readme_content = (result.project_path / "README.md").read_text()
    assert "Override Test Project" in readme_content


def test_extra_context_preserves_special_chars(cookies):
    """Test that special characters in values are preserved."""
    result = cookies.bake(
        extra_context={
            "pypi_package_name": "special-test",
            "project_short_description": "Testing: colons, semicolons; and more!",
        },
    )
    assert result.exit_code == 0
    content = (result.project_path / "pyproject.toml").read_text()
    assert "Testing: colons, semicolons; and more!" in content
