#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup


setup_kwargs = dict(
    test_suite='tests',
)

try:
    setup(
        use_scm_version=True,
        **setup_kwargs
    )
except LookupError:
    # This means the source code was not from git / PyPI
    setup(
        version='{{ cookiecutter.version }}',
        **setup_kwargs
    )

