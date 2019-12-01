.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

ENVIRONMENT := {% if cookiecutter.use_pipenv == 'y' %}pipenv run {% endif %}

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

{%- if cookiecutter.use_pipenv == 'y' %}
init:	
	pipenv --three
	pipenv install --dev --skip-lock
	pipenv install -r requirements_dev.txt
	pipenv run python setup.py develop
{%- endif %}

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

lint: ## check style with flake8
	$(ENVIRONMENT) flake8 {{ cookiecutter.project_slug }} tests

test: ## run tests quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	$(ENVIRONMENT) pytest
{%- else %}
	$(ENVIRONMENT) python setup.py test
{%- endif %}

test-all: ## run tests on every Python version with tox
	$(ENVIRONMENT) tox

coverage: ## check code coverage quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	$(ENVIRONMENT) coverage run --source {{ cookiecutter.project_slug }} -m pytest
{%- else %}
	$(ENVIRONMENT) coverage run --source {{ cookiecutter.project_slug }} setup.py test
{%- endif %}
	$(ENVIRONMENT) coverage report -m
	$(ENVIRONMENT) coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/{{ cookiecutter.project_slug }}.rst
	rm -f docs/modules.rst
	$(ENVIRONMENT) sphinx-apidoc -o docs/ {{ cookiecutter.project_slug }}
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	$(ENVIRONMENT) watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	$(ENVIRONMENT) twine upload dist/*

dist: clean ## builds source and wheel package
	$(ENVIRONMENT) python setup.py sdist
	$(ENVIRONMENT) python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	$(ENVIRONMENT) python setup.py install
