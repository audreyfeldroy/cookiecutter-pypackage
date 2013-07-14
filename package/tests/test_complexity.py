#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_complexity
------------

Tests for `complexity` module.
"""

import os
import shutil
import unittest

from complexity import complexity


class TestComplexity(unittest.TestCase):

    def setUp(self):
        # os.chdir('tests/')
        os.mkdir('output/')

    def test_make_sure_path_exists(self):
        self.assertTrue(complexity.make_sure_path_exists('/usr/'))
        self.assertFalse(
            complexity.make_sure_path_exists(
                '/this-dir-does-not-exist-and-cant-be-created/'
            )
        )

    def test_generate_html(self):
        complexity.generate_html(['index', 'about'], context=None, input_dir='tests/input')
        self.assertTrue(os.path.isfile('output/index.html'))
        self.assertTrue(os.path.isfile('output/about/index.html'))

    def test_generate_context(self):
        context = complexity.generate_context(input_dir='tests/input')
        self.assertEqual(context, {"test": {"1": 2}})



    def tearDown(self):
        shutil.rmtree('output/')

if __name__ == '__main__':
    unittest.main()
