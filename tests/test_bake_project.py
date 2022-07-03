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
def suppressed_hook_items(skip_github_and_circleci_creation=True,
                          skip_fix_script=False):
    """A context manager which sets an env variable to suppress different
    hook items

    """
    os.environ['SKIP_GITHUB_AND_CIRCLECI_CREATION'] =\
        '1' if skip_github_and_circleci_creation else '0'
    os.environ['SKIP_FIX_SCRIPT'] = '1' if skip_fix_script else '0'
    try:
        yield
    finally:
        del os.environ['SKIP_GITHUB_AND_CIRCLECI_CREATION']
        del os.environ['SKIP_FIX_SCRIPT']


def errmsg(exception):
    if isinstance(exception, jinja2.exceptions.TemplateSyntaxError):
        return f"Found error at {exception.filename}:{exception.lineno}"
    else:
        return str(exception)


@contextmanager
def bake_in_temp_dir(cookies, skip_fix_script=False, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    with suppressed_hook_items(skip_github_and_circleci_creation=True,
                               skip_fix_script=skip_fix_script):
        result = cookies.bake(*args, **kwargs)
        assert result is not None, result
        assert result.exception is None, errmsg(result.exception)
        assert result.exit_code == 0
    try:
        yield result
    finally:
        rmtree(str(result.project_path))


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
    project_path = str(result.project_path)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, result.context['package_name'])
    return project_path, project_slug, project_dir


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies, skip_fix_script=True) as result:
        assert result.project_path.is_dir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert 'setup.py' in found_toplevel_files
        assert 'python_boilerplate' in found_toplevel_files
        assert 'tox.ini' in found_toplevel_files
        assert 'tests' in found_toplevel_files
        assert 'README.rst' in found_toplevel_files
        assert 'LICENSE' in found_toplevel_files
        assert 'fix.sh' in found_toplevel_files


TRICKY_QUOTE_CHARACTERS_CONTEXT = {
    'full_name': 'name "quote" O\'connor',
    'project_short_description':
    'The greatest project ever created by name "quote" O\'connor.',
}


def test_bake_without_author_file(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={'create_author_file': 'n'},
        skip_fix_script=True,
    ) as result:
        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert 'AUTHORS.rst' not in found_toplevel_files
        doc_files = [f.name for f in (result.project_path / 'docs').iterdir()]
        assert 'authors.rst' not in doc_files

        # Assert there are no spaces in the toc tree
        docs_index_path = result.project_path / 'docs/index.rst'
        with open(str(docs_index_path)) as index_file:
            assert 'contributing\n   history' in index_file.read()

        # Check that
        manifest_path = result.project_path / 'MANIFEST.in'
        with open(str(manifest_path)) as manifest_file:
            assert 'AUTHORS.rst' not in manifest_file.read()


def test_make_help(cookies):
    with bake_in_temp_dir(cookies,
                          skip_fix_script=True) as result:
        # The supplied Makefile does not support win32
        if sys.platform != "win32":
            output = check_output_inside_dir(
                'make help',
                str(result.project_path)
            )
            assert b"run precommit quality checks" in \
                output


def test_bake_selecting_license(cookies):
    license_strings = {
        'MIT license': 'MIT ',
        'BSD license': 'Redistributions of source code must retain the ' +
                       'above copyright notice, this',
        'ISC license': 'ISC License',
        'Apache Software License 2.0':
            'Licensed under the Apache License, Version 2.0',
        'GNU General Public License v3': 'GNU GENERAL PUBLIC LICENSE',
    }
    for license, target_string in license_strings.items():
        with bake_in_temp_dir(
            cookies,
            extra_context={'open_source_license': license},
            skip_fix_script=True,
        ) as result:
            assert target_string in (result.project_path / 'LICENSE').open().read()
            assert license in (result.project_path / 'setup.py').open().read()
            license_file_path = result.project_path / 'LICENSE'
            now = datetime.datetime.now()
            assert str(now.year) in license_file_path.open().read()


def test_bake_not_open_source(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={'open_source_license': 'Not open source'},
        skip_fix_script=True,
    ) as result:
        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert 'setup.py' in found_toplevel_files
        assert 'LICENSE' not in found_toplevel_files
        assert 'License' not in (result.project_path / 'README.rst').open().read()


def test_bake_with_no_console_script(cookies):
    context = {'command_line_interface': "No command-line interface"}
    context.update(TRICKY_QUOTE_CHARACTERS_CONTEXT)
    with suppressed_hook_items():
        result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" not in found_project_files

    setup_path = os.path.join(project_path, 'setup.py')
    with open(setup_path, 'r') as setup_file:
        assert 'entry_points' not in setup_file.read()
    assert run_inside_dir('make citypecheck citypecoverage', str(result.project_path)) == 0
    assert run_inside_dir('make citest cicoverage', str(result.project_path)) == 0
    assert run_inside_dir('make quality', str(result.project_path)) == 0
    assert run_inside_dir('make docs BROWSER=echo', str(result.project_path)) == 0


def test_bake_with_argparse_console_script_files(cookies):
    context = {'command_line_interface': 'Argparse'}
    context.update(TRICKY_QUOTE_CHARACTERS_CONTEXT)
    with suppressed_hook_items():
        result = cookies.bake(extra_context=context)
        assert result is not None
        assert result.project_path is not None

    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" in found_project_files

    setup_path = os.path.join(project_path, 'setup.py')
    with open(setup_path, 'r') as setup_file:
        assert 'entry_points' in setup_file.read()
    assert run_inside_dir('make citypecheck citypecoverage', str(result.project_path)) == 0
    assert run_inside_dir('make citest cicoverage', str(result.project_path)) == 0
    assert run_inside_dir('make quality', str(result.project_path)) == 0
