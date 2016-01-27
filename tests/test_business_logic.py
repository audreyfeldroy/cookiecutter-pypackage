# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: enable=missing-docstring

import unittest2
from {{egg}}.business_logic import BusinessProcess


class TestBusinessProcess(unittest2.TestCase):
    """ The goal, or acceptance criteria should be reminded here
    """

    def setUp(self):
        """ This is run __before__ *each* test
         remove if not needed
        """
        pass

    def tearDown(self):
        """ This is run __after__ *each* test
         remove if not needed
        """
        pass

    def test_something(self):
        """ Prefix you unit test with 'test_'
         so the test collector finds them

        be verbose about the setup, the expectations
        https://xkcd.com/1421/

        you have a number of different assertion tools available
        https://docs.python.org/2/library/unittest.html#test-cases

        the specialized assertions for dicts, lists... are worth a read
        https://docs.python.org/2/library/unittest.html#unittest.TestCase.assertMultiLineEqual

        as they provide a much more useful output in case of failure
        """
        pass
