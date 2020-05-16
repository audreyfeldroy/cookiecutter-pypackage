"""Development tasks for the cookiecutter template project"""

import webbrowser
from pathlib import Path
from invoke import task

ROOT_DIR = Path(__file__).parent
DOCS_DIR = ROOT_DIR.joinpath('docs')
DOCS_BUILD_DIR = DOCS_DIR.joinpath('_build')
DOCS_INDEX = DOCS_BUILD_DIR.joinpath('index.html')


def _run(c, command):
    _run(c, command)


@task
def test(c):
    """
    Run tests
    """
    _run(c, "pytest")


@task
def docs(c):
    """
    Generate documentation
    """
    _run(c, "sphinx-build -b html {} {}".format(DOCS_DIR, DOCS_BUILD_DIR))
    webbrowser.open(DOCS_INDEX.absolute().as_uri())


@task
def clean_docs(c):
    """
    Clean up files from documentation builds
    """
    _run(c, "rm -fr {}".format(DOCS_BUILD_DIR))
