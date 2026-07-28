import datetime
import shlex
import subprocess
import sys
import tomllib

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


def test_bake_and_run_ruff(cookies):
    """Baked project passes ruff linting and formatting out of the box."""
    result = cookies.bake()
    assert result.project_path.is_dir()
    run_inside_dir("uv run ruff check .", str(result.project_path))
    run_inside_dir("uv run ruff format --check .", str(result.project_path))


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


@pytest.mark.parametrize(
    "description",
    [
        'A "quoted" description',
        "A multiline\ndescription",
        "A path ending in a backslash \\",
    ],
)
def test_bake_preserves_description_in_valid_toml(cookies, description):
    """Descriptions with TOML-sensitive characters remain valid and unchanged."""
    result = cookies.bake(extra_context={"project_short_description": description})
    assert result.project_path.is_dir()
    assert result.exit_code == 0
    with (result.project_path / "pyproject.toml").open("rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)
    assert pyproject["project"]["description"] == description


@pytest.mark.skipif(sys.platform == "win32", reason="justfile not supported on Windows")
def test_just_list(cookies):
    result = cookies.bake()
    output = check_output_inside_dir("just list", str(result.project_path))
    assert b"Show available commands" in output


def test_py_typed_marker_exists(cookies):
    """Verify generated package includes a py.typed marker file (PEP 561)."""
    result = cookies.bake()
    assert result.exit_code == 0
    import_name = result.project_path.name.lower().replace("-", "_")
    assert (result.project_path / "src" / import_name / "py.typed").is_file()


def test_typing_classifier_in_pyproject(cookies):
    """Verify generated pyproject.toml includes the Typing :: Typed classifier."""
    result = cookies.bake()
    assert result.exit_code == 0
    content = (result.project_path / "pyproject.toml").read_text()
    assert '"Typing :: Typed"' in content


def test_baked_workflows_support_private_repositories(cookies):
    """Checkout and security workflows use safe private-repository defaults."""
    result = cookies.bake()
    assert result.exit_code == 0
    workflows = result.project_path / ".github" / "workflows"

    ci = (workflows / "ci.yml").read_text()
    assert ci.count("contents: read") == 4

    publish = (workflows / "publish.yml").read_text()
    build_job = publish.split("  publish:", maxsplit=1)[0]
    assert "contents: read" in build_job

    codeql = (workflows / "codeql.yml").read_text()
    private_code_security_opt_in = (
        "${{ github.event.repository.private == false "
        "|| vars.CODE_SECURITY_ENABLED == 'true' }}"
    )
    assert private_code_security_opt_in in codeql
    assert "actions: read" in codeql
    assert "contents: read" in codeql

    zizmor = (workflows / "zizmor.yml").read_text()
    assert f"advanced-security: {private_code_security_opt_in}" in zizmor
    assert "actions: read" in zizmor
    assert "contents: read" in zizmor
