"""
Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
import shutil
import platform

from invoke import task
from pathlib import Path
import webbrowser


ROOT_DIR = Path(__file__).parent
SETUP_FILE = ROOT_DIR.joinpath("setup.py")
TEST_DIR = ROOT_DIR.joinpath("tests")
SOURCE_DIR = ROOT_DIR.joinpath("{{ cookiecutter.project_slug }}")
TOX_DIR = ROOT_DIR.joinpath(".tox")
COVERAGE_FILE = ROOT_DIR.joinpath(".coverage")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")
COVERAGE_REPORT = COVERAGE_DIR.joinpath("index.html")
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("_build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")
PYTHON_DIRS = [str(d) for d in [SOURCE_DIR, TEST_DIR]]


def _delete_file(file):
    try:
        file.unlink(missing_ok=True)
    except TypeError:
        # missing_ok argument added in 3.8
        try:
            file.unlink()
        except FileNotFoundError:
            pass


def _run(c, command):
    return c.run(command, pty=platform.system() != 'Windows')


@task(help={'check': "Checks if source is formatted without applying changes"})
def format(c, check=False):
    """
    Format code
    """
    python_dirs_string = " ".join(PYTHON_DIRS)
    # Run yapf
    yapf_options = '--diff' if check else ''
    _run(c, "black {} {}".format(yapf_options, python_dirs_string))
    # Run isort
    isort_options = '--recursive {}'.format(
        '--check-only --diff' if check else '')
    _run(c, "isort {} {}".format(isort_options, python_dirs_string))


@task
def lint_flake8(c):
    """
    Lint code with flake8
    """
    _run(c, "flake8 {}".format(" ".join(PYTHON_DIRS)))


@task
def lint_pylint(c):
    """
    Lint code with pylint
    """
    _run(c, "pylint {}".format(" ".join(PYTHON_DIRS)))


@task(lint_flake8, lint_pylint)
def lint(c):
    """
    Run all linting
    """


@task
def test(c):
    """
    Run tests
    """
    _run(c, "pytest")


@task(help={'publish': "Publish the result via coveralls"})
def coverage(c, publish=False):
    """
    Create coverage report
    """
    _run(c, "coverage run --source {} -m pytest".format(SOURCE_DIR))
    _run(c, "coverage report")
    if publish:
        # Publish the results via coveralls
        _run(c, "coveralls")
    else:
        # Build a local report
        _run(c, "coverage html")
        webbrowser.open(COVERAGE_REPORT.as_uri())


@task(help={'launch': "Launch documentation in the web browser"})
def docs(c, launch=True):
    """
    Generate documentation
    """
    _run(c, "sphinx-build -b html {} {}".format(DOCS_DIR, DOCS_BUILD_DIR))
    if launch:
        webbrowser.open(DOCS_INDEX.as_uri())


@task
def clean_docs(c):
    """
    Clean up files from documentation builds
    """
    _run(c, "rm -fr {}".format(DOCS_BUILD_DIR))


@task
def clean_build(c):
    """
    Clean up files from package building
    """
    _run(c, "rm -fr build/")
    _run(c, "rm -fr dist/")
    _run(c, "rm -fr .eggs/")
    _run(c, "find . -name '*.egg-info' -exec rm -fr {} +")
    _run(c, "find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(c):
    """
    Clean up python file artifacts
    """
    _run(c, "find . -name '*.pyc' -exec rm -f {} +")
    _run(c, "find . -name '*.pyo' -exec rm -f {} +")
    _run(c, "find . -name '*~' -exec rm -f {} +")
    _run(c, "find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_tests(c):
    """
    Clean up files from testing
    """
    _delete_file(COVERAGE_FILE)
    shutil.rmtree(TOX_DIR, ignore_errors=True)
    shutil.rmtree(COVERAGE_DIR, ignore_errors=True)


@task(pre=[clean_build, clean_python, clean_tests, clean_docs])
def clean(c):
    """
    Runs all clean sub-tasks
    """
    pass


@task(clean)
def dist(c):
    """
    Build source and wheel packages
    """
    _run(c, "poetry build")


@task(pre=[clean, dist])
def release(c):
    """
    Make a release of the python package to pypi
    """
    _run(c, "poetry publish")
