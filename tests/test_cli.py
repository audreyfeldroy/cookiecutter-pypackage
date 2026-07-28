"""Tests for the cookiecutter-pypackage CLI.

These tests cover locating the bundled template, listing variables, and
forwarding extra_context values when generating projects.
"""

import json

from typer.testing import CliRunner

from cookiecutter_pypackage import cli


def test_find_template_dir_in_source_checkout(monkeypatch, tmp_path):
    """Use the repository root when the CLI is running from src/."""
    module_path = tmp_path / "src" / "cookiecutter_pypackage" / "cli.py"
    module_path.parent.mkdir(parents=True)
    (tmp_path / "cookiecutter.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(cli, "__file__", str(module_path))

    assert cli._find_template_dir() == tmp_path


def test_find_template_dir_in_installed_package(monkeypatch, tmp_path):
    """Use package data when the CLI is installed from a wheel."""
    package_dir = tmp_path / "site-packages" / "cookiecutter_pypackage"
    template_dir = package_dir / "template"
    template_dir.mkdir(parents=True)
    (template_dir / "cookiecutter.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(cli, "__file__", str(package_dir / "cli.py"))

    assert cli._find_template_dir() == template_dir


def test_list_variables(monkeypatch, tmp_path):
    """List public variables and exit without generating a project."""
    variables = {
        "full_name": "Example User",
        "_copy_without_render": ["*.html"],
        "package_name": "{{ cookiecutter.project_name }}",
    }
    (tmp_path / "cookiecutter.json").write_text(json.dumps(variables), encoding="utf-8")
    monkeypatch.setattr(cli, "_find_template_dir", lambda: tmp_path)

    def fail_cookiecutter(*args, **kwargs):
        raise AssertionError("cookiecutter should not run when listing variables")

    monkeypatch.setattr(cli, "cookiecutter", fail_cookiecutter)
    result = CliRunner().invoke(cli.app, ["--list-variables"])

    assert result.exit_code == 0
    assert result.output.splitlines() == [
        "Available template variables:",
        "  full_name (default: 'Example User')",
        "  package_name (default: '{{ cookiecutter.project_name }}')",
    ]


def test_extra_context_single_value(cookies):
    """Test that a single extra_context value overrides defaults."""
    result = cookies.bake(extra_context={"package_name": "test-package"})
    assert result.exit_code == 0
    assert result.project_path.name == "test-package"
    assert result.project_path.is_dir()


def test_extra_context_multiple_values(cookies):
    """Test that multiple extra_context values work together."""
    result = cookies.bake(
        extra_context={
            "package_name": "my-package",
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
            "package_name": "test-pkg",
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
            "package_name": "empty-test",
            "project_short_description": "",
        },
    )
    assert result.exit_code == 0
    assert result.project_path.name == "empty-test"


def test_extra_context_with_quotes_in_value(cookies):
    """Test that quoted values work correctly in generated TOML."""
    result = cookies.bake(
        extra_context={
            "package_name": "quoted-test",
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
            "package_name": "override-test",
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
            "package_name": "special-test",
            "project_short_description": "Testing: colons, semicolons; and more!",
        },
    )
    assert result.exit_code == 0
    content = (result.project_path / "pyproject.toml").read_text()
    assert "Testing: colons, semicolons; and more!" in content
