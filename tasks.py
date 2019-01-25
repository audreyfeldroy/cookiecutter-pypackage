"""Development tasks for the cookiecutter template project"""

import webbrowser
from pathlib import Path

from invoke import task

DOCS_DIR = Path('docs')
DOCS_BUILD_DIR = DOCS_DIR.joinpath('_build')
DOCS_INDEX = DOCS_BUILD_DIR.joinpath('index.html')


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
