#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
from setuptools import setup


# When https://github.com/pypa/setuptools/issues/1055 is fixed
# this can be moved to setup.cfg
setup(
    use_scm_version={
        'write_to': 'src/{{cookiecutter.project_slug}}/_version.py',
        'write_to_template': '__version__ = "{version}"',
    }
)
# Note: The source code should be either cloned with version control
# or installed from PyPI.
