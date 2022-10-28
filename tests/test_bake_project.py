import datetime
import os
import shlex
import subprocess
from contextlib import contextmanager
from typing import Generator

from cookiecutter.utils import rmtree
from pytest_cookies.plugin import Result


@contextmanager
def inside_dir(dirpath) -> Generator[None, None, None]:
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


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs) -> Generator[Result, None, None]:
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project_path))


def run_inside_dir(command, dirpath, **kwargs) -> int:
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    :param kwargs: Keyword arguments to pass into subprocess.check_call
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command), **kwargs)


def check_output_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path
        license_file_path = result.project_path / "LICENSE"
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read_text()


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path
        assert result.project_path.is_dir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert "python_boilerplate" in found_toplevel_files
        assert "pyproject.toml" in found_toplevel_files
        assert "tests" in found_toplevel_files


def test_bake_and_run_tests(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path
        assert result.project_path.is_dir()
        assert run_inside_dir("pytest", str(result.project_path)) == 0


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break"""
    with bake_in_temp_dir(
        cookies, extra_context={"full_name": 'name "quote" name'}
    ) as result:
        assert result.project_path
        assert result.project_path.is_dir()
        assert run_inside_dir("pytest", str(result.project_path)) == 0


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break"""
    with bake_in_temp_dir(cookies, extra_context={"full_name": "O'connor"}) as result:
        assert result.project_path
        assert result.project_path.is_dir()
        assert run_inside_dir("pytest", str(result.project_path)) == 0


def test_bake_and_run_flake8(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path
        assert result.project_path.is_dir()
        assert run_inside_dir("flake8", str(result.project_path)) == 0


def test_bake_and_run_black(cookies):
    with bake_in_temp_dir(cookies) as result:
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


def test_bake_and_run_precommit(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path
        assert result.project_path.is_dir()

        assert result.context

        # pre-commit requires a git repo to be initialized
        run_inside_dir("git init .", str(result.project_path))
        # install the pre-commit hooks
        run_inside_dir("pre-commit install-hooks", str(result.project_path))
        # run against all files
        assert (
            run_inside_dir("pre-commit run --all-files", str(result.project_path)) == 0
        )
