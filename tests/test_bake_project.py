from contextlib import contextmanager
import shlex
import os
import subprocess
import yaml
import datetime
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
        return subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_year_compute_in_license_file(cookies):
    result = cookies.bake()
    license_file_path = result.project.join('LICENSE')
    now = datetime.datetime.now()
    assert str(now.year) in license_file_path.read()


def test_bake_with_defaults(cookies):

    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'setup.py' in found_toplevel_files
        assert 'python_boilerplate' in found_toplevel_files
        assert 'tox.ini' in found_toplevel_files
        assert 'tests' in found_toplevel_files
        assert 'travis_pypi_setup.py' in found_toplevel_files


def test_bake_and_run_tests(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir('python setup.py test', str(result.project)) == 0
        print("test_bake_and_run_tests path", str(result.project))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break setup.py"""
    with bake_in_temp_dir(cookies, extra_context={'full_name': 'name "quote" name'}) as result:
        assert result.project.isdir()
        run_inside_dir('python setup.py test', str(result.project)) == 0


def test_bake_and_run_travis_pypi_setup(cookies):

    # given:
    with bake_in_temp_dir(cookies) as result:
        project_path = str(result.project)

        # when:
        travis_setup_cmd = ('python travis_pypi_setup.py'
                            ' --repo audreyr/cookiecutter-pypackage --password invalidpass')
        run_inside_dir(travis_setup_cmd, project_path)

        # then:
        result_travis_config = yaml.load(open(os.path.join(project_path, ".travis.yml")))
        assert "secure" in result_travis_config["deploy"]["password"],\
            "missing password config in .travis.yml"


def test_make_help(cookies):
    with bake_in_temp_dir(cookies) as result:
        output = check_output_inside_dir('make help', str(result.project))
        assert b"check code coverage quickly with the default Python" in output

def test_bake_selecting_license(cookies):
    license_strings = {
        'MIT': 'MIT ',
        'BSD': 'Redistributions of source code must retain the above copyright notice, this',
    }
    for license, target_string in license_strings.items():
        with bake_in_temp_dir(cookies, extra_context={'open_source_license': license}) as result:
            assert target_string in result.project.join('LICENSE').read()
