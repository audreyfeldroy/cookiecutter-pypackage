#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_{{ cookiecutter.project_slug }}
----------------------------------

Tests for `{{ cookiecutter.project_slug }}` module.
"""

import unittest

from {{ cookiecutter.project_slug }} import {{ cookiecutter.project_slug }}


class Test{{ cookiecutter.project_slug|capitalize }}(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
