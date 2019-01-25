"""Development tasks for the cookiecutter template project"""

import webbrowser
try:
    from pathlib import Path
    Path().expanduser()
except (ImportError, AttributeError):
    from pathlib2 import Path

from invoke import task

ROOT_DIR = Path(__file__).parent
DOCS_DIR = ROOT_DIR.joinpath('docs')
DOCS_BUILD_DIR = DOCS_DIR.joinpath('_build')
DOCS_INDEX = DOCS_BUILD_DIR.joinpath('index.html')
TEST_DIR = ROOT_DIR.joinpath('tests')


@task
def test(c):
    """
    Run tests
    """
    c.run("pytest".format(TEST_DIR), pty=True)


@task
def docs(c):
    """
    Generate documentation
    """
    c.run("sphinx-build -b html {} {}".format(DOCS_DIR, DOCS_BUILD_DIR))
    webbrowser.open(DOCS_INDEX.absolute().as_uri())


@task
def clean_docs(c):
    """
    Clean up files from documentation builds
    """
    c.run("rm -fr {}".format(DOCS_BUILD_DIR))
