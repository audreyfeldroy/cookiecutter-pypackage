from contextlib import contextmanager
import shlex
import os
import sys
import subprocess
import yaml

from click.testing import CliRunner

if sys.version_info > (3, 0):
    import importlib
else:
    import imp

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


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


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
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" not in found_project_files

    setup_path = os.path.join(project_path, 'setup.py')
    with open(setup_path, 'r') as setup_file:
        assert 'entry_points' not in setup_file.read()


def test_bake_with_console_script_files(cookies):
    context = {'create_console_script': 'y'}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" in found_project_files

    setup_path = os.path.join(project_path, 'setup.py')
    with open(setup_path, 'r') as setup_file:
        assert 'entry_points' in setup_file.read()


def test_bake_with_console_script_cli(cookies):
    context = {'create_console_script': 'y'}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    module_path = os.path.join(project_dir, 'cli.py')
    module_name = '.'.join([project_slug, 'cli'])
    if sys.version_info >= (3, 5):
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
    elif sys.version_info >= (3, 3):
        file_loader = importlib.machinery.SourceFileLoader
        cli = file_loader(module_name, module_path).load_module()
    else:
        cli = imp.load_source(module_name, module_path)
    print(dir(cli))
    noarg_result = runner.invoke(cli.main)
    assert noarg_result.exit_code == 0
    noarg_output = ' '.join(['Add a console script for', project_slug])
    assert noarg_output in noarg_result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Console script for python_boilerplate' in help_result.output
