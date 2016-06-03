from contextlib import contextmanager
import shlex
import os
import subprocess
import yaml
import importlib

from click.testing import CliRunner

runner = CliRunner()

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

def test_bake_with_no_console_script(cookies):
    context = {'create_console_script': 'n'}
    result = cookies.bake(extra_context=context)
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    found_project_files = os.listdir(project_dir)
    assert "__main__.py" not in found_project_files
    
    setup_path = os.path.join(project_path, 'setup.py')
    with open(setup_path, 'r') as setup_file:
        assert 'entry_points' not in setup_file.read()

def test_bake_with_console_script(cookies):
    context = {'create_console_script': 'y'}
    result = cookies.bake(extra_context=context)
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    found_project_files = os.listdir(project_dir)
    assert "__main__.py" in found_project_files
    
    setup_path = os.path.join(project_path, 'setup.py')
    with open(setup_path, 'r') as setup_file:
        assert 'entry_points' in setup_file.read()

    module_path = '.'.join([project_slug, '__main__'])
    main_module = importlib.import_module(module_path)
    noarg_result = runner.invoke(main_module.main)
    assert noarg_result.exit_code == 0
    expected_noarg_output = ' '.join(['Add a console script for', project_slug])
    assert expected_noarg_output in noarg_result.output
    help_result = runner.invoke(main_module.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Console script for python_boilerplate' in help_result.output
    

    

    
    
    
