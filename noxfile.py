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


@nox.parametrize('python', ['2.7', '3.5', '3.6', '3.7'])
@nox.session(reuse_venv=True)
def tests(session, python):
  with open('requirements_dev.txt', 'r') as reqs_file:
    reqs = reqs_file.readlines()
  session.install(*reqs)
  session.run('pip', 'list')
  session.run('pytest')


@nox.parametrize('python', '3.7')
@nox.session(reuse_venv=True)
def lint(session, python):
  session.install('pylint')
  session.run('pylint')


@nox.parametrize('python', '3.7')
@nox.session(reuse_venv=True)
def docs(session, python):
  session.install('Sphinx')
  
  for del_file in ['docs/{{ cookiecutter.project_slug }}.rst',
	                 'docs/modules.rst']:
    try:
      os.remove(del_file)
    except FileNotFoundError as fnfe:
      pass
  session.run('sphinx-apidoc', '-o', 'docs/', '{{ cookiecutter.project_slug }}')
  _browser('docs/')


@nox.parametrize('python', '3.7')
@nox.session(reuse_venv=True)
def coverage(session, python):
  for cmd in [
        ['coverage', 'run', '--source', '{{ cookiecutter.project_slug }}', '-m', 'pytest'],
        ['coverage', 'report', '-m'],
        ['coverage', 'html']
      ]:
	  session.run(*cmd)
  _browser('htmlcov/index.html')