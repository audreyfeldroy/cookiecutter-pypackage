#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_{{ project.repo_name }}
------------

Tests for `{{ project.repo_name }}` module.
"""

import os
import shutil
import unittest

from {{ project.repo_name }} import {{ project.repo_name }}


class TestComplexity(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
