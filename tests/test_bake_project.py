import datetime
import shlex
import subprocess
import sys
from pathlib import Path

import pytest


def run_inside_dir(command, dirpath):
    """Run a command from inside a given directory, raising on non-zero exit."""
    return subprocess.check_call(shlex.split(command), cwd=dirpath)


def check_output_inside_dir(command, dirpath):
    """Run a command from inside a given directory, returning the command output."""
    return subprocess.check_output(shlex.split(command), cwd=dirpath)


def test_year_compute_in_license_file(cookies):
    result = cookies.bake()
    assert result.exit_code == 0
    license_file = result.project_path / "LICENSE"
    now = datetime.datetime.now()
    assert str(now.year) in license_file.read_text()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    assert result.exception is None
    assert result.project_path.is_dir()

    project_path = result.project_path
    project_slug = project_path.name
    project_dir = project_path / project_slug
    return str(project_path), project_slug, str(project_dir)


def test_bake_with_defaults(cookies):
    result = cookies.bake()
    assert result.project_path.is_dir()
    assert result.exit_code == 0
    assert result.exception is None
    found_toplevel_files = [f.name for f in result.project_path.iterdir()]
    assert "src" in found_toplevel_files
    assert "tests" in found_toplevel_files


def test_bake_and_run_tests(cookies):
    result = cookies.bake()
    assert result.project_path.is_dir()
    run_inside_dir("uv run pytest", str(result.project_path))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break pyproject.toml"""
    result = cookies.bake(extra_context={"full_name": 'name "quote" name'})
    assert result.project_path.is_dir()
    assert result.exit_code == 0
    run_inside_dir("uv run pytest", str(result.project_path))


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break pyproject.toml"""
    result = cookies.bake(extra_context={"full_name": "O'connor"})
    assert result.project_path.is_dir()
    run_inside_dir("uv run pytest", str(result.project_path))


def test_bake_with_quotes_in_description(cookies):
    """Ensure that double quotes in project_short_description produce valid TOML."""
    result = cookies.bake(
        extra_context={"project_short_description": 'A "quoted" description'}
    )
    assert result.project_path.is_dir()
    assert result.exit_code == 0
    content = (result.project_path / "pyproject.toml").read_text()
    assert 'description = "A \\"quoted\\" description"' in content


@pytest.mark.skipif(sys.platform == "win32", reason="justfile not supported on Windows")
def test_just_list(cookies):
    result = cookies.bake()
    output = check_output_inside_dir("just list", str(result.project_path))
    assert b"Show available commands" in output


def test_py_typed_marker_exists(cookies):
    """Verify generated package includes a py.typed marker file (PEP 561)."""
    result = cookies.bake()
    assert result.exit_code == 0
    project_path, project_slug, project_dir = project_info(result)
    # src/ uses project_slug (underscores), not pypi_package_name (hyphens)
    slug = project_slug.replace("-", "_")
    py_typed = Path(project_path) / "src" / slug / "py.typed"
    assert py_typed.is_file()


def test_typing_classifier_in_pyproject(cookies):
    """Verify generated pyproject.toml includes the Typing :: Typed classifier."""
    result = cookies.bake()
    assert result.exit_code == 0
    content = (result.project_path / "pyproject.toml").read_text()
    assert '"Typing :: Typed"' in content
