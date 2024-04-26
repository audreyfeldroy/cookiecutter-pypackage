from contextlib import contextmanager
import shlex
import os
import subprocess
import datetime
import pytest
import re
from packaging import version


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
        pass
        # rmtree(str(result.project))


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
        assert 'setup.py' in found_toplevel_files
        assert 'your_python_project' in found_toplevel_files
        assert 'environment.yml' in found_toplevel_files
        assert 'tests' in found_toplevel_files


def test_bake_and_run_tests(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir('pytest', str(result.project)) == 0
        print("test_bake_and_run_tests path", str(result.project))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break setup.py"""
    with bake_in_temp_dir(
        cookies,
        extra_context={'full_name': 'name "quote" name'}
    ) as result:
        assert result.project.isdir()
        run_inside_dir('pytest', str(result.project)) == 0


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break setup.py"""
    with bake_in_temp_dir(
        cookies,
        extra_context={'full_name': "O'connor"}
    ) as result:
        assert result.project.isdir()
        run_inside_dir('pytest', str(result.project)) == 0


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
            extra_context={'open_source_license': license}
        ) as result:
            assert target_string in result.project.join('LICENSE').read()
            assert license in result.project.join('setup.py').read()


def test_bake_not_open_source(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={'open_source_license': 'Not open source'}
    ) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'setup.py' in found_toplevel_files
        assert 'LICENSE' not in found_toplevel_files
        assert 'License' not in result.project.join('README.rst').read()


def test_bake_with_no_console_script(cookies):
    context = {'command_line_interface': "No command-line interface"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" not in found_project_files

    setup_path = os.path.join(project_path, 'setup.py')
    with open(setup_path, 'r') as setup_file:
        assert 'entry_points' not in setup_file.read()


@pytest.mark.parametrize("use_black,expected", [("y", True), ("n", False)])
def test_black(cookies, use_black, expected):
    with bake_in_temp_dir(
        cookies,
        extra_context={'use_black': use_black}
    ) as result:
        assert result.project.isdir()
        requirements_path = result.project.join('requirements_dev.txt')
        assert ("black" in requirements_path.read()) is expected


@pytest.mark.parametrize("use_circle_ci,expected", [('y', True), ('n', False)])
def test_bake_with_and_wo_circle_ci(cookies, use_circle_ci, expected):
    with bake_in_temp_dir(
        cookies,
        extra_context={'use_circle_ci': use_circle_ci}
    ) as result:
        # assert result.project.isdir()
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert ('.circleci' in found_toplevel_files) is expected


@pytest.mark.parametrize("package", ['numpy', 'matplotlib', 'scipy', 'pyfar'])
@pytest.mark.parametrize("input,expected", [('y', True), ('n', False)])
def test_bake_with_and_wo_packages(cookies, package, input, expected):
    with bake_in_temp_dir(
        cookies,
        extra_context={f'use_{package}': input}
    ) as result:
        assert result.project.isdir()
        requirements_path = result.project.join('requirements_dev.txt')
        assert (package in requirements_path.read()) is expected
        environment_path = result.project.join('environment.yml')
        assert (package in environment_path.read()) is expected
        docs_conf = result.project.join(os.path.join('docs', 'conf.py'))
        assert (f"'{package}': ('" in docs_conf.read()) is expected


@pytest.mark.parametrize("version", [
    '3.12', '3.11', '3.10', '3.9', '3.8', '3.7', '3.6'])
def test_bake_default_python_version(cookies, version):
    with bake_in_temp_dir(
        cookies,
        extra_context={'default_python_version': version,
                       'minimum_python_version': '3.6'}
    ) as result:
        assert result.project.isdir()
        config = result.project.join(os.path.join('.circleci', 'config.yml'))
        assert len(re.findall(version, config.read())) == 7

        run_inside_dir('pytest', str(result.project)) == 0


@pytest.mark.parametrize("min_version", [
    '3.12', '3.11', '3.10', '3.9', '3.8', '3.7', '3.6'])
def test_bake_minimum_python_version(cookies, min_version):
    with bake_in_temp_dir(
        cookies,
        extra_context={'minimum_python_version': min_version,
                       'default_python_version': min_version}
    ) as result:
        assert result.project.isdir()

        config = result.project.join(os.path.join('.circleci', 'config.yml'))
        assert len(re.findall(min_version, config.read())) >= 2
        next_version = min_version
        while True:
            next_version = f'{version.parse(next_version).release[0]}' \
                f'.{version.parse(next_version).release[1]+1}'
            print(next_version)
            if version.parse(next_version) > version.parse('3.12'):
                break
            assert len(re.findall(next_version, config.read())) >= 2

        config = result.project.join('README.rst')
        assert len(re.findall(min_version, config.read())) == 1

        run_inside_dir('pytest', str(result.project)) == 0


def test_bake_incident_with_logic(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        # test for incident in setup.py
        setup = result.project.join('setup.py')
        assert len(re.findall("\n    \'pyfar\',\n", setup.read())) == 1
        assert len(re.findall("\n    \'numpy\',\n", setup.read())) == 1

        # test for incident in docs/conf.py
        setup = result.project.join('docs', 'conf.py')
        assert len(re.findall("\n    \'numpy\': ", setup.read())) == 1


def test_bake_workflow_issue(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        # test for incident in setup.py
        setup = result.project.join(os.path.join(
            '.github', 'workflows', 'create_issue_if_cookiecutter.yml'))
        assert len(re.findall(
            "if: github.event.label.name == 'cookiecutter'",
            setup.read())) == 1
