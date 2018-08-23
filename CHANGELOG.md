# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - First Syapse Version

### Added

* A `Dockerfile` configuration which can be used for local testing.
* A ready-to-use `setup.py` and `setup.cfg` for building a Python package using [setuptools_scm](https://github.com/pypa/setuptools_scm) for versioning.

* A default [CircleCI](https://circleci.com/) configuration that builds and tests the code
  and publishes to [packagecloud](https://packagecloud.io/)
* Dependency management with [Pipenv](https://docs.pipenv.org/).
* A default [CodeClimate](https://codeclimate.com/) configuration.
* Linter configurations for PEP8 compliance.

### Changed

* Tox support
* switched from unsupport [bumpversion](https://github.com/peritus/bumpversion), to supported fork
[bump2version](https://github.com/c4urself/bump2version)
* Tests for this cookiecutter template are not working.
* Reduced python version support to 2.7, 3.6 and 3.7

### Removed

* Travis support (both this project, and cookie)
* Github issue template (both this project, and cookie)
* appveyor support
* CONTRIBUTING guidelines
* pytest support
* support for named authors
* sphinx documentation support (both this project, and cookie)
* and more ...

## Forked from [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)

