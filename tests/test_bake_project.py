from contextlib import contextmanager
import datetime
import os
import shlex
import subprocess
import sys

from cookiecutter.utils import rmtree
import jinja2


@contextmanager
def inside_dir(dirpath):
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
def suppressed_github_and_circleci_creation():
    """A context manager which sets an env variable to suppress creating
    GitHub repos and pushing to CircleCI during the hooks.
    """
    os.environ['SKIP_GITHUB_AND_CIRCLECI_CREATION'] = '1'
    try:
        yield
    finally:
        del os.environ['SKIP_GITHUB_AND_CIRCLECI_CREATION']


def errmsg(exception):
    if isinstance(exception, jinja2.exceptions.TemplateSyntaxError):
        return f"Found error at {exception.filename}:{exception.lineno}"
    else:
        return str(exception)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    with suppressed_github_and_circleci_creation():
        result = cookies.bake(*args, **kwargs)
        assert result is not None, result
        assert result.exception is None, errmsg(result.exception)
        assert result.exit_code == 0
    try:
        yield result
    finally:
        rmtree(str(result.project))


def run_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def test_bake_and_run_build(cookies):
    with bake_in_temp_dir(cookies,
                          extra_context={
                              'full_name': 'name "quote" O\'connor',
                              'project_short_description':
                              'The greatest project ever created by name "quote" O\'connor.',
                          }) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'README.md' in found_toplevel_files
        assert 'LICENSE' in found_toplevel_files
        assert 'fix.sh' in found_toplevel_files

        assert run_inside_dir('make test', str(result.project)) == 0
        assert run_inside_dir('make quality', str(result.project)) == 0
        # The supplied Makefile does not support win32
        if sys.platform != "win32":
            output = check_output_inside_dir(
                'make help',
                str(result.project)
            )
            assert b"run precommit quality checks" in \
                output
        license_file_path = result.project.join('LICENSE')
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()
        print("test_bake_and_run_build path", str(result.project))
