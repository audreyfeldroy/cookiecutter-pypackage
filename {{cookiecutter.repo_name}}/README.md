# {{cookiecutter.repo_name}}

[![Build Status](https://secure.travis-ci.org/{{cookiecutter.github_username}}/{{cookiecutter.repo_name}}.png)](http://travis-ci.org/{{cookiecutter.github_username}}/{{cookiecutter.repo_name}})
[![Stories in Ready](https://badge.waffle.io/{{cookiecutter.github_username}}/{{cookiecutter.repo_name}}.png?label=ready)](https://waffle.io/{{cookiecutter.github_username}}/{{cookiecutter.repo_name}}) [![pypi version](https://badge.fury.io/py/{{cookiecutter.repo_name}}.png)](http://badge.fury.io/py/{{cookiecutter.repo_name}})
[![# of downloads](https://pypip.in/d/{{cookiecutter.repo_name}}/badge.png)](https://crate.io/packages/{{cookiecutter.repo_name}}?version=latest)
[![code coverage](https://coveralls.io/repos/{{cookiecutter.github_username}}/{{cookiecutter.repo_name}}/badge.png?branch=master)](https://coveralls.io/r/{{cookiecutter.github_username}}/{{cookiecutter.repo_name}}?branch=master)

## Overview

{{cookiecutter.project_description}}

* features
* and stuff 

## Usage

Install `{{cookiecutter.repo_name}}`:

    pip install {{cookiecutter.repo_name}}

## Documentation

[API Documentation](http://{{cookiecutter.repo_name}}.rtfd.org)

## Testing

Install development requirements:

    pip install -r requirements.txt

Tests can then be run with:

    nosetests

Lint the project with:

    flake8 {{cookiecutter.repo_name}} tests

## API documentation

Generate the documentation with:

    cd docs && PYTHONPATH=.. make singlehtml

To monitor changes to Python files and execute flake8 and nosetests
automatically, execute the following from the root project directory:

    stir
