.PHONY: help init update clean clean-pyc clean-docs clean-build lint test test-all coverage docs release sdist

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

init:	
	pipenv --three
	pipenv install --dev --skip-lock
	pipenv install -r requirements_dev.txt
	pipenv run setup.py develop

update:
	pipenv update
	pipenv lock -r

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-docs:
	make -C docs clean

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	pipenv run flake8 --output-file=.flake8.txt {{ cookiecutter.module_name }} tests 	

test:
	pipenv run py.test --junitxml=.tests_report.xml

test-all:
	tox

coverage:
	pipenv run py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=requests tests

docs: clean-docs
	make -C docs html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

release: clean
	pipenv run setup.py sdist upload
	pipenv run setup.py bdist_wheel upload

sdist: clean
	pipenv run setup.py sdist
	pipenv run setup.py bdist_wheel upload
	ls -l dist
