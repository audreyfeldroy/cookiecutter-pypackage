import datetime
import os
import shlex
import subprocess
import sys
from contextlib import contextmanager

import yaml
from cookiecutter.utils import rmtree


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
        license_file_path = result.project.join("LICENSE")
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_repo = os.path.split(project_path)[-1]
    project_slug = project_repo.replace("-", "_")
    project_dir = os.path.join(project_path, project_repo)
    return project_path, project_repo, project_slug, project_dir


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "setup.py" in found_toplevel_files
        assert "python_boilerplate" in found_toplevel_files
        assert "tox.ini" in found_toplevel_files
        assert "tests" in found_toplevel_files


def test_bake_and_run_tests(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert run_inside_dir("make test", str(result.project)) == 0
        print("test_bake_and_run_tests path", str(result.project))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break setup.py"""
    with bake_in_temp_dir(
        cookies, extra_context={"full_name": 'name "quote" name'}
    ) as result:
        assert result.project.isdir()
        assert run_inside_dir("make test", str(result.project)) == 0


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break setup.py"""
    with bake_in_temp_dir(cookies, extra_context={"full_name": "O'connor"}) as result:
        assert result.project.isdir()
        assert run_inside_dir("python setup.py test", str(result.project)) == 0


def test_bake_with_gh_actions(cookies):
    with bake_in_temp_dir(cookies) as result:
        result_github_actions_config = yaml.load(
            result.project.join(".github/workflows/pythonpackage.yml").open(),
            Loader=yaml.FullLoader,
        )
        assert "Python package" == result_github_actions_config["name"]


def test_bake_without_author_file(cookies):
    with bake_in_temp_dir(cookies, extra_context={"create_author_file": "n"}) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "AUTHORS.md" not in found_toplevel_files

        # Check that
        manifest_path = result.project.join("MANIFEST.in")
        with open(str(manifest_path)) as manifest_file:
            assert "AUTHORS.md" not in manifest_file.read()


def test_bake_slug_in_readme_output(cookies):
    with bake_in_temp_dir(cookies) as result:
        _, repo, _, _ = project_info(result)

        readme_path = result.project.join("README.md")
        with open(str(readme_path)) as readme_file:
            assert repo in readme_file.read()


def test_bake_badge_in_readme_output_if_open_source(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={"github_username": "UKHO", "open_source_license": "MIT license"},
    ) as result:
        _, repo, _, _ = project_info(result)

        badge = (
            f"![Python Package](https://github.com/UKHO/{repo}/"
            "workflows/Python%20package/badge.svg)"
        )

        readme_path = result.project.join("README.md")
        with open(str(readme_path)) as readme_file:
            assert badge in readme_file.read()


def test_bake_badge_not_in_readme_output_if_open_source(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "github_username": "UKHO",
            "open_source_license": "Not open source",
        },
    ) as result:
        _, repo, _, _ = project_info(result)

        badge = (
            f"![Python Package](https://github.com/UKHO/{repo}/"
            "workflows/Python%20package/badge.svg)"
        )

        readme_path = result.project.join("README.md")
        with open(str(readme_path)) as readme_file:
            assert badge not in readme_file.read()


def test_make_help(cookies):
    with bake_in_temp_dir(cookies) as result:
        # The supplied Makefile does not support win32
        if sys.platform != "win32":
            output = check_output_inside_dir("make help", str(result.project))
            assert b"check code coverage quickly with the default Python" in output


def test_bake_selecting_license(cookies):
    license_strings = {
        "MIT license": "MIT ",
        "BSD license": "Redistributions of source code must retain the "
        + "above copyright notice, this",
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
    with bake_in_temp_dir(cookies,) as result:
        assert result.project.isdir()
        test_file_path = result.project.join("tests/test_python_boilerplate.py")
        lines = test_file_path.readlines()
        assert "import pytest" in "".join(lines)
        # Test the new pytest target
        assert run_inside_dir("python setup.py pytest", str(result.project)) == 0
        # Test the test alias (which invokes pytest)
        assert run_inside_dir("python setup.py test", str(result.project)) == 0


def test_bake_and_run_lints(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert run_inside_dir("make lint", str(result.project)) == 0


def test_bake_and_run_static_analysis(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert run_inside_dir("make sast", str(result.project)) == 0
