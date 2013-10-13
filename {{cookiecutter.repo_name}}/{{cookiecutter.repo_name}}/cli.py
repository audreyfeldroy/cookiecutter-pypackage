"""
{{cookiecutter.repo_name}}.

Usage:
  {{cookiecutter.repo_name}} [options] command <param> <another_params>
  {{cookiecutter.repo_name}} [options] another-command <param>

  {{cookiecutter.repo_name}} -h | --help

Options:
  --kw-arg=<kw>         Keyword option description.
  -b --boolean          Boolean option description.
  --debug               Debug.

  -h --help             Show this screen.
"""

from docopt import docopt
import logging

import {{cookiecutter.repo_name}}

log = logging.getLogger(__name__)


def main():
    arguments = docopt(__doc__, version={{cookiecutter.repo_name}}.__version__)
    debug = arguments['--debug']
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    log.debug('arguments: %s', arguments)

