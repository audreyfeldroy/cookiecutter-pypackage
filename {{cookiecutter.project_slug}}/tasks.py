"""Tasks for maintaining the project"""

from invoke import task
try:
    from pathlib import Path
    Path().expanduser()
except (ImportError, AttributeError):
    from pathlib2 import Path
import webbrowser


ROOT_DIR = Path(__file__).parent
SETUP_FILE = Path(__file__).joinpath("setup.py")
TEST_DIR = ROOT_DIR.joinpath("tests")
SOURCE_DIR = ROOT_DIR.joinpath("pyflipdot")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")
COVERAGE_REPORT = COVERAGE_DIR.joinpath("index.html")
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("_build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")
PYTHON_DIRS = [str(d) for d in [SOURCE_DIR, TEST_DIR]]


@task
def format(c, check=False):
    """
    Format code
    """
    python_dirs_string = " ".join(PYTHON_DIRS)
    # Run yapf
    yapf_options = '--recursive {}'.format('--diff' if check else '--in-place')
    c.run("yapf {} {}".format(yapf_options, python_dirs_string))
    # Run isort
    isort_options = '--recursive {}'.format(
        '--check-only' if check else '')
    c.run("isort {} {}".format(isort_options, python_dirs_string))


@task
def lint(c):
    """
    Lint code
    """
    c.run("flake8 {}".format(SOURCE_DIR))
    c.run("pylint {}".format(SOURCE_DIR))


@task
def test(c):
    """
    Run tests
    """
    c.run("python {} test".format(SETUP_FILE), pty=True)


@task
def coverage(c, publish=False):
    """
    Create coverage report
    """
    c.run("coverage run --source {} -m pytest".format(SOURCE_DIR))
    c.run("coverage report")
    if publish:
        # Publish the results via coveralls
        c.run("coveralls")
    else:
        # Build a local report
        c.run("coverage html")
        webbrowser.open(COVERAGE_REPORT.as_uri())


@task
def docs(c):
    """
    Generate documentation
    """
    c.run("sphinx-build -b html {} {}".format(DOCS_DIR, DOCS_BUILD_DIR))
    webbrowser.open(DOCS_INDEX.as_uri())


@task
def clean_docs(c):
    """
    Clean up files from documentation builds
    """
    c.run("rm -fr {}".format(DOCS_BUILD_DIR))


@task
def clean_build(c):
    """
    Clean up files from package building
    """
    c.run("rm -fr build/")
    c.run("rm -fr dist/")
    c.run("rm -fr .eggs/")
    c.run("find . -name '*.egg-info' -exec rm -fr {} +")
    c.run("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(c):
    """
    Clean up python file artifacts
    """
    c.run("find . -name '*.pyc' -exec rm -f {} +")
    c.run("find . -name '*.pyo' -exec rm -f {} +")
    c.run("find . -name '*~' -exec rm -f {} +")
    c.run("find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_tests(c):
    """
    Clean up files from testing
    """
    c.run("rm -fr .tox/")
    c.run("rm -f .coverage")
    c.run("rm -fr {}".format(COVERAGE_DIR))


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
    c.run("python setup.py sdist")
    c.run("python setup.py bdist_wheel")


@task(pre=[clean, dist])
def release(c):
    """
    Make a release of the python package to pypi
    """
    c.run("twine upload dist/*")
