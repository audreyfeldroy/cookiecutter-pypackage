from contextlib import contextmanager
import shlex
import os
import subprocess
import yaml


@contextmanager
def inside_dir(dirpath):
    "Execute code from inside the given directory"
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


def run_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the exit status"
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))

def check_output_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))

def test_bake_with_defaults(cookies):
    result = cookies.bake()
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
    result = cookies.bake()
    assert result.project.isdir()
    run_inside_dir('python setup.py test', str(result.project)) == 0

def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break setup.py"""
    result = cookies.bake(extra_context={'full_name': 'name "quote" name'})
    assert result.project.isdir()
    run_inside_dir('python setup.py test', str(result.project)) == 0

def test_bake_and_run_travis_pypi_setup(cookies):
    # given:
    result = cookies.bake()
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
    result = cookies.bake()

    output = check_output_inside_dir('make help', str(result.project))
    assert "check code coverage quickly with the default Python" in output
