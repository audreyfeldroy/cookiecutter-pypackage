import datetime
import os
import shlex
import subprocess
from contextlib import contextmanager
from typing import Generator
from unittest.mock import patch

from cookiecutter.utils import rmtree
from pytest_cookies.plugin import Cookies


@contextmanager
def inside_dir(dirpath: str) -> Generator[None, None, None]:
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


def run_inside_dir(command: str, dirpath: str, **kwargs) -> int:
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    :param kwargs: Keyword arguments to pass into subprocess.check_call
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command), **kwargs)


def check_output_inside_dir(command: str, dirpath: str):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


@patch.dict(os.environ, {"COOKIECUTTER_SKIP_POST_GEN_HOOK": "1"})
def test_year_compute_in_license_file(cookies: Cookies):
    result = cookies.bake()
    assert result.project_path
    license_file_path = result.project_path / "LICENSE"
    now = datetime.datetime.now()
    assert str(now.year) in license_file_path.read_text()


@patch.dict(os.environ, {"COOKIECUTTER_SKIP_POST_GEN_HOOK": "1"})
def test_bake_with_defaults(cookies: Cookies):
    result = cookies.bake()
    assert result.project_path
    assert result.project_path.is_dir()
    assert result.exit_code == 0
    assert result.exception is None

    found_toplevel_files = [f.name for f in result.project_path.iterdir()]
    assert "python_boilerplate" in found_toplevel_files
    assert "pyproject.toml" in found_toplevel_files
    assert "tests" in found_toplevel_files


@patch.dict(os.environ, {"COOKIECUTTER_SKIP_POST_GEN_HOOK": "1"})
def test_bake_and_run_tests(cookies: Cookies):
    result = cookies.bake()
    assert result.project_path
    assert result.project_path.is_dir()
    assert run_inside_dir("pytest", str(result.project_path)) == 0


@patch.dict(os.environ, {"COOKIECUTTER_SKIP_POST_GEN_HOOK": "1"})
def test_bake_withspecialchars_and_run_tests(cookies: Cookies):
    """Ensure that a `full_name` with double quotes does not break"""
    result = cookies.bake(extra_context={"full_name": 'name "quote" name'})
    assert result.project_path
    assert result.project_path.is_dir()
    assert run_inside_dir("pytest", str(result.project_path)) == 0


@patch.dict(os.environ, {"COOKIECUTTER_SKIP_POST_GEN_HOOK": "1"})
def test_bake_with_apostrophe_and_run_tests(cookies: Cookies):
    """Ensure that a `full_name` with apostrophes does not break"""
    result = cookies.bake(extra_context={"full_name": "O'connor"})
    assert result.project_path
    assert result.project_path.is_dir()
    assert run_inside_dir("pytest", str(result.project_path)) == 0


@patch.dict(os.environ, {"COOKIECUTTER_SKIP_POST_GEN_HOOK": "1"})
def test_bake_and_run_flake8(cookies: Cookies):
    result = cookies.bake()
    assert result.project_path
    assert result.project_path.is_dir()
    assert run_inside_dir("flake8", str(result.project_path)) == 0


@patch.dict(os.environ, {"COOKIECUTTER_SKIP_POST_GEN_HOOK": "1"})
def test_bake_and_run_black(cookies: Cookies):
    result = cookies.bake()
    assert result.project_path
    assert result.project_path.is_dir()

    assert result.context
    project_slug = result.context["project_slug"]

    with inside_dir(str(result.project_path)):
        find_ps = subprocess.Popen(
            shlex.split(f"find {project_slug}/ -name '*.py' -type f -print"),
            stdout=subprocess.PIPE,
        )
    assert (
        run_inside_dir(
            "xargs black --check", str(result.project_path), stdin=find_ps.stdout
        )
        == 0
    )


@patch.dict(os.environ, {"COOKIECUTTER_SKIP_POST_GEN_HOOK": "1"})
def test_bake_and_run_precommit(cookies: Cookies):

    result = cookies.bake()
    assert result.project_path
    assert result.project_path.is_dir()

    assert result.context

    # install the pre-commit hooks
    run_inside_dir("pre-commit install-hooks", str(result.project_path))
    # run against all files
    assert run_inside_dir("pre-commit run --all-files", str(result.project_path)) == 0


@patch.dict(os.environ, {"COOKIECUTTER_SKIP_POST_GEN_HOOK": "0"})
def test_bake_and_lock_files_created(cookies: Cookies):

    # * note: this test doesn't pass within vscode test runner
    # * pip-compile not found on PATH

    result = cookies.bake()
    assert result.project_path
    assert result.project_path.is_dir()

    assert result.context

    from pathlib import Path

    assert Path.exists(Path(result.project_path) / "requirements.txt")
    assert Path.exists(Path(result.project_path) / "requirements_dev.txt")
