from contextlib import contextmanager
import shlex
import os
import pytest
import sys
import subprocess
import yaml
import datetime
from cookiecutter.utils import rmtree

from click.testing import CliRunner

import importlib


_DEPENDENCY_FILE = "pyproject.toml"
_INSTALL_DEPS_COMMANDS = [
    "poetry install",
]


def build_commands(commands):
    cmds = _INSTALL_DEPS_COMMANDS.copy()
    cmds.extend(commands)
    return cmds


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


def run_inside_dir(commands, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param commands: Commands that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        for command in commands:
            subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command, dirpath):
    """Run a command from inside a given directory, returning the command output"""
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project.join('LICENSE')
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert _DEPENDENCY_FILE in found_toplevel_files
        assert 'python_boilerplate' in found_toplevel_files
        assert 'tox.ini' in found_toplevel_files
        assert 'tests' in found_toplevel_files


@pytest.mark.parametrize("extra_context", [
    {},
    {'full_name': 'name "quote" name'},
    {'full_name': "O'connor"}
])
def test_bake_and_run_tests(cookies, extra_context):
    with bake_in_temp_dir(
            cookies,
            extra_context=extra_context,
    ) as result:
        assert result.project.isdir()
        # Test pyproject installs pytest
        dep_file_path = result.project.join(_DEPENDENCY_FILE)
        lines = dep_file_path.readlines()
        assert "pytest = \"*\"\n" in lines
        # Test contents of test file
        test_file_path = result.project.join('tests/test_python_boilerplate.py')
        lines = test_file_path.readlines()
        assert "import pytest" in ''.join(lines)
        # Run the tests
        commands = build_commands(["poetry run invoke test"])
        run_inside_dir(commands, str(result.project))


# def test_bake_and_run_travis_pypi_setup(cookies):
#     # given:
#     with bake_in_temp_dir(cookies) as result:
#         project_path = str(result.project)
#
#         # when:
#         travis_setup_cmd = ('python travis_pypi_setup.py'
#                             ' --repo audreyr/cookiecutter-pypackage'
#                             ' --password invalidpass')
#         run_inside_dir(travis_setup_cmd, project_path)
#         # then:
#         result_travis_config = yaml.load(
#             result.project.join(".travis.yml").open()
#         )
#         min_size_of_encrypted_password = 50
#         assert len(
#             result_travis_config["deploy"]["password"]["secure"]
#         ) > min_size_of_encrypted_password


def test_bake_without_travis_pypi_setup(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={'use_pypi_deployment_with_travis': 'n'}
    ) as result:
        result_travis_config = yaml.load(
            result.project.join(".travis.yml").open(),
            Loader=yaml.FullLoader
        )
        assert "deploy" not in result_travis_config
        assert "python" == result_travis_config["language"]
        # found_toplevel_files = [f.basename for f in result.project.listdir()]


def test_bake_without_author_file(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={'create_author_file': 'n'}
    ) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'AUTHORS.rst' not in found_toplevel_files
        doc_files = [f.basename for f in result.project.join('docs').listdir()]
        assert 'authors.rst' not in doc_files

        # Assert there are no spaces in the toc tree
        docs_index_path = result.project.join('docs/index.rst')
        with open(str(docs_index_path)) as index_file:
            assert 'contributing\n   history' in index_file.read()


@pytest.mark.parametrize("license_info", [
    ('MIT', 'MIT '),
    ('BSD-3-Clause', 'Redistributions of source code must retain the ' +
     'above copyright notice, this'),
    ('ISC', 'ISC License'),
    ('Apache-2.0', 'Licensed under the Apache License, Version 2.0'),
    ('GPL-3.0-only', 'GNU GENERAL PUBLIC LICENSE'),
])
def test_bake_selecting_license(cookies, license_info):
    license, target_string = license_info
    with bake_in_temp_dir(
        cookies,
        extra_context={'open_source_license': license}
    ) as result:
        assert target_string in result.project.join('LICENSE').read()
        assert license in result.project.join(_DEPENDENCY_FILE).read()


def test_bake_not_open_source(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={'open_source_license': 'Not open source'}
    ) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert _DEPENDENCY_FILE in found_toplevel_files
        assert 'LICENSE' not in found_toplevel_files
        assert 'License' not in result.project.join('README.rst').read()
        assert 'license' not in result.project.join(_DEPENDENCY_FILE).read()


def test_not_using_pytest(cookies):
    with bake_in_temp_dir(cookies, extra_context={'use_pytest': 'n'}) as result:
        assert result.project.isdir()
        # Test pyproject doesn't install pytest
        dep_file_path = result.project.join(_DEPENDENCY_FILE)
        lines = dep_file_path.readlines()
        assert "pytest = \"*\"\n" not in lines
        # Test contents of test file
        test_file_path = result.project.join('tests/test_python_boilerplate.py')
        lines = test_file_path.readlines()
        assert "import unittest" in ''.join(lines)
        assert "import pytest" not in ''.join(lines)


def test_using_google_docstrings(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        # Test docs include sphinx extension
        docs_conf_file_path = result.project.join('docs/conf.py')
        lines = docs_conf_file_path.readlines()
        assert "sphinx.ext.napoleon" in ''.join(lines)


def test_not_using_google_docstrings(cookies):
    with bake_in_temp_dir(cookies, extra_context={'use_google_docstrings': 'n'}) as result:
        assert result.project.isdir()
        # Test docs do not include sphinx extension
        docs_conf_file_path = result.project.join('docs/conf.py')
        lines = docs_conf_file_path.readlines()
        assert "sphinx.ext.napoleon" not in ''.join(lines)


# def test_project_with_hyphen_in_module_name(cookies):
#     result = cookies.bake(
#         extra_context={'project_name': 'something-with-a-dash'}
#     )
#     assert result.project is not None
#     project_path = str(result.project)
#
#     # when:
#     travis_setup_cmd = ('python travis_pypi_setup.py'
#                         ' --repo audreyr/cookiecutter-pypackage'
#                         ' --password invalidpass')
#     run_inside_dir(travis_setup_cmd, project_path)
#
#     # then:
#     result_travis_config = yaml.load(
#         open(os.path.join(project_path, ".travis.yml"))
#     )
#     assert "secure" in result_travis_config["deploy"]["password"],\
#         "missing password config in .travis.yml"


@pytest.mark.parametrize("args", [
    ({'command_line_interface': "No command-line interface"}, False),
    ({'command_line_interface': 'click'}, True),
    ({'command_line_interface': 'argparse'}, True),
])
def test_bake_with_no_console_script(cookies, args):
    context, is_present = args
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert ("cli.py" in found_project_files) == is_present

    pyproject_path = os.path.join(project_path, _DEPENDENCY_FILE)
    with open(pyproject_path, 'r') as pyproject_file:
        assert ('[tool.poetry.scripts]' in pyproject_file.read()) == is_present


def test_bake_with_console_script_cli(cookies):
    context = {'command_line_interface': 'click'}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    module_path = os.path.join(project_dir, 'cli.py')
    module_name = '.'.join([project_slug, 'cli'])
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    runner = CliRunner()
    noarg_result = runner.invoke(cli.main)
    assert noarg_result.exit_code == 0
    noarg_output = ' '.join([
        'Replace this message by putting your code into',
        project_slug])
    assert noarg_output in noarg_result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message' in help_result.output


def test_bake_with_argparse_console_script_cli(cookies):
    context = {'command_line_interface': 'argparse'}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    module_path = os.path.join(project_dir, 'cli.py')
    module_name = '.'.join([project_slug, 'cli'])
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    runner = CliRunner()
    noarg_result = runner.invoke(cli.main)
    assert noarg_result.exit_code == 0
    noarg_output = ' '.join([
        'Replace this message by putting your code into',
        project_slug])
    assert noarg_output in noarg_result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message' in help_result.output


@pytest.mark.parametrize("command", [
    "poetry run invoke format --check",
    "poetry run invoke lint",
    "poetry run invoke docs --no-launch",
])
def test_bake_and_run_and_invoke(cookies, command):
    """Run the unit tests of a newly-generated project"""
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        commands = build_commands([command])
        run_inside_dir(commands, str(result.project))
