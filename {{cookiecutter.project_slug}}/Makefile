.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8
        {%- if cookiecutter.use_black == 'y' %} lint/black{% endif %}
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
# Scan thru a Makefile (e.g. this file), looking for target definitions that have a special trailing comment
# (one that starts with two #'s), and consider that comment to be the help text.
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST) # MAKEFILE_LIST names this file itself, plus any include files

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

# NOTE: You might want to make the following invocation of flake8 less strict 
# than what .flake8 specifies (especially if you'll be running this frequently 
# against a work in progress)
#
# To do this, add the following option to the command line:
#
#   --extend-ignore=W191,W391,E203,E265,F841,E722,E301
#
#   E301 = expected 1 blank line, found 0
#   F841 = variable defined but never used
#   E722 = do not use bare 'except'
#
# You might also want to add:
#
#   --max-line-length=256

lint/flake8: ## check style with flake8
	flake8 {{ cookiecutter.project_slug }} tests

{%- if cookiecutter.use_black == 'y' %}
lint/black: ## check style with black
	black --check {{ cookiecutter.project_slug }} tests
{%- endif %}

lint: lint/flake8{%- if cookiecutter.use_black == 'y' %} lint/black{%- endif %} ## check style

test: ## run tests quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	pytest
{%- else %}
	python setup.py test
{%- endif %}

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	coverage run --source {{ cookiecutter.project_slug }} -m pytest
{%- else %}
	coverage run --source {{ cookiecutter.project_slug }} setup.py test
{%- endif %}
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/{{ cookiecutter.project_slug }}.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ {{ cookiecutter.project_slug }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
