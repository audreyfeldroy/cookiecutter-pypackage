from os.path import abspath
import os
import sys
import webbrowser

import nox

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url


def _browser(path):
  webbrowser.open("file://" + pathname2url(abspath(path)))


@nox.session(python=['2.7', '3.4', '3.5', '3.6', '3.7'], reuse_venv=True)
def prep(session):
  with open('requirements_dev.txt', 'r') as reqs_file:
    reqs = reqs_file.readlines()
  session.install(**reqs)

@nox.session(python=['2.7', '3.4', '3.5', '3.6', '3.7'], reuse_venv=True)
def tests(session):
  session.run('pytest')

@nox.session(python='3.7', reuse_venv=True)
def lint(session):
  session.run('pylint')

@nox.session(python='3.7', reuse_venv=True)
def docs(session):
  for del_file in ['rm -f docs/{{ cookiecutter.project_slug }}.rst',
	                 'rm -f docs/modules.rst']:
    try:
      os.remove(del_file)
    except FileNotFoundError as fnfe:
      pass
  session.run(['sphinx-apidoc', '-o', 'docs/', '{{ cookiecutter.project_slug }}'])
  _browser('docs/')

@nox.session(python='3.7', reuse_venv=True)
def coverage(session):
  commands = 
  for cmd in [
        ['coverage', 'run', '--source', '{{ cookiecutter.project_slug }}', '-m', 'pytest'],
        ['coverage', 'report', '-m'],
        ['coverage', 'html']
      ]:
	  session.run(cmd)
  _browser('htmlcov/index.html')