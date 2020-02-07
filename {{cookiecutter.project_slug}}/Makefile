.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define CLEAN_ALL_TRASH
import os
import shutil
ROOT = os.getcwd()
ignore_dirs = ['venv', '.venv', 'env', '.env', 'ENV']
exclude_files = ['.egg', '.pyc', '*~', '.pyo', '.coverage']
exclude_dirs = ['.egg-info', '__pycache__', '.tox', 'htmlcov', '.pytest_cache']
for root, dirs, files in os.walk(ROOT, topdown=True):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    for dir_ in dirs:
        for i in exclude_dirs:
            if dir_.endswith(i):
                print(os.path.join(root, dir_))
                shutil.rmtree(os.path.join(root, dir_))
    files = [file for file in files if os.path.splitext(file)[1] in exclude_files]
    for file in files:
        print(os.path.join(root, file))
        os.remove(os.path.join(root, file))
endef
export CLEAN_ALL_TRASH

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

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean ## remove all artifacts
	rm -fr build/
	rm -fr dist/
    rm -fr .eggs/
	@python -c "$$CLEAN_ALL_TRASH"

lint: ## check style with flake8
	flake8 {{ cookiecutter.project_slug }} tests

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
