import datetime
import os
import shlex
import subprocess
import sys
from contextlib import contextmanager

import yaml
from click.testing import CliRunner
from cookiecutter.utils import rmtree

if sys.version_info > (3, 0):
    import importlib
else:
    import imp


TEST_CMD = "python -m pip install -r requirements_dev.txt && pytest"


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
    :param cookies: pytest_cookies.Cookies, cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
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
        result = subprocess.run(shlex.split(command))
        return result.returncode


def check_output_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        result = subprocess.run(shlex.split(command), capture_output=True)
        return result.stdout


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project.join("LICENSE")
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    print("Result")
    print(result)
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, "src", project_slug)
    return project_path, project_slug, project_dir


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "setup.py" in found_toplevel_files
        assert "tox.ini" in found_toplevel_files
        assert "tests" in found_toplevel_files

        srcdir = None
        for f in result.project.listdir():
            if f.basename == "src":
                srcdir = f
        assert srcdir is not None
        assert "python_boilerplate" in [f.basename for f in srcdir.listdir()]


def test_bake_and_run_tests(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir(TEST_CMD, str(result.project)) == 0
        print("test_bake_and_run_tests path", str(result.project))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break setup.py"""
    with bake_in_temp_dir(
        cookies, extra_context={"full_name": 'name "quote" name'}
    ) as result:
        assert result.project.isdir()
        run_inside_dir(TEST_CMD, str(result.project)) == 0


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break setup.py"""
    with bake_in_temp_dir(cookies, extra_context={"full_name": "O'connor"}) as result:
        assert result.project.isdir()
        run_inside_dir(TEST_CMD, str(result.project)) == 0


# def test_bake_and_run_travis_pypi_setup(cookies):
#     # given:
#     with bake_in_temp_dir(cookies) as result:
#         project_path = str(result.project)
#
#         # when:
#         travis_setup_cmd = ('python travis_pypi_setup.py'
#                             ' --repo audreyr/cookiecutter-pypackage --password invalidpass')
#         run_inside_dir(travis_setup_cmd, project_path)
#         # then:
#         result_travis_config = yaml.load(result.project.join(".travis.yml").open())
#         min_size_of_encrypted_password = 50
#         assert len(result_travis_config["deploy"]["password"]["secure"]) > min_size_of_encrypted_password


def test_bake_without_travis_pypi_setup(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"use_pypi_deployment_with_travis": "n"}
    ) as result:
        result_travis_config = yaml.safe_load(result.project.join(".travis.yml").open())
        assert "deploy" not in result_travis_config
        assert "python" == result_travis_config["language"]
        found_toplevel_files = [f.basename for f in result.project.listdir()]


def test_bake_without_author_file(cookies):
    with bake_in_temp_dir(cookies, extra_context={"create_author_file": "n"}) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "AUTHORS.rst" not in found_toplevel_files
        doc_files = [f.basename for f in result.project.join("docs").listdir()]
        assert "authors.rst" not in doc_files

        # Assert there are no spaces in the toc tree
        docs_index_path = result.project.join("docs/index.rst")
        with open(str(docs_index_path)) as index_file:
            assert "contributing\n   history" in index_file.read()

        # Check that
        manifest_path = result.project.join("MANIFEST.in")
        with open(str(manifest_path)) as manifest_file:
            assert "AUTHORS.rst" not in manifest_file.read()


def test_make_help(cookies):
    with bake_in_temp_dir(cookies) as result:
        output = check_output_inside_dir("make help", str(result.project))
        assert b"check code coverage quickly with the default Python" in output


def test_bake_selecting_license(cookies):
    license_strings = {
        "MIT license": "MIT ",
        "BSD license": "Redistributions of source code must retain the above copyright notice, this",
        "ISC license": "ISC License",
        "Apache Software License 2.0": "Licensed under the Apache License, Version 2.0",
        "GNU General Public License v3": "GNU GENERAL PUBLIC LICENSE",
    }
    for license, target_string in license_strings.items():
        with bake_in_temp_dir(
            cookies, extra_context={"open_source_license": license}
        ) as result:
            assert target_string in result.project.join("LICENSE").read()
            assert license in result.project.join("setup.py").read()


def test_bake_not_open_source(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"open_source_license": "Not open source"}
    ) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "setup.py" in found_toplevel_files
        assert "LICENSE" not in found_toplevel_files
        assert "License" not in result.project.join("README.md").read()


def test_using_pytest(cookies):
    with bake_in_temp_dir(cookies, extra_context={"use_pytest": "y"}) as result:
        assert result.project.isdir()
        test_file_path = result.project.join("tests/test_python_boilerplate.py")
        lines = test_file_path.readlines()
        assert "import pytest" in "".join(lines)
        # Test the new pytest target
        run_inside_dir("python setup.py pytest", str(result.project)) == 0
        # Test the test alias (which invokes pytest)
        run_inside_dir(TEST_CMD, str(result.project)) == 0


def test_not_using_pytest(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        test_file_path = result.project.join("tests/test_python_boilerplate.py")
        lines = test_file_path.readlines()
        assert "import unittest" in "".join(lines)
        assert "import pytest" not in "".join(lines)


# def test_project_with_hyphen_in_module_name(cookies):
#     result = cookies.bake(extra_context={'project_name': 'something-with-a-dash'})
#     assert result.project is not None
#     project_path = str(result.project)
#
#     # when:
#     travis_setup_cmd = ('python travis_pypi_setup.py'
#                         ' --repo audreyr/cookiecutter-pypackage --password invalidpass')
#     run_inside_dir(travis_setup_cmd, project_path)
#
#     # then:
#     result_travis_config = yaml.load(open(os.path.join(project_path, ".travis.yml")))
#     assert "secure" in result_travis_config["deploy"]["password"],\
#         "missing password config in .travis.yml"


def test_bake_with_no_console_script(cookies):
    context = {"command_line_interface": "No command-line interface"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" not in found_project_files

    setup_path = os.path.join(project_path, "setup.py")
    with open(setup_path, "r") as setup_file:
        assert "entry_points" not in setup_file.read()


def test_bake_with_console_script_files(cookies):
    context = {"command_line_interface": "click"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" in found_project_files

    setup_path = os.path.join(project_path, "setup.py")
    with open(setup_path, "r") as setup_file:
        assert "entry_points" in setup_file.read()


def test_bake_with_console_script_cli(cookies):
    context = {"command_line_interface": "click"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    module_path = os.path.join(project_dir, "cli.py")
    module_name = ".".join([project_slug, "cli"])
    if sys.version_info >= (3, 5):
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
    elif sys.version_info >= (3, 3):
        file_loader = importlib.machinery.SourceFileLoader
        cli = file_loader(module_name, module_path).load_module()
    else:
        cli = imp.load_source(module_name, module_path)
    runner = CliRunner()
    noarg_result = runner.invoke(cli.cli)

    print(noarg_result.output)

    assert noarg_result.exit_code == 0
    assert "Show this message" in noarg_result.output
    assert "Console script for python_boilerplate" in noarg_result.output
    help_result = runner.invoke(cli.cli, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message" in help_result.output


def test_bake_selecting_license(cookies):
    license_strings = {
        "MIT license": "MIT ",
        "BSD license": "Redistributions of source code must retain the above copyright notice, this",
        "ISC license": "ISC License",
        "Apache Software License 2.0": "Licensed under the Apache License, Version 2.0",
        "GNU General Public License v3": "GNU GENERAL PUBLIC LICENSE",
    }
    for license, target_string in license_strings.items():
        with bake_in_temp_dir(
            cookies, extra_context={"open_source_license": license}
        ) as result:
            assert target_string in result.project.join("LICENSE").read()
            assert license in result.project.join("setup.py").read()


def test_bake_github_org(cookies):
    for k, context in zip(
        ["github_org", "github_username"],
        [
            {
                "github_org": "steadysense",
                "github_user": "mofe23",
                "add_pyup_badge": "y",
            },
            {"github_org": "", "github_username": "mofe23", "add_pyup_badge": "y"},
        ],
    ):
        pyup = "https://pyup.io/repos/github/" + context[k]
        travis = "https://travis-ci.org/" + context[k]
        repo = "https://github.com/" + context[k]
        travis_yml = "repo: " + context[k]

        with bake_in_temp_dir(cookies, extra_context=context) as result:
            assert pyup in result.project.join("README.md").read()
            assert travis in result.project.join("README.md").read()
            assert repo in result.project.join("CONTRIBUTING.rst").read()
            assert repo in result.project.join("setup.py").read()
            assert repo in result.project.join("docs/installation.rst").read()
            assert travis_yml in result.project.join(".travis.yml").read()


def test_bake_and_make_dist(cookies):
    version = "0.1.0"
    with bake_in_temp_dir(cookies, extra_context={"version": version}) as result:
        project_path, project_slug, project_dir = project_info(result)
        assert result.project.isdir()
        run_inside_dir("make dist", str(result.project)) == 0
        found_dist_files = [d.basename for d in result.project.join("dist").listdir()]
        import pprint

        pprint.pprint(found_dist_files)
        """
        "python_boilerplate/dist/python_boilerplate-0.1.0-py2.py3-none-any.whl"
                                "python_boilerplate-0.1.0-py2.py3-none-any.whl"
        """
        assert f"{project_slug}-{version}-py2.py3-none-any.whl" in found_dist_files
        assert f"{project_slug}-{version}.tar.gz" in found_dist_files
